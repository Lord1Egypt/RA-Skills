import fs from "fs";
import path from "path";
import process from "process";
import { execFileSync } from "child_process";
import { fileURLToPath } from "url";
import http from "http";
import https from "https";

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const cacheRoot = path.join(skillRoot, ".cache", "payment-skill-contexts");
const downloadCacheRoot = path.join(skillRoot, ".cache", "payment-skill-downloads");
const extractCacheRoot = path.join(skillRoot, ".cache", "payment-skill-extracts");

const dependencies = [
  {
    id: "agentic-payment-skills",
    label: "agentic-payment-skills",
    aliases: ["agent-payment-skills"],
    expectedSkillName: "clink-payment-skill",
    urlEnv: "CLINK_AGENTIC_PAYMENT_SKILLS_URL",
    urlEnvAliases: ["CLINK_AGENT_PAYMENT_SKILLS_URL"],
    pathEnv: "CLINK_AGENTIC_PAYMENT_SKILLS_PATH",
    pathEnvAliases: ["CLINK_AGENT_PAYMENT_SKILLS_PATH"],
    defaultUrl: "https://codeload.github.com/clinkbillcom/agentic-payment-skills/zip/refs/heads/main",
    alternateUrls: [
      "https://codeload.github.com/clinkbillcom/agentic-payment-skill/zip/refs/heads/main",
      "https://codeload.github.com/clinkbillcom/agent-payment-skills/zip/refs/heads/main",
      "https://codeload.github.com/clinkbillcom/agent-payment-skill/zip/refs/heads/main",
    ],
    localFallbackPath: path.resolve(skillRoot, "..", "agentic-payment-skills"),
    localFallbackPaths: [path.resolve(skillRoot, "..", "agent-payment-skills")],
    files: ["SKILL.md", "README.md", "package.json"],
  },
  {
    id: "openclaw-payment-skills",
    label: "openclaw-payment-skills",
    expectedSkillName: "openclaw-payment-skills",
    urlEnv: "CLINK_OPENCLAW_PAYMENT_SKILLS_URL",
    pathEnv: "CLINK_OPENCLAW_PAYMENT_SKILLS_PATH",
    defaultUrl: "https://codeload.github.com/clinkbillcom/openclaw-payment-skills/zip/refs/heads/main",
    alternateUrls: ["https://codeload.github.com/clinkbillcom/openclaw-payment-skill/zip/refs/heads/main"],
    localFallbackPath: path.resolve(skillRoot, "..", "openclaw-payment-skills"),
    files: ["SKILL.md", "README.md", "package.json"],
  },
];

function parseArgs(argv) {
  const values = argv.slice(2);
  const args = new Set(values);
  const dependencies = [];

  for (let index = 0; index < values.length; index += 1) {
    if (values[index] === "--dependency") {
      const value = values[index + 1];
      if (!value) throw new Error("--dependency requires a value");
      dependencies.push(value);
      index += 1;
    }
  }

  return {
    json: args.has("--json"),
    printPath: args.has("--print-path"),
    statusOnly: args.has("--status"),
    force: args.has("--force"),
    dependencies,
  };
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function runCommand(command, args, options = {}) {
  return execFileSync(command, args, {
    cwd: options.cwd || skillRoot,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  }).trim();
}

function tryCommand(command, args, options = {}) {
  try {
    return { ok: true, stdout: runCommand(command, args, options), error: null };
  } catch (error) {
    return {
      ok: false,
      stdout: "",
      error: error.stderr?.toString?.().trim() || error.message,
    };
  }
}

function tryGit(args, options = {}) {
  return tryCommand("git", args, options);
}

function readMaybe(filePath) {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch {
    return null;
  }
}

function parseSkillName(contents) {
  const frontmatter = contents.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatter) return null;
  const name = frontmatter[1].match(/^name:\s*["']?([^"'\n]+)["']?\s*$/m);
  return name ? name[1].trim() : null;
}

function readFilesFromWorkingTree(repoDir, files) {
  const loaded = {};
  for (const file of files) {
    const contents = readMaybe(path.join(repoDir, file));
    if (contents !== null) loaded[file] = contents;
  }
  return loaded;
}

function assertExpectedSkill(dep, files, sourceLabel) {
  const skill = files["SKILL.md"];
  if (!skill) throw new Error(`${sourceLabel} did not provide SKILL.md`);
  const actual = parseSkillName(skill);
  if (actual !== dep.expectedSkillName) {
    throw new Error(`${sourceLabel} SKILL.md name is ${actual || "missing"}, expected ${dep.expectedSkillName}`);
  }
}

function candidateUrls(dep) {
  if (process.env[dep.urlEnv]) return [process.env[dep.urlEnv]];
  for (const envName of dep.urlEnvAliases || []) {
    if (process.env[envName]) return [process.env[envName]];
  }
  return [dep.defaultUrl, ...(dep.alternateUrls || [])];
}

function selectedDependencies(args) {
  if (!args.dependencies.length) return dependencies;

  const selected = [];
  for (const value of args.dependencies) {
    const dep = dependencies.find(
      (item) => item.id === value || item.label === value || (item.aliases || []).includes(value)
    );
    if (!dep) {
      throw new Error(`Unknown payment skill dependency: ${value}`);
    }
    selected.push(dep);
  }
  return selected;
}

function requestUrl(urlString, redirects = 0) {
  return new Promise((resolve, reject) => {
    const client = urlString.startsWith("https://") ? https : http;
    const request = client.get(urlString, (response) => {
      if (
        response.statusCode &&
        response.statusCode >= 300 &&
        response.statusCode < 400 &&
        response.headers.location
      ) {
        response.resume();
        if (redirects >= 5) {
          reject(new Error(`Too many redirects while downloading ${urlString}`));
          return;
        }
        resolve(requestUrl(new URL(response.headers.location, urlString).toString(), redirects + 1));
        return;
      }

      if (response.statusCode !== 200) {
        response.resume();
        reject(new Error(`Download failed for ${urlString}: HTTP ${response.statusCode}`));
        return;
      }

      const chunks = [];
      response.on("data", (chunk) => chunks.push(chunk));
      response.on("end", () => resolve(Buffer.concat(chunks)));
    });

    request.setTimeout(30000, () => {
      request.destroy(new Error(`Download timed out for ${urlString}`));
    });

    request.on("error", reject);
  });
}

async function downloadZip(url, targetPath) {
  ensureDir(path.dirname(targetPath));
  const body = await requestUrl(url);
  fs.writeFileSync(targetPath, body);
}

function extractZip(dep, zipPath, args) {
  const extractDir = path.join(extractCacheRoot, dep.id);

  if (fs.existsSync(extractDir)) {
    fs.rmSync(extractDir, { recursive: true, force: true });
  }

  ensureDir(extractDir);
  runCommand("unzip", ["-q", "-o", zipPath, "-d", extractDir]);

  const entries = fs.readdirSync(extractDir, { withFileTypes: true });
  const topLevel = entries.find((entry) => entry.isDirectory());
  return topLevel ? path.join(extractDir, topLevel.name) : extractDir;
}

async function loadFromZipDownload(dep, args) {
  const errors = [];

  for (const url of candidateUrls(dep)) {
    try {
      const zipPath = path.join(downloadCacheRoot, `${dep.id}.zip`);
      await downloadZip(url, zipPath);
      const extractedPath = extractZip(dep, zipPath, args);
      const files = readFilesFromWorkingTree(extractedPath, dep.files);
      assertExpectedSkill(dep, files, `${dep.id} zip download`);
      return {
        id: dep.id,
        label: dep.label,
        source: "zip-download",
        repoUrl: url,
        repoPath: extractedPath,
        ref: "refs/heads/main",
        commit: null,
        dirty: false,
        latest: true,
        warning: null,
        remoteErrors: errors,
        files,
      };
    } catch (error) {
      errors.push({
        repoUrl: url,
        error: error instanceof Error ? error.message : String(error),
      });
    }
  }

  const detail = errors.map((item) => `${item.repoUrl}: ${item.error}`).join("; ");
  const aggregate = new Error(detail || `${dep.id} zip download failed`);
  aggregate.remoteErrors = errors;
  throw aggregate;
}

function loadFromLocalFallback(dep) {
  const envPath = process.env[dep.pathEnv] || (dep.pathEnvAliases || []).map((item) => process.env[item]).find(Boolean);
  const fallbackPaths = [dep.localFallbackPath, ...(dep.localFallbackPaths || [])];
  const repoPath = envPath || fallbackPaths.find((item) => fs.existsSync(item)) || dep.localFallbackPath;
  if (!fs.existsSync(repoPath)) {
    throw new Error(`${dep.id} local fallback not found at ${repoPath}`);
  }

  const files = readFilesFromWorkingTree(repoPath, dep.files);
  assertExpectedSkill(dep, files, `${dep.id} local fallback`);

  const commit = tryGit(["rev-parse", "HEAD"], { cwd: repoPath });
  const status = tryGit(["status", "--short"], { cwd: repoPath });

  return {
    id: dep.id,
    label: dep.label,
    source: "local-fallback",
    repoUrl: null,
    repoPath,
    ref: "working-tree",
    commit: commit.ok ? commit.stdout : null,
    dirty: status.ok ? status.stdout.length > 0 : null,
    latest: false,
    warning: "Zip download failed; using local fallback. Treat exact payment-skill behavior as best-effort until zip download succeeds.",
    files,
  };
}

function writeContext(result) {
  const targetDir = path.join(cacheRoot, result.id);
  ensureDir(targetDir);

  for (const [file, contents] of Object.entries(result.files)) {
    fs.writeFileSync(path.join(targetDir, file), contents, "utf8");
  }

  const metadata = {
    id: result.id,
    label: result.label,
    source: result.source,
    repoUrl: result.repoUrl,
    repoPath: result.repoPath,
    ref: result.ref,
    commit: result.commit,
    dirty: result.dirty,
    latest: result.latest,
    warning: result.warning,
    remoteErrors: result.remoteErrors || [],
    loadedAt: new Date().toISOString(),
    files: Object.keys(result.files),
  };

  fs.writeFileSync(path.join(cacheRoot, `${result.id}.meta.json`), JSON.stringify(metadata, null, 2), "utf8");
  return metadata;
}

function contextPathForResults(results) {
  if (results.length === 1) {
    const fileNameByDependency = {
      "agentic-payment-skills": "agentic-payment-skills.md",
      "openclaw-payment-skills": "openclaw-payment-skills.md",
    };
    return path.join(cacheRoot, fileNameByDependency[results[0].id] || `${results[0].id}.md`);
  }
  return path.join(cacheRoot, "combined.md");
}

function buildContextFile(results) {
  ensureDir(cacheRoot);
  const lines = [
    "# Payment Skill Contexts",
    "",
    `Generated at: ${new Date().toISOString()}`,
    "",
    "Read this file before generating or reviewing merchant skill code that integrates with agentic-payment-skills or openclaw-payment-skills.",
    "",
  ];

  for (const result of results) {
    lines.push(`## ${result.label}`, "");
    lines.push(`- source: ${result.source}`);
    if (result.repoUrl) lines.push(`- repoUrl: ${result.repoUrl}`);
    lines.push(`- repoPath: ${result.repoPath}`);
    lines.push(`- ref: ${result.ref}`);
    lines.push(`- commit: ${result.commit || "unknown"}`);
    lines.push(`- latestRemoteContext: ${result.latest ? "true" : "false"}`);
    if (result.warning) lines.push(`- warning: ${result.warning}`);
    lines.push("");

    for (const [file, contents] of Object.entries(result.files)) {
      lines.push(`### ${result.label}/${file}`, "");
      lines.push("```markdown");
      lines.push(contents.trimEnd());
      lines.push("```", "");
    }
  }

  const contextPath = contextPathForResults(results);
  fs.writeFileSync(contextPath, `${lines.join("\n")}\n`, "utf8");
  return contextPath;
}

function getStatus(items = dependencies) {
  return items.map((dep) => {
    const metaPath = path.join(cacheRoot, `${dep.id}.meta.json`);
    const meta = readMaybe(metaPath);
    return {
      id: dep.id,
      cachePath: path.join(cacheRoot, dep.id),
      metaPath,
      exists: Boolean(meta),
      meta: meta ? JSON.parse(meta) : null,
    };
  });
}

async function main() {
  const args = parseArgs(process.argv);
  const selected = selectedDependencies(args);

  if (args.statusOnly) {
    const payload = {
      cacheRoot,
      contextPath: path.join(cacheRoot, selected.length === 1 ? `${selected[0].id}.md` : "combined.md"),
      dependencies: getStatus(selected),
    };
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  const results = [];
  for (const dep of selected) {
    try {
      results.push(await loadFromZipDownload(dep, args));
    } catch (remoteError) {
      try {
        const fallback = loadFromLocalFallback(dep);
        fallback.remoteErrors = remoteError.remoteErrors || [
          { repoUrl: null, error: remoteError instanceof Error ? remoteError.message : String(remoteError) },
        ];
        results.push(fallback);
      } catch (fallbackError) {
        throw new Error(
          `${dep.id} context load failed. Remote error: ${
            remoteError instanceof Error ? remoteError.message : String(remoteError)
          }. Fallback error: ${fallbackError instanceof Error ? fallbackError.message : String(fallbackError)}`
        );
      }
    }
  }

  const metadata = results.map(writeContext);
  const contextPath = buildContextFile(results);

  if (args.printPath) {
    console.log(contextPath);
    return;
  }

  const payload = { cacheRoot, contextPath, dependencies: metadata };
  if (args.json) {
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  console.log(`Payment skill context path: ${contextPath}`);
  for (const item of metadata) {
    console.log(`${item.label}: ${item.source} ${item.commit || "unknown"}${item.warning ? ` (${item.warning})` : ""}`);
  }
  console.log("");
  console.log(fs.readFileSync(contextPath, "utf8"));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
