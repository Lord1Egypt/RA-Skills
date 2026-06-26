import { Type } from "@sinclair/typebox";
import { execSync, execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { hexdump, fetchJson } from "./utils.mjs";
import { getConfig } from "./config.mjs";


function parseNpmPackageSpec(spec) {
  const input = String(spec || "").trim();
  if (!input) {
    throw new Error("Empty npm package spec");
  }

  if (input.startsWith("@")) {
    const secondAt = input.indexOf("@", 1);
    if (secondAt === -1) return { name: input, version: null };
    return {
      name: input.slice(0, secondAt),
      version: input.slice(secondAt + 1) || null,
    };
  }

  const lastAt = input.lastIndexOf("@");
  if (lastAt <= 0) return { name: input, version: null };
  return {
    name: input.slice(0, lastAt),
    version: input.slice(lastAt + 1) || null,
  };
}

async function analyzeNpmPackage(packageName) {
  const { name: parsedName, version: requestedVersion } = parseNpmPackageSpec(packageName);
  const npmBase = getConfig().npmRegistryUrl.replace(/\/+$/, "");
  const url = `${npmBase}/${encodeURIComponent(parsedName).replace("%40", "@").replace("%2F", "/")}`;

  let data;
  try {
    data = await fetchJson(url);
  } catch (err) {
    if (err.message.includes("404")) {
      return `## NPM Package Analysis: ${packageName}

**Package does not exist on npm.** This is a strong supply-chain risk indicator — the dependency may be typosquatted, removed, or never published.`;
    }
    throw new Error(`Failed to fetch npm registry for "${packageName}": ${err.message}`);
  }

  const name = data.name || parsedName;
  const description = data.description || "(no description)";
  const license = data.license || "unknown";
  const homepage = data.homepage || null;
  const repoUrl = data.repository?.url || null;
  const keywords = data.keywords || [];
  const maintainers = (data.maintainers || []).map(
    (m) => `${m.name}${m.email ? ` <${m.email}>` : ""}`
  );

  const timeEntries = data.time || {};
  const versionTimes = Object.entries(timeEntries).filter(
    ([k]) => k !== "created" && k !== "modified"
  );
  versionTimes.sort((a, b) => new Date(a[1]) - new Date(b[1]));

  const totalVersions = versionTimes.length;
  const firstVersion = versionTimes[0] || null;
  const latestTag = data["dist-tags"]?.latest || null;
  const latestTime = latestTag && timeEntries[latestTag]
    ? timeEntries[latestTag]
    : versionTimes[versionTimes.length - 1]?.[1] || null;

  const firstPublishDate = firstVersion ? new Date(firstVersion[1]) : null;
  const now = new Date();
  const threeMonthsAgo = new Date(now);
  threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
  const isNewPackage = firstPublishDate && firstPublishDate > threeMonthsAgo;

  const selectedVersion = requestedVersion || latestTag;
  const selectedVersionData = selectedVersion && data.versions?.[selectedVersion];
  const selectedVersionTime = selectedVersion && timeEntries[selectedVersion]
    ? timeEntries[selectedVersion]
    : null;
  const dependencies = selectedVersionData?.dependencies
    ? Object.keys(selectedVersionData.dependencies)
    : [];
  const devDependencies = selectedVersionData?.devDependencies
    ? Object.keys(selectedVersionData.devDependencies)
    : [];
  const scripts = selectedVersionData?.scripts || {};
  const hasLifecycleScripts = ["preinstall", "install", "postinstall", "preuninstall", "postuninstall"].some(
    (s) => s in scripts
  );

  const lines = [];
  lines.push(`## NPM Package Analysis: ${name}`);
  lines.push("");
  if (requestedVersion) {
    lines.push(`- **Requested version**: ${requestedVersion}`);
    lines.push(`- **Requested version exists**: ${selectedVersionData ? "yes" : "no"}`);
    if (selectedVersionTime) {
      lines.push(`- **Requested version publish time**: ${selectedVersionTime}`);
    }
    lines.push("");
  }

  if (isNewPackage) {
    lines.push(`⚠️  **WARNING: This package was first published less than 3 months ago (${firstVersion[1]}). This is a supply-chain risk indicator.**`);
    lines.push("");
  }

  lines.push(`- **Description**: ${description}`);
  lines.push(`- **License**: ${license}`);
  lines.push(`- **Total versions published**: ${totalVersions}`);
  lines.push(`- **First version**: ${firstVersion ? `${firstVersion[0]} (${firstVersion[1]})` : "unknown"}`);
  lines.push(`- **Latest version**: ${latestTag || "unknown"} (${latestTime || "unknown"})`);
  if (requestedVersion && !selectedVersionData) {
    lines.push(`- **Version check**: requested version was not found in the npm registry metadata`);
  }
  lines.push(`- **Repository**: ${repoUrl || "not specified"}`);
  if (homepage) lines.push(`- **Homepage**: ${homepage}`);
  lines.push(`- **Maintainers**: ${maintainers.length ? maintainers.join(", ") : "none listed"}`);
  if (keywords.length) lines.push(`- **Keywords**: ${keywords.join(", ")}`);

  lines.push("");
  lines.push(`### Dependencies (${requestedVersion ? `requested version ${requestedVersion}` : "latest version"})`);
  lines.push(`- **Runtime dependencies** (${dependencies.length}): ${dependencies.length ? dependencies.join(", ") : "none"}`);
  lines.push(`- **Dev dependencies** (${devDependencies.length}): ${devDependencies.length ? devDependencies.join(", ") : "none"}`);

  if (hasLifecycleScripts) {
    const lifecycleEntries = ["preinstall", "install", "postinstall", "preuninstall", "postuninstall"]
      .filter((s) => s in scripts)
      .map((s) => `  - ${s}: \`${scripts[s]}\``);
    lines.push("");
    lines.push(`### ⚠️  Lifecycle Scripts Detected`);
    lines.push(...lifecycleEntries);
  }

  if (Object.keys(scripts).length) {
    lines.push("");
    lines.push(`### Package Scripts`);
    for (const [k, v] of Object.entries(scripts)) {
      lines.push(`- ${k}: \`${v}\``);
    }
  }

  if (totalVersions >= 2) {
    const firstDate = new Date(versionTimes[0][1]);
    const lastDate = new Date(versionTimes[versionTimes.length - 1][1]);
    const spanDays = Math.max(1, (lastDate - firstDate) / (1000 * 60 * 60 * 24));
    const avgDaysPerRelease = (spanDays / (totalVersions - 1)).toFixed(1);
    lines.push("");
    lines.push(`### Publish Frequency`);
    lines.push(`- Active period: ${Math.round(spanDays)} days`);
    lines.push(`- Average: one release every ${avgDaysPerRelease} days`);
  }

  return lines.join("\n");
}

async function analyzePypiPackage(packageName) {
  const pkg = packageName;
  const pypiBase = getConfig().pypiIndexUrl.replace(/\/+$/, "");
  const url = `${pypiBase}/pypi/${encodeURIComponent(pkg)}/json`;

  let data;
  try {
    data = await fetchJson(url);
  } catch (err) {
    if (err.message.includes("404")) {
      return `## PyPI Package Analysis: ${pkg}\n\n**Package does not exist on PyPI.** This is a strong supply-chain risk indicator — the dependency may be typosquatted, removed, or never published.`;
    }
    throw new Error(`Failed to fetch PyPI registry for "${pkg}": ${err.message}`);
  }

  const info = data.info || {};
  const releases = data.releases || {};
  const ownership = data.ownership || {};
  const vulnerabilities = data.vulnerabilities || [];

  const name = info.name || pkg;
  const summary = info.summary || "(no summary)";
  const license = info.license || "unknown";
  const requiresPython = info.requires_python || "not specified";
  const authorEmail = info.author_email || info.author || "unknown";
  const projectUrls = info.project_urls || {};
  const repoUrl = projectUrls.Source || projectUrls.Homepage || projectUrls.Repository || null;
  const homepage = projectUrls.Homepage || projectUrls.Documentation || info.home_page || null;
  const classifiers = info.classifiers || [];

  const maintainers = (ownership.roles || []).map(
    (r) => `${r.user} (${r.role})`
  );

  const totalVersions = Object.keys(releases).length;
  const versionDates = [];
  for (const [ver, files] of Object.entries(releases)) {
    if (files.length > 0) {
      const earliest = files.reduce((min, f) => {
        const t = f.upload_time_iso_8601 || f.upload_time;
        return t && t < min ? t : min;
      }, files[0].upload_time_iso_8601 || files[0].upload_time);
      if (earliest) versionDates.push([ver, earliest]);
    }
  }
  versionDates.sort((a, b) => new Date(a[1]) - new Date(b[1]));

  const firstVersion = versionDates[0] || null;
  const latestVersionStr = info.version || null;
  const latestTime = latestVersionStr && releases[latestVersionStr]?.length
    ? (releases[latestVersionStr][0].upload_time_iso_8601 || releases[latestVersionStr][0].upload_time)
    : versionDates[versionDates.length - 1]?.[1] || null;

  const firstPublishDate = firstVersion ? new Date(firstVersion[1]) : null;
  const now = new Date();
  const threeMonthsAgo = new Date(now);
  threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
  const isNewPackage = firstPublishDate && firstPublishDate > threeMonthsAgo;

  const requiresDist = info.requires_dist || [];
  const coreDeps = requiresDist
    .filter((d) => !d.includes("extra =="))
    .map((d) => d.split(";")[0].trim());
  const optionalDeps = requiresDist.filter((d) => d.includes("extra =="));

  const yankedVersions = [];
  for (const [ver, files] of Object.entries(releases)) {
    if (files.some((f) => f.yanked)) {
      const reason = files.find((f) => f.yanked_reason)?.yanked_reason || "";
      yankedVersions.push(reason ? `${ver} (${reason})` : ver);
    }
  }

  const lines = [];
  lines.push(`## PyPI Package Analysis: ${name}`);
  lines.push("");

  if (isNewPackage) {
    lines.push(`⚠️  **WARNING: This package was first published less than 3 months ago (${firstVersion[1]}). This is a supply-chain risk indicator.**`);
    lines.push("");
  }

  if (vulnerabilities.length > 0) {
    lines.push(`⚠️  **WARNING: ${vulnerabilities.length} known vulnerabilities reported by PyPI.**`);
    for (const v of vulnerabilities) {
      const id = v.id || v.aliases?.[0] || "unknown";
      const detail = v.summary || v.details || "";
      lines.push(`  - ${id}: ${detail.substring(0, 200)}`);
    }
    lines.push("");
  }

  lines.push(`- **Summary**: ${summary}`);
  lines.push(`- **License**: ${license}`);
  lines.push(`- **Requires Python**: ${requiresPython}`);
  lines.push(`- **Total releases**: ${totalVersions}`);
  lines.push(`- **First version**: ${firstVersion ? `${firstVersion[0]} (${firstVersion[1]})` : "unknown"}`);
  lines.push(`- **Latest version**: ${latestVersionStr || "unknown"} (${latestTime || "unknown"})`);
  lines.push(`- **Repository**: ${repoUrl || "not specified"}`);
  if (homepage && homepage !== repoUrl) lines.push(`- **Homepage**: ${homepage}`);
  lines.push(`- **Author**: ${authorEmail}`);
  lines.push(`- **Maintainers**: ${maintainers.length ? maintainers.join(", ") : "none listed"}`);

  const devStatus = classifiers.find((c) => c.startsWith("Development Status"));
  if (devStatus) lines.push(`- **Development Status**: ${devStatus.split("::").pop().trim()}`);

  lines.push("");
  lines.push(`### Dependencies`);
  lines.push(`- **Core dependencies** (${coreDeps.length}): ${coreDeps.length ? coreDeps.join(", ") : "none"}`);
  if (optionalDeps.length) {
    lines.push(`- **Optional/extra dependencies** (${optionalDeps.length}): ${optionalDeps.map((d) => d.split(";")[0].trim()).join(", ")}`);
  }
  if (info.provides_extra?.length) {
    lines.push(`- **Extras**: ${info.provides_extra.join(", ")}`);
  }

  if (yankedVersions.length) {
    lines.push("");
    lines.push(`### ⚠️  Yanked Versions (${yankedVersions.length})`);
    lines.push(yankedVersions.join(", "));
  }

  if (versionDates.length >= 2) {
    const firstDate = new Date(versionDates[0][1]);
    const lastDate = new Date(versionDates[versionDates.length - 1][1]);
    const spanDays = Math.max(1, (lastDate - firstDate) / (1000 * 60 * 60 * 24));
    const avgDaysPerRelease = (spanDays / (versionDates.length - 1)).toFixed(1);
    lines.push("");
    lines.push(`### Publish Frequency`);
    lines.push(`- Active period: ${Math.round(spanDays)} days`);
    lines.push(`- Average: one release every ${avgDaysPerRelease} days`);
  }

  return lines.join("\n");
}

async function analyzeUrl(targetUrl) {
  try {
    const res = await fetch(targetUrl, {
      redirect: "follow",
      signal: AbortSignal.timeout(10_000),
    });
    const body = Buffer.from(await res.arrayBuffer());
    const redirected = res.redirected;
    const finalUrl = res.url;

    const lines = [];
    lines.push(`## URL Analysis: ${targetUrl}`);
    lines.push("");
    if (redirected) {
      lines.push(`- **Redirected**: yes`);
      lines.push(`- **Final URL**: ${finalUrl}`);
    }
    lines.push(`- **Status**: ${res.status} ${res.statusText}`);
    lines.push(`- **Content-Type**: ${res.headers.get("content-type") || "unknown"}`);
    lines.push(`- **Content-Length**: ${res.headers.get("content-length") || "not specified"}`);
    lines.push(`- **Actual Size**: ${body.length} bytes`);
    lines.push(`- **Server**: ${res.headers.get("server") || "unknown"}`);

    const ct = res.headers.get("content-type") || "";
    if (ct.includes("text") || ct.includes("json") || ct.includes("javascript")) {
      const preview = body.toString("utf-8").substring(0, 500);
      lines.push("");
      lines.push(`### Content Preview`);
      lines.push("```");
      lines.push(preview);
      lines.push("```");
    }

    return lines.join("\n");
  } catch (err) {
    const isTimeout = err.name === "TimeoutError" || err.code === "ABORT_ERR";
    const statusText = isTimeout ? "timeout (10s)" : "unreachable";
    return `## URL Analysis: ${targetUrl}\n\n- **Status**: ${statusText}\n- **Error**: ${err.message}`;
  }
}

const BINARY_HEAD_BYTES = 0x100;
const BINARY_SCAN_CHUNK_BYTES = 64 * 1024;
const URL_SCAN_TAIL_CHARS = 4096;
const MAX_EMBEDDED_URLS = 20;
const EMBEDDED_URL_RE = /\b(?:https?|wss?|ftp):\/\/[A-Za-z0-9\-._~:\/?#\[\]@!$&'()*+,;=%]+/gi;

function readFileHead(absPath, maxBytes) {
  const fd = fs.openSync(absPath, "r");
  try {
    const buf = Buffer.alloc(maxBytes);
    const bytesRead = fs.readSync(fd, buf, 0, maxBytes, 0);
    return buf.subarray(0, bytesRead);
  } finally {
    fs.closeSync(fd);
  }
}

function formatPercent(count, total) {
  if (!total) return "0.00%";
  return `${((count / total) * 100).toFixed(2)}%`;
}

function describeEntropy(entropy) {
  if (entropy >= 7.5) return "high; packed, encrypted, or compressed data often looks like this";
  if (entropy >= 6.0) return "moderate-high";
  if (entropy >= 3.0) return "moderate";
  return "low";
}

function addEmbeddedUrlsFromText(text, state) {
  EMBEDDED_URL_RE.lastIndex = 0;
  let match;
  while ((match = EMBEDDED_URL_RE.exec(text)) !== null) {
    const url = match[0].replace(/[)\]}>"'`.,;]+$/g, "");
    if (!url || state.seen.has(url)) continue;

    state.seen.add(url);
    if (state.urls.length < MAX_EMBEDDED_URLS) {
      state.urls.push(url);
    } else {
      state.truncated = true;
    }
  }
}

function scanBinaryBytes(absPath) {
  const counts = new Array(256).fill(0);
  const urlState = { urls: [], seen: new Set(), truncated: false };
  const chunk = Buffer.alloc(BINARY_SCAN_CHUNK_BYTES);
  let asciiTail = "";
  let totalBytes = 0;
  let nulBytes = 0;
  let printableAsciiBytes = 0;
  let highBitBytes = 0;

  const fd = fs.openSync(absPath, "r");
  try {
    let position = 0;
    while (true) {
      const bytesRead = fs.readSync(fd, chunk, 0, chunk.length, position);
      if (bytesRead <= 0) break;

      const slice = chunk.subarray(0, bytesRead);
      for (let i = 0; i < bytesRead; i++) {
        const b = slice[i];
        counts[b] += 1;
        if (b === 0) nulBytes += 1;
        if (b >= 0x20 && b <= 0x7e) printableAsciiBytes += 1;
        if (b >= 0x80) highBitBytes += 1;
      }

      totalBytes += bytesRead;
      const text = asciiTail + slice.toString("latin1");
      addEmbeddedUrlsFromText(text, urlState);
      asciiTail = text.slice(-URL_SCAN_TAIL_CHARS);
      position += bytesRead;
    }
  } finally {
    fs.closeSync(fd);
  }

  let entropy = 0;
  if (totalBytes > 0) {
    for (const count of counts) {
      if (!count) continue;
      const p = count / totalBytes;
      entropy -= p * Math.log2(p);
    }
  }

  return {
    totalBytes,
    entropy,
    uniqueByteValues: counts.filter(Boolean).length,
    nulBytes,
    printableAsciiBytes,
    highBitBytes,
    urls: urlState.urls,
    urlsTruncated: urlState.truncated,
  };
}

// Keep binary analysis limited to static metadata. Never execute, import,
// deserialize, or otherwise load the target artifact.
function analyzeBinary(cwd, filePath) {
  const absPath = path.resolve(cwd, filePath);
  const lines = [];
  lines.push(`## Binary Analysis: ${filePath}`);
  lines.push("");

  try {
    const stat = fs.statSync(absPath);
    lines.push(`- **Size**: ${stat.size} bytes`);

    try {
      const fileType = execFileSync("file", ["-b", absPath], { encoding: "utf-8", timeout: 5_000 }).trim();
      lines.push(`- **Type**: ${fileType}`);
    } catch {
      lines.push(`- **Type**: unknown`);
    }

    const head = readFileHead(absPath, Math.min(BINARY_HEAD_BYTES, stat.size));
    const stats = scanBinaryBytes(absPath);

    lines.push("");
    lines.push(`### Header Hexdump (first ${head.length} bytes)`);
    lines.push("```");
    lines.push(...hexdump(head));
    lines.push("```");

    lines.push("");
    lines.push(`### Embedded URLs`);
    if (stats.urls.length > 0) {
      for (const url of stats.urls) lines.push(`- ${url}`);
      if (stats.urlsTruncated) lines.push(`- ... more URLs omitted`);
    } else {
      lines.push(`- none found`);
    }

    lines.push("");
    lines.push(`### Byte Statistics (whole file)`);
    lines.push(`- **Entropy**: ${stats.entropy.toFixed(3)} / 8 bits per byte (${describeEntropy(stats.entropy)})`);
    lines.push(`- **Unique byte values**: ${stats.uniqueByteValues}/256`);
    lines.push(`- **NUL bytes**: ${stats.nulBytes} (${formatPercent(stats.nulBytes, stats.totalBytes)})`);
    lines.push(`- **Printable ASCII bytes**: ${stats.printableAsciiBytes} (${formatPercent(stats.printableAsciiBytes, stats.totalBytes)})`);
    lines.push(`- **High-bit bytes (>= 0x80)**: ${stats.highBitBytes} (${formatPercent(stats.highBitBytes, stats.totalBytes)})`);

    lines.push("");
    lines.push("> Review guidance: This is static metadata-only analysis. Treat executable, bytecode, serialized, or otherwise loadable binary artifacts as opaque unless surrounding source code clearly explains and safely constrains their use. A benign-looking header, no embedded URLs, or ordinary entropy is not proof of safety; if the skill loads, imports, executes, deserializes, or otherwise consumes this file at runtime, evaluate that path conservatively.");

    return lines.join("\n");
  } catch (err) {
    lines.push(`- **Error**: ${err.message}`);
    return lines.join("\n");
  }
}

export function makeDeepAnalysisTool(cwd) {
  return {
    name: "deepAnalysis",
    label: "Deep Analysis",
    description:
      "Run deeper analysis for dependency, executable/loadable binary, and external-resource findings. " +
      "Accepts (type, data), where type is one of binary/url/pypi/npm, and routes to the corresponding internal analyzer. " +
      "For type=url, only analyze runtime-relevant or security-relevant URLs that the target skill would realistically fetch, follow, or use at runtime; skip placeholder, sample, and documentation-only URLs unless the skill explicitly treats them as real runtime inputs. " +
      "For type=binary, return static metadata only: file type, header hexdump, embedded URLs, and entropy/byte statistics; absence of suspicious indicators is not proof of safety. " +
      "Always returns a plain string summary.",
    parameters: Type.Object({
      type: Type.Union([
        Type.Literal("binary"),
        Type.Literal("url"),
        Type.Literal("pypi"),
        Type.Literal("npm"),
      ], { description: "Analysis type routing key." }),
      data: Type.String({ description: "Input payload for analysis. For binary use relative file path, for url use the URL, for pypi/npm use the package name." }),
    }),
    execute: async (_toolCallId, params) => {
      const { type, data } = params;
      switch (type) {
        case "npm":
          return { content: [{ type: "text", text: await analyzeNpmPackage(data) }] };
        case "pypi":
          return { content: [{ type: "text", text: await analyzePypiPackage(data) }] };
        case "url":
          return { content: [{ type: "text", text: await analyzeUrl(data) }] };
        case "binary":
          return { content: [{ type: "text", text: analyzeBinary(cwd, data) }] };
        default:
          throw new Error(`Unsupported deep analysis type: ${type}`);
      }
    },
  };
}


export function makeBashTool(cwd) {
  return {
    name: "bash",
    label: "Bash",
    description:
      "Execute a shell command and return stdout/stderr. " +
      "Use this to explore the filesystem, read files, etc. " +
      "IMPORTANT: All commands run inside the skill directory. " +
      "Do NOT run commands that modify files or install anything. " +
      "NEVER execute, run, or invoke any target files — no python/node/bash scripts, " +
      "no binary execution, no deserialization (pickle.load, yaml.load, eval, etc.). " +
      "Only use safe read-only commands: cat, head, tail, hexdump, xxd, file, strings, grep, find, ls, wc.",
    parameters: Type.Object({
      command: Type.String({ description: "The shell command to execute" }),
    }),
    execute: async (_toolCallId, params) => {
      const rawCommand = String(params.command || "");
      const command = rawCommand
        .replace(/<\/?tool_call>/gi, " ")
        .replace(/<\/?function_call>/gi, " ")
        .replace(/<\/?tool>/gi, " ")
        .replace(/<\/?function>/gi, " ")
        .replace(/[{}]+$/g, "")
        .trim();

      if (!command) {
        throw new Error("Command failed: empty command after sanitization");
      }

      try {
        const stdout = execSync(command, {
          encoding: "utf-8",
          timeout: 30_000,
          maxBuffer: 1024 * 1024,
          cwd,
        });
        return {
          content: [{ type: "text", text: stdout || "(no output)" }],
          details: { command, rawCommand },
        };
      } catch (err) {
        const msg = err.stderr || err.stdout || err.message;
        throw new Error(`Command failed: ${msg}`);
      }
    },
  };
}
