#!/usr/bin/env node
// Acquire the pinned EIN.LLC activation continuation 0.1.5 archive and run its
// existing discover, assess, prepare, resume, status, show, and cancel commands.
import { createHash } from "node:crypto";
import { constants, fchmodSync, mkdirSync, openSync, readFileSync, writeSync, closeSync } from "node:fs";
import { lstat, mkdir, open, readFile, realpath, rm } from "node:fs/promises";
import path from "node:path";
import { Readable } from "node:stream";
import { fileURLToPath, pathToFileURL } from "node:url";
import { gunzipSync } from "node:zlib";

const SKILL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const FETCH_TIMEOUT_MS = 15_000;
const CONTEXT_LIMIT = 32 * 1024;
const STDOUT_LIMIT = 64 * 1024;
const TASK_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{7,79}$/;
const CLIENT_COMMANDS = new Set(["discover", "assess", "prepare", "resume", "status", "show", "cancel"]);
const TRANSPORTS = new Set(["http", "mcp", "a2a", "a2a-rest"]);
const BOOLEAN_FLAGS = new Set([
  "show-claim-url", "reassess", "pay", "settle", "sign", "wallet", "claim", "attest", "register", "file",
]);
const KNOWN_FLAGS = new Set([
  ...BOOLEAN_FLAGS,
  "work", "public-root", "caller", "command", "state", "task-id", "customer-key-file", "context",
  "intended-email-file", "grant-file", "grant-origin", "base-url", "lane", "transport",
  "catalog-transport", "deadline-ms",
]);
const REFUSALS = new Set([
  "redirect_refused", "cross_origin_refused", "public_root_rejected", "origin_refused", "lane_refused",
  "payment_refused", "action_refused", "tampered_archive", "tampered_descriptor", "tampered_source",
  "truncated_archive", "truncated_descriptor", "source_disagreement", "traversal_refused", "link_refused",
  "device_refused", "fifo_refused", "body_too_large", "input_rejected", "flag_rejected", "fetch_failed",
  "overwrite_refused", "closure_failed", "output_withheld", "output_limit", "directory_rejected",
]);

export const PIN = JSON.parse(readFileSync(path.join(SKILL_ROOT, "references", "continuation-pin.json"), "utf8"));

export function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function code(name) {
  const error = new Error(name);
  error.code = name;
  return error;
}

function baseResult(extra = {}) {
  return {
    usefulness: "unknown",
    paymentCreated: false,
    claimPerformed: false,
    filingAuthorization: false,
    ...extra,
  };
}

export function parseArgs(argv) {
  const [command, ...rest] = argv;
  const flags = {};
  for (let index = 0; index < rest.length; index += 1) {
    const item = rest[index];
    if (!item.startsWith("--")) throw code("flag_rejected");
    const key = item.slice(2);
    if (!KNOWN_FLAGS.has(key)) throw code("flag_rejected");
    if (BOOLEAN_FLAGS.has(key)) {
      flags[key] = true;
      continue;
    }
    const value = rest[index + 1];
    if (value === undefined || value.startsWith("--")) throw code("flag_rejected");
    flags[key] = value;
    index += 1;
  }
  return { command, flags };
}

function finish(status, payload) {
  process.stdout.write(`${JSON.stringify(payload)}\n`);
  process.exit(status);
}

export function allowedPublicRoot(value) {
  if (value === undefined) {
    return { origin: PIN.origin, receiving: "hosted_descriptor" };
  }
  let url;
  try { url = new URL(value); } catch { throw code("public_root_rejected"); }
  const loopback = url.protocol === "http:" && (url.hostname === "127.0.0.1" || url.hostname === "[::1]");
  if (!loopback || !url.port || url.username || url.password || url.pathname !== "/" || url.search || url.hash) {
    throw code("public_root_rejected");
  }
  return { origin: url.origin, receiving: "local_receiving" };
}

function pinnedRequest(origin, pathname) {
  const url = new URL(pathname, origin);
  if (url.origin !== origin || url.pathname !== pathname || url.search || url.hash || url.username) {
    throw code("cross_origin_refused");
  }
  return url;
}

async function readBounded(response, exactBytes, truncatedCode) {
  const reader = response.body?.getReader();
  if (!reader) throw code("fetch_failed");
  const chunks = [];
  let total = 0;
  try {
    while (true) {
      const next = await reader.read();
      if (next.done) break;
      total += next.value.byteLength;
      if (total > exactBytes) {
        await reader.cancel();
        throw code("body_too_large");
      }
      chunks.push(Buffer.from(next.value));
    }
  } catch (error) {
    if (error?.code && REFUSALS.has(error.code)) throw error;
    throw code("fetch_failed");
  }
  if (total < exactBytes) throw code(truncatedCode);
  return Buffer.concat(chunks);
}

async function getExact(origin, pathname, exactBytes, truncatedCode) {
  let current = pinnedRequest(origin, pathname);
  for (let hop = 0; hop < 3; hop += 1) {
    let response;
    try {
      response = await fetch(current, {
        method: "GET",
        redirect: "manual",
        headers: { accept: "*/*", "accept-encoding": "identity" },
        signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
      });
    } catch {
      throw code("fetch_failed");
    }
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get("location");
      await response.body?.cancel();
      if (!location) throw code("redirect_refused");
      let next;
      try { next = new URL(location, current); } catch { throw code("redirect_refused"); }
      if (next.origin !== origin || next.pathname !== pathname || next.search || next.hash || next.username || next.password) {
        throw code("redirect_refused");
      }
      current = next;
      continue;
    }
    if (response.status !== 200) {
      await response.body?.cancel();
      throw code("fetch_failed");
    }
    const bytes = await readBounded(response, exactBytes, truncatedCode);
    return bytes;
  }
  throw code("redirect_refused");
}

function readOctal(buffer, start, length) {
  const raw = buffer.subarray(start, start + length);
  const zero = raw.indexOf(0);
  const text = (zero === -1 ? raw : raw.subarray(0, zero)).toString("utf8").trim();
  if (!/^[0-7]+$/.test(text)) throw code("tampered_archive");
  return Number.parseInt(text, 8);
}

function cString(buffer) {
  const zero = buffer.indexOf(0);
  return (zero === -1 ? buffer : buffer.subarray(0, zero)).toString("utf8");
}

function headerChecksum(header) {
  let sum = 0;
  for (let index = 0; index < 512; index += 1) sum += index >= 148 && index < 156 ? 32 : header[index];
  return sum;
}

function safeMember(name) {
  if (!name || name.startsWith("/") || name.includes("\\") || name.includes("\0")) throw code("traversal_refused");
  const parts = name.split("/");
  if (parts.some((part) => part === "" || part === "." || part === "..")) throw code("traversal_refused");
  return name;
}

function memberName(header) {
  const name = cString(header.subarray(0, 100));
  const prefix = cString(header.subarray(345, 500));
  if (prefix && (prefix.startsWith("/") || prefix.includes(".."))) throw code("traversal_refused");
  return prefix ? `${prefix}/${name}` : name;
}

export function extractPinnedArchive(archive, destination) {
  let raw;
  try {
    raw = gunzipSync(archive, { maxOutputLength: PIN.files.archive.uncompressedBytes });
  } catch {
    throw code("tampered_archive");
  }
  const expected = new Map(PIN.members.map((member) => [`${PIN.prefix}${member.path}`, member]));
  const seen = new Set();
  let offset = 0;
  while (offset + 512 <= raw.length) {
    const header = raw.subarray(offset, offset + 512);
    offset += 512;
    if (header.every((byte) => byte === 0)) {
      if (!raw.subarray(offset).every((byte) => byte === 0)) throw code("tampered_archive");
      break;
    }
    if (headerChecksum(header) !== readOctal(header, 148, 8)) throw code("tampered_archive");
    const magic = header.subarray(257, 263);
    const gnu = header.subarray(257, 265).equals(Buffer.from("ustar  \0"));
    if (!magic.equals(Buffer.from("ustar\0")) && !gnu) throw code("tampered_archive");
    const typeflag = header[156];
    if (typeflag === 49 || typeflag === 50) throw code("link_refused");
    if (typeflag === 51 || typeflag === 52) throw code("device_refused");
    if (typeflag === 54) throw code("fifo_refused");
    if (typeflag !== 48 && typeflag !== 0) throw code("traversal_refused");
    if (cString(header.subarray(157, 257))) throw code("traversal_refused");
    const name = safeMember(memberName(header));
    const size = readOctal(header, 124, 12);
    const mode = readOctal(header, 100, 8);
    const dataStart = offset;
    const dataEnd = offset + size;
    offset += Math.ceil(size / 512) * 512;
    if (dataEnd > raw.length) throw code("truncated_archive");
    const spec = expected.get(name);
    const body = raw.subarray(dataStart, dataEnd);
    if (!spec || seen.has(name) || body.length !== spec.bytes || sha256(body) !== spec.sha256 || mode !== spec.mode) {
      throw code("tampered_archive");
    }
    seen.add(name);
    const relative = name.slice(PIN.prefix.length);
    const target = path.resolve(destination, relative);
    const root = path.resolve(destination);
    if (target !== root && !target.startsWith(`${root}${path.sep}`)) throw code("traversal_refused");
    writeExclusive(target, body, spec.mode);
  }
  if (seen.size !== expected.size || raw.length !== PIN.files.archive.uncompressedBytes) throw code("tampered_archive");
}

function writeExclusive(target, body, mode) {
  mkdirSync(path.dirname(target), { recursive: true, mode: 0o700 });
  const fd = openSync(target, constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW, mode);
  try {
    writeSync(fd, body);
    fchmodSync(fd, mode);
  } finally {
    closeSync(fd);
  }
}

async function readRegular(file, maxBytes) {
  let info;
  try {
    info = await lstat(file);
  } catch (error) {
    if (error?.code === "ENOENT") throw code("missing_input");
    throw error;
  }
  if (info.isSymbolicLink()) throw code("link_refused");
  if (info.isFIFO()) throw code("fifo_refused");
  if (!info.isFile() || info.size > maxBytes) throw code("input_rejected");
  const fd = await open(file, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
  try {
    const stat = await fd.stat();
    if (!stat.isFile() || stat.size > maxBytes) throw code("input_rejected");
    return await fd.readFile();
  } finally {
    await fd.close();
  }
}

export async function verifyCallerTree(caller) {
  let root;
  try {
    root = await realpath(caller);
  } catch (error) {
    if (error?.code === "ENOENT") throw code("missing_input");
    throw error;
  }
  for (const member of PIN.members) {
    const target = path.resolve(root, member.path);
    if (target !== root && !target.startsWith(`${root}${path.sep}`)) throw code("traversal_refused");
    let fd;
    try {
      fd = await open(target, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
    } catch (error) {
      if (error?.code === "ENOENT" || error?.code === "ENOTDIR" || error?.code === "ELOOP") throw code("tampered_source");
      throw error;
    }
    try {
      const info = await fd.stat();
      if (!info.isFile() || info.size !== member.bytes) throw code("tampered_source");
      const body = await fd.readFile();
      if (sha256(body) !== member.sha256) throw code("tampered_source");
    } finally {
      await fd.close();
    }
  }
  const manifest = JSON.parse(await readFile(path.join(root, "package.json"), "utf8"));
  const vendor = JSON.parse(await readFile(path.join(root, PIN.vendor.path, "package.json"), "utf8"));
  const acquisition = JSON.parse(await readFile(path.join(root, "ACQUISITION.json"), "utf8"));
  if (manifest.name !== PIN.package || manifest.version !== PIN.version || manifest.license !== "MIT") {
    throw code("source_disagreement");
  }
  if (vendor.name !== PIN.vendor.packageName || vendor.version !== PIN.vendor.version || vendor.license !== "MIT") {
    throw code("source_disagreement");
  }
  if (acquisition.published !== false || acquisition.version !== PIN.version || acquisition.spdxLicense !== "MIT") {
    throw code("source_disagreement");
  }
  return root;
}

async function assertClosure(caller) {
  const loaded = await import(pathToFileURL(path.join(caller, "src/index.mjs")).href);
  if (typeof loaded.executeCommand !== "function" || typeof loaded.main !== "function") throw code("closure_failed");
}

function classifyDescriptor(bytes) {
  if (bytes.length !== PIN.files.descriptor.bytes || sha256(bytes) !== PIN.files.descriptor.sha256) {
    throw code("tampered_descriptor");
  }
  let parsed;
  try { parsed = JSON.parse(bytes.toString("utf8")); } catch { throw code("tampered_descriptor"); }
  if (parsed.published !== false || parsed.version !== PIN.version || parsed.archiveSha256 !== PIN.files.archive.sha256) {
    throw code("tampered_descriptor");
  }
  if (!Array.isArray(parsed.files) || parsed.files.length !== PIN.members.length) throw code("tampered_descriptor");
  return parsed;
}

export async function acquire(flags) {
  if (!flags.work) {
    return {
      exit: 0,
      body: baseResult({
        outcome: "missing_input",
        nextAction: "Pass --work DIR for a new directory. This command does not extract or run a bundled example.",
      }),
    };
  }
  const root = allowedPublicRoot(flags["public-root"]);
  const work = path.resolve(flags.work);
  try {
    await mkdir(work, { recursive: false, mode: 0o700 });
  } catch (error) {
    if (error?.code === "EEXIST") throw code("overwrite_refused");
    if (error?.code === "ENOENT") throw code("directory_rejected");
    throw error;
  }
  try {
    const real = await realpath(work);
    const parent = await realpath(path.dirname(work));
    if (real !== path.join(parent, path.basename(work))) throw code("traversal_refused");
    const descriptorBytes = await getExact(
      root.origin,
      PIN.files.descriptor.path,
      PIN.files.descriptor.bytes,
      "truncated_descriptor",
    );
    classifyDescriptor(descriptorBytes);
    const archive = await getExact(
      root.origin,
      PIN.files.archive.path,
      PIN.files.archive.bytes,
      "truncated_archive",
    );
    if (sha256(archive) !== PIN.files.archive.sha256) throw code("tampered_archive");
    const caller = path.join(work, PIN.prefix.slice(0, -1));
    extractPinnedArchive(archive, caller);
    await verifyCallerTree(caller);
    await assertClosure(caller);
    return {
      exit: 0,
      body: baseResult({
        outcome: "acquired",
        caller,
        version: PIN.version,
        descriptorPublishedField: false,
        members: PIN.members.length,
        npmInstall: false,
        runtime: process.version,
        receiving: root.receiving,
      }),
    };
  } catch (error) {
    await rm(work, { recursive: true, force: true });
    throw error;
  }
}

function loopbackOrigin(value) {
  let url;
  try { url = new URL(value); } catch { throw code("origin_refused"); }
  const loopback = url.protocol === "http:" && (url.hostname === "127.0.0.1" || url.hostname === "[::1]");
  if (!loopback || !url.port || url.username || url.password || url.search || url.hash || (url.pathname && url.pathname !== "/")) {
    throw code("origin_refused");
  }
  return url.origin;
}

function serviceOrigin(value) {
  let url;
  try { url = new URL(value); } catch { throw code("origin_refused"); }
  const bare = url.username === "" && url.password === "" && !url.search && !url.hash && (url.pathname === "/" || url.pathname === "");
  if (url.origin === PIN.origin && bare) return url.origin;
  return loopbackOrigin(value);
}

function laneFor(flags, origin) {
  const requested = flags.lane;
  if (requested === "autonomous_machine_purchase") throw code("lane_refused");
  if (requested !== undefined && requested !== "agent_assisted_human" && requested !== "disposable_owner_qa") {
    throw code("lane_refused");
  }
  if (origin === PIN.origin) {
    if (requested === "disposable_owner_qa") throw code("lane_refused");
    return "agent_assisted_human";
  }
  if (requested === "agent_assisted_human") throw code("lane_refused");
  return "disposable_owner_qa";
}

async function assertStatePath(file) {
  if (!file || file.includes("\0")) throw code("input_rejected");
  const parent = path.dirname(path.resolve(file));
  let parentInfo;
  try { parentInfo = await lstat(parent); } catch (error) {
    if (error?.code === "ENOENT") throw code("missing_input");
    throw error;
  }
  if (parentInfo.isSymbolicLink() || !parentInfo.isDirectory()) throw code("input_rejected");
  try {
    const info = await lstat(file);
    if (info.isSymbolicLink()) throw code("link_refused");
    if (info.isFIFO()) throw code("fifo_refused");
    if (!info.isFile()) throw code("input_rejected");
  } catch (error) {
    if (error?.code === "ENOENT") return;
    throw error;
  }
}

function textFile(bytes, max) {
  const text = bytes.toString("utf8").replace(/\r?\n$/, "");
  if (text.length < 1 || text.length > max || /[\u0000-\u001f\u007f]/.test(text)) throw code("input_rejected");
  return text;
}

function missing(nextAction) {
  return { exit: 0, body: baseResult({ outcome: "missing_input", nextAction }) };
}

export async function runContinuation(flags, supplied = {}) {
  if (flags.pay || flags.settle || flags.sign || flags.wallet) throw code("payment_refused");
  if (flags.claim || flags.attest || flags.register || flags.file) throw code("action_refused");
  if (!flags.caller || !flags.command || !flags.state || !flags["task-id"] || !flags["customer-key-file"] || !flags["base-url"]) {
    return missing("Pass --caller, --command, --state, --task-id, --customer-key-file, and --base-url. Missing files are not replaced with an example.");
  }
  if (!CLIENT_COMMANDS.has(flags.command)) throw code("flag_rejected");
  const transport = flags.transport ?? "http";
  if (!TRANSPORTS.has(transport)) throw code("flag_rejected");
  if (flags["catalog-transport"] !== undefined && flags["catalog-transport"] !== "http") throw code("flag_rejected");
  if ((transport === "a2a" || transport === "a2a-rest") && flags.command === "discover" && flags["catalog-transport"] !== "http") {
    return missing("A2A discover needs --catalog-transport http. Operations stay on A2A. A stored offer is not the current contract.");
  }
  const origin = serviceOrigin(flags["base-url"]);
  const lane = laneFor(flags, origin);
  if (!TASK_ID.test(flags["task-id"])) throw code("input_rejected");
  const deadline = flags["deadline-ms"] === undefined ? 15_000 : Number(flags["deadline-ms"]);
  if (!Number.isInteger(deadline) || deadline < 50 || deadline > 60_000) throw code("input_rejected");
  await assertStatePath(flags.state);
  const customerKey = textFile(await readRegular(flags["customer-key-file"], 256), 128);
  if (customerKey.length < 12) throw code("input_rejected");
  let contextBytes = null;
  if (flags.command === "assess") {
    if (!flags.context) return missing("Pass --context FILE with ein.supplied-context.v1 or a flat assessment. Task prose is not a business fact.");
    contextBytes = await readRegular(flags.context, CONTEXT_LIMIT);
    try {
      const parsed = JSON.parse(contextBytes.toString("utf8"));
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) throw code("input_rejected");
    } catch (error) {
      if (error?.code === "input_rejected") throw error;
      throw code("input_rejected");
    }
  }
  let email = null;
  if (flags.command === "prepare" || flags["intended-email-file"]) {
    if (flags.command === "prepare" && !flags["intended-email-file"]) {
      return missing("Pass --intended-email-file for the human recipient. This command does not invent one.");
    }
    if (flags["intended-email-file"]) email = textFile(await readRegular(flags["intended-email-file"], 320), 320);
  }
  let grant = null;
  if (flags["grant-file"]) {
    await readRegular(flags["grant-file"], 4096);
    grant = path.resolve(flags["grant-file"]);
    if (!flags["grant-origin"]) return missing("Pass --grant-origin with --grant-file. The grant origin and the continuation file are different facts.");
  }
  const caller = await verifyCallerTree(flags.caller);
  const env = {
    PATH: process.env.PATH || "",
    LANG: "C",
    EIN_ACTIVATION_BASE_URL: origin,
    EIN_CONTINUATION_FILE: path.resolve(flags.state),
    EIN_CONTINUATION_TASK_ID: flags["task-id"],
    EIN_CONTINUATION_CUSTOMER_KEY: customerKey,
    EIN_CONTINUATION_LANE: lane,
    EIN_CONTINUATION_TRANSPORT: transport,
    EIN_CONTINUATION_DEADLINE_MS: String(deadline),
    EIN_CONTINUATION_MAX_RESPONSE_BYTES: "1048576",
  };
  if (email) env.EIN_CONTINUATION_INTENDED_EMAIL = email;
  if (flags.reassess) env.EIN_CONTINUATION_REASSESS = "1";
  if (flags["catalog-transport"]) env.EIN_CONTINUATION_CATALOG_TRANSPORT = "http";
  if (grant) {
    env.EIN_AGENT_GRANT_FILE = grant;
    env.EIN_AGENT_GRANT_ORIGIN = flags["grant-origin"];
  }
  const secrets = [customerKey, email].filter((item) => typeof item === "string" && item.length >= 8);
  if (grant) {
    const token = (await readFile(grant, "utf8")).trim();
    if (token.length >= 8) secrets.push(token);
  }
  const stdout = capture(STDOUT_LIMIT);
  const stderr = capture(STDOUT_LIMIT);
  const { main } = await import(pathToFileURL(path.join(caller, "src/cli.mjs")).href);
  // supplied.fetch is a test seam. It is not a command flag, and it is not a live production result.
  const exitCode = await main(
    [flags.command, ...(flags["show-claim-url"] ? ["--show-claim-url"] : [])],
    {
      env,
      stdin: Readable.from(contextBytes ? [contextBytes] : []),
      stdout,
      stderr,
      fetch: typeof supplied.fetch === "function" ? supplied.fetch : globalThis.fetch,
    },
  );
  const combined = `${stdout.text}${stderr.text}`;
  if (secrets.some((secret) => combined.includes(secret))) throw code("output_withheld");
  if (!flags["show-claim-url"] && /[?&]claim=/.test(combined)) throw code("output_withheld");
  let client = null;
  try { client = JSON.parse(stdout.text); } catch { client = null; }
  return {
    exit: exitCode === 0 ? 0 : exitCode === 2 ? 2 : 1,
    body: baseResult({
      outcome: "client",
      command: flags.command,
      exitCode,
      client,
    }),
  };
}

function capture(limit) {
  let text = "";
  return {
    get text() { return text; },
    write(chunk) {
      const next = Buffer.isBuffer(chunk) ? chunk.toString("utf8") : String(chunk);
      if (Buffer.byteLength(text) + Buffer.byteLength(next) > limit) throw code("output_limit");
      text += next;
      return true;
    },
  };
}

function mapError(error) {
  const name = typeof error?.code === "string" ? error.code : "failed";
  if (name === "missing_input") {
    return { exit: 0, body: baseResult({ outcome: "missing_input", nextAction: "Supply the caller-owned file named by the command." }) };
  }
  if (REFUSALS.has(name)) return { exit: 2, body: baseResult({ outcome: name }) };
  return { exit: 1, body: baseResult({ outcome: "unexpected_failure" }) };
}

async function main() {
  let parsed;
  try { parsed = parseArgs(process.argv.slice(2)); } catch (error) {
    const mapped = mapError(error);
    finish(mapped.exit, mapped.body);
    return;
  }
  if (parsed.flags.pay || parsed.flags.settle || parsed.flags.sign || parsed.flags.wallet) {
    finish(2, baseResult({ outcome: "payment_refused", nextAction: "Payment, signing, and wallet access stay outside this skill." }));
    return;
  }
  if (parsed.flags.claim || parsed.flags.attest || parsed.flags.register || parsed.flags.file) {
    finish(2, baseResult({ outcome: "action_refused", nextAction: "Claim, attestation, registration, and filing stay with the human." }));
    return;
  }
  try {
    const command = parsed.command;
    const result = command === "acquire" ? await acquire(parsed.flags)
      : command === "run" ? await runContinuation(parsed.flags)
        : missing("Run acquire or run. A missing command does not execute a bundled example.");
    finish(result.exit, result.body);
  } catch (error) {
    const mapped = mapError(error);
    finish(mapped.exit, mapped.body);
  }
}

const entry = process.argv[1] ? pathToFileURL(path.resolve(process.argv[1])).href : "";
if (import.meta.url === entry) await main();
