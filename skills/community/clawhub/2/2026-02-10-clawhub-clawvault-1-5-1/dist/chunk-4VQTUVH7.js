import {
  buildEntityIndex
} from "./chunk-J7ZWCI2C.js";

// src/lib/backlinks.ts
import * as fs from "fs";
import * as path from "path";
var CLAWVAULT_DIR = ".clawvault";
var BACKLINKS_FILE = "backlinks.json";
var WIKI_LINK_REGEX = /\[\[([^\]]+)\]\]/g;
function ensureClawvaultDir(vaultPath) {
  const dir = path.join(vaultPath, CLAWVAULT_DIR);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  return dir;
}
function toVaultId(vaultPath, filePath) {
  const relative2 = path.relative(vaultPath, filePath).replace(/\.md$/, "");
  return relative2.split(path.sep).join("/");
}
function normalizeLinkTarget(raw) {
  let target = raw.trim();
  if (!target) return "";
  if (target.startsWith("[[") && target.endsWith("]]")) {
    target = target.slice(2, -2);
  }
  const pipeIndex = target.indexOf("|");
  if (pipeIndex !== -1) {
    target = target.slice(0, pipeIndex);
  }
  if (target.startsWith("#")) return "";
  const hashIndex = target.indexOf("#");
  if (hashIndex !== -1) {
    target = target.slice(0, hashIndex);
  }
  target = target.trim();
  if (!target) return "";
  if (target.endsWith(".md")) {
    target = target.slice(0, -3);
  }
  if (target.startsWith("/")) {
    target = target.slice(1);
  }
  return target.replace(/\\/g, "/");
}
function listMarkdownFiles(vaultPath) {
  const files = [];
  const skipDirs = /* @__PURE__ */ new Set(["archive", "templates", "node_modules"]);
  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (entry.name.startsWith(".") || skipDirs.has(entry.name)) continue;
        walk(fullPath);
      } else if (entry.isFile() && entry.name.endsWith(".md")) {
        files.push(fullPath);
      }
    }
  }
  walk(vaultPath);
  return files;
}
function buildKnownIds(vaultPath, files) {
  const ids = /* @__PURE__ */ new Set();
  const idsLower = /* @__PURE__ */ new Map();
  for (const file of files) {
    const id = toVaultId(vaultPath, file);
    ids.add(id);
    const lower = id.toLowerCase();
    if (!idsLower.has(lower)) {
      idsLower.set(lower, id);
    }
  }
  return { ids, idsLower };
}
function resolveTarget(target, known, entityIndex) {
  if (!target) return null;
  if (known.ids.has(target)) return target;
  const lower = target.toLowerCase();
  if (known.idsLower.has(lower)) return known.idsLower.get(lower);
  if (entityIndex?.entries.has(lower)) return entityIndex.entries.get(lower);
  return null;
}
function scanVaultLinks(vaultPath, options = {}) {
  const files = listMarkdownFiles(vaultPath);
  const known = buildKnownIds(vaultPath, files);
  const entityIndex = options.entityIndex ?? buildEntityIndex(vaultPath);
  const backlinks = /* @__PURE__ */ new Map();
  const orphans = [];
  let linkCount = 0;
  for (const file of files) {
    const sourceId = toVaultId(vaultPath, file);
    const content = fs.readFileSync(file, "utf-8");
    const matches = content.match(WIKI_LINK_REGEX) || [];
    linkCount += matches.length;
    for (const match of matches) {
      const target = normalizeLinkTarget(match);
      if (!target) continue;
      const resolved = resolveTarget(target, known, entityIndex);
      if (!resolved) {
        orphans.push({ source: sourceId, target });
        continue;
      }
      if (!backlinks.has(resolved)) {
        backlinks.set(resolved, /* @__PURE__ */ new Set());
      }
      backlinks.get(resolved).add(sourceId);
    }
  }
  const backlinksMap = /* @__PURE__ */ new Map();
  for (const [target, sources] of backlinks) {
    backlinksMap.set(target, [...sources].sort());
  }
  return { backlinks: backlinksMap, orphans, linkCount };
}
function writeBacklinksIndex(vaultPath, backlinks) {
  const dir = ensureClawvaultDir(vaultPath);
  const output = {};
  const targets = [...backlinks.keys()].sort();
  for (const target of targets) {
    const sources = backlinks.get(target) || [];
    output[target] = [...new Set(sources)].sort();
  }
  fs.writeFileSync(path.join(dir, BACKLINKS_FILE), JSON.stringify(output, null, 2));
}
function readBacklinksIndex(vaultPath) {
  const filePath = path.join(vaultPath, CLAWVAULT_DIR, BACKLINKS_FILE);
  if (!fs.existsSync(filePath)) return null;
  try {
    const raw = JSON.parse(fs.readFileSync(filePath, "utf-8"));
    const map = /* @__PURE__ */ new Map();
    for (const [target, sources] of Object.entries(raw)) {
      if (Array.isArray(sources)) {
        map.set(target, sources);
      }
    }
    return map;
  } catch {
    return null;
  }
}
function rebuildBacklinksIndex(vaultPath, options = {}) {
  const result = scanVaultLinks(vaultPath, options);
  writeBacklinksIndex(vaultPath, result.backlinks);
  return result;
}

export {
  scanVaultLinks,
  readBacklinksIndex,
  rebuildBacklinksIndex
};
