#!/usr/bin/env node

import { copyFile, mkdir, writeFile } from "node:fs/promises";
import { appendFileSync, chmodSync, createReadStream, createWriteStream, existsSync, mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { Readable } from "node:stream";
import { pipeline } from "node:stream/promises";
import pino from "pino";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc.js";
import timezone from "dayjs/plugin/timezone.js";

const TIMESTAMP_PREFIX_RE = /^\d+_/;
const SKILL_NAME = "aios-transfer-file";

dayjs.extend(utc);
dayjs.extend(timezone);

const warnedLogDirs = new Set();

function beijingTime() {
  return dayjs().tz("Asia/Shanghai").format("YYYY-MM-DDTHH:mm:ss.SSSZ");
}

function resolveLogDir() {
  const configured = process.env.AIOS_LOG_DIR?.trim();
  if (configured) {
    return configured;
  }

  const root = process.env.AIOS_ROOT?.trim();
  if (root) {
    return path.join(root, "logs");
  }

  const dataDir = process.env.AIOS_DATA_DIR?.trim() || process.env.AIOS_KERNEL_DATA_DIR?.trim();
  if (dataDir) {
    return path.join(path.dirname(dataDir), "logs");
  }

  return undefined;
}

function getDailyLogFile() {
  const logDir = resolveLogDir();
  if (!logDir) {
    return undefined;
  }

  try {
    mkdirSync(logDir, { recursive: true });
    const logFile = path.join(logDir, `${SKILL_NAME}-${dayjs().tz("Asia/Shanghai").format("YYYYMMDD")}.log`);
    if (!existsSync(logFile)) {
      writeFileSync(logFile, "", { mode: 0o660 });
      chmodSync(logFile, 0o660);
    }
    return logFile;
  } catch (error) {
    if (!warnedLogDirs.has(logDir)) {
      warnedLogDirs.add(logDir);
      const message = error instanceof Error ? error.message : String(error);
      process.stderr.write(`[logger] ${beijingTime()} failed to initialize daily log file in ${logDir}: ${message}\n`);
    }
    return undefined;
  }
}

function createDestination() {
  return {
    write(line) {
      process.stderr.write(line);
      const logFile = getDailyLogFile();
      if (logFile) {
        appendFileSync(logFile, line, { mode: 0o660 });
      }
    }
  };
}

const logger = pino({
  name: SKILL_NAME,
  level: process.env.AIOS_LOG_LEVEL || "info",
  timestamp: () => `,"ts":"${beijingTime()}"`,
  base: null
}, createDestination());

function fail(message, code = 1) {
  logger.error({ error: { message } }, "aios-transfer-file failed");
  process.exit(code);
}

function readRequiredEnv(name) {
  const value = process.env[name]?.trim();
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

function readOptionalEnv(name, fallback) {
  const value = process.env[name] ?? fallback;
  if (!value || value.trim().length === 0) {
    return undefined;
  }
  return value.trim();
}

function readBooleanEnv(name, fallback) {
  const value = process.env[name];
  if (!value || value.trim().length === 0) {
    return fallback;
  }

  const normalized = value.trim().toLowerCase();
  if (normalized === "true" || normalized === "1" || normalized === "yes") {
    return true;
  }
  if (normalized === "false" || normalized === "0" || normalized === "no") {
    return false;
  }

  throw new Error(`${name} must be one of true,false,1,0,yes,no`);
}

function ensureOptionalUrl(name, value) {
  if (!value) {
    return undefined;
  }

  try {
    const url = new URL(value);
    if (!url.protocol || !url.hostname) {
      throw new Error("missing protocol or hostname");
    }
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    throw new Error(`${name} must be a valid URL: ${reason}`);
  }

  return value;
}

function parseFileInputUri(rawUri) {
  const trimmed = rawUri.split(" ", 1)[0].trim();
  const match = /^file_input:\/\/([^/]+)\/(.+)$/.exec(trimmed);
  if (!match) {
    throw new Error(`Malformed file input URI: ${rawUri}`);
  }

  const [, bucket, key] = match;
  if (!bucket || !key) {
    throw new Error(`Malformed file input URI: ${rawUri}`);
  }

  return { sourceUri: trimmed, bucket, key };
}

function makeTimestampedName(name, { replaceSpaces }) {
  const normalized = (replaceSpaces ? name.replaceAll(" ", "_") : name).replace(TIMESTAMP_PREFIX_RE, "");
  return `${Math.floor(Date.now() / 1000)}_${normalized}`;
}

function resolveOutboxEnvName() {
  if (readOptionalEnv("AIOS_S3_AGENT_OUTBOX_BUCKET")) {
    return "AIOS_S3_AGENT_OUTBOX_BUCKET";
  }
  throw new Error("Missing required environment variable: AIOS_S3_AGENT_OUTBOX_BUCKET");
}

async function loadAwsSdk() {
  try {
    return await import("@aws-sdk/client-s3");
  } catch {
    throw new Error("Missing dependency: @aws-sdk/client-s3. Run npm install in this skill directory.");
  }
}

async function createS3Client() {
  const sdk = await loadAwsSdk();
  const endpoint = ensureOptionalUrl("AIOS_S3_ENDPOINT", readOptionalEnv("AIOS_S3_ENDPOINT"));
  const region = readOptionalEnv("AIOS_S3_REGION", "us-east-1") ?? "us-east-1";
  const accessKeyId = readRequiredEnv("AIOS_S3_ACCESS_KEY_ID");
  const secretAccessKey = readRequiredEnv("AIOS_S3_SECRET_ACCESS_KEY");
  const forcePathStyle = readBooleanEnv("AIOS_S3_FORCE_PATH_STYLE", true);

  return {
    sdk,
    client: new sdk.S3Client({
      endpoint,
      region,
      forcePathStyle,
      credentials: {
        accessKeyId,
        secretAccessKey
      }
    })
  };
}

async function ensureDirectory(dirPath) {
  await mkdir(dirPath, { recursive: true });
  return dirPath;
}

async function writeBodyToFile(body, destination) {
  if (!body) {
    throw new Error("S3 object body is empty");
  }

  if (typeof body.transformToWebStream === "function") {
    await pipeline(Readable.fromWeb(body.transformToWebStream()), createWriteStream(destination));
    return;
  }

  if (typeof body.transformToByteArray === "function") {
    await writeFile(destination, Buffer.from(await body.transformToByteArray()));
    return;
  }

  if (body instanceof Readable) {
    await pipeline(body, createWriteStream(destination));
    return;
  }

  if (body instanceof Uint8Array) {
    await writeFile(destination, body);
    return;
  }

  throw new Error("Unsupported S3 object body type");
}

async function ensureBucket(clientBundle, bucket) {
  const { sdk, client } = clientBundle;
  try {
    await client.send(new sdk.HeadBucketCommand({ Bucket: bucket }));
    return;
  } catch {}

  const region = readOptionalEnv("AIOS_S3_REGION", "us-east-1") ?? "us-east-1";
  try {
    await client.send(new sdk.CreateBucketCommand(
      region === "us-east-1"
        ? { Bucket: bucket }
        : {
            Bucket: bucket,
            CreateBucketConfiguration: { LocationConstraint: region }
          }
    ));
  } catch (error) {
    if (region !== "us-east-1") {
      await client.send(new sdk.CreateBucketCommand({ Bucket: bucket }));
      return;
    }
    throw error;
  }
}

async function downloadUri(options) {
  const workspace = path.resolve(options.workspace);
  const inputDir = await ensureDirectory(path.join(workspace, options.inputDirName));
  const { sourceUri, bucket, key } = parseFileInputUri(options.uri);
  const basename = path.basename(key);
  if (!basename) {
    throw new Error(`Malformed file input URI: ${options.uri}`);
  }

  const localName = makeTimestampedName(basename, { replaceSpaces: false });
  const localPath = path.join(inputDir, localName);
  const { sdk, client } = await createS3Client();
  const response = await client.send(new sdk.GetObjectCommand({
    Bucket: bucket,
    Key: key
  }));

  await writeBodyToFile(response.Body, localPath);

  console.log(JSON.stringify({
    bucket,
    key,
    sourceUri,
    localPath,
    localName
  }));
}

async function uploadFile(options) {
  const workspace = path.resolve(options.workspace);
  const outputDir = await ensureDirectory(path.join(workspace, options.outputDirName));
  const sourcePath = path.resolve(options.source);
  const outboxEnvName = resolveOutboxEnvName();
  const bucket = readRequiredEnv(outboxEnvName);
  const stagedName = makeTimestampedName(path.basename(sourcePath), { replaceSpaces: true });
  const stagedPath = path.join(outputDir, stagedName);

  await copyFile(sourcePath, stagedPath);

  const clientBundle = await createS3Client();
  await ensureBucket(clientBundle, bucket);
  await clientBundle.client.send(new clientBundle.sdk.PutObjectCommand({
    Bucket: bucket,
    Key: stagedName,
    Body: createReadStream(stagedPath)
  }));

  const result = {
    bucket,
    key: stagedName,
    sourcePath,
    stagedPath,
    uri: `file_output://${bucket}/${stagedName}`
  };
  console.log(options.uriOnly ? result.uri : JSON.stringify(result));
}

function parseArgs(argv) {
  const args = {
    command: undefined,
    workspace: ".",
    inputDirName: "file_input",
    outputDirName: "file_output",
    uri: undefined,
    source: undefined,
    uriOnly: false
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "-h" || token === "--help") {
      printHelp();
      process.exit(0);
    }
    if (!args.command) {
      args.command = token;
      continue;
    }
    if (token === "--workspace") {
      args.workspace = argv[++index] ?? fail("Missing value for --workspace");
      continue;
    }
    if (token === "--input-dir-name") {
      args.inputDirName = argv[++index] ?? fail("Missing value for --input-dir-name");
      continue;
    }
    if (token === "--output-dir-name") {
      args.outputDirName = argv[++index] ?? fail("Missing value for --output-dir-name");
      continue;
    }
    if (token === "--uri") {
      args.uri = argv[++index] ?? fail("Missing value for --uri");
      continue;
    }
    if (token === "--source") {
      args.source = argv[++index] ?? fail("Missing value for --source");
      continue;
    }
    if (token === "--uri-only") {
      args.uriOnly = true;
      continue;
    }

    fail(`Unknown argument: ${token}`);
  }

  return args;
}

function printHelp() {
  console.log(`Usage:
  node scripts/transfer_s3.mjs download-uri --uri "file_input://bucket/path/to/file.bin" [--workspace .] [--input-dir-name file_input]
  node scripts/transfer_s3.mjs upload-file --source "/abs/path/to/file.bin" [--workspace .] [--output-dir-name file_output] [--uri-only]

Commands:
  download-uri   Download a file_input:// URI into the workspace file_input directory.
  upload-file    Copy a local file into file_output and upload it to the outbox bucket root.
`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.command === "download-uri") {
    if (!args.uri) {
      fail("download-uri requires --uri");
    }
    await downloadUri(args);
    return;
  }
  if (args.command === "upload-file") {
    if (!args.source) {
      fail("upload-file requires --source");
    }
    await uploadFile(args);
    return;
  }

  printHelp();
  process.exit(args.command ? 1 : 0);
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  logger.error({
    error: error instanceof Error
      ? { message, stack: error.stack }
      : { message }
  }, "aios-transfer-file failed");
  process.exit(1);
});
