import {
  autoLink,
  dryRunLink,
  findUnlinkedMentions
} from "../chunk-42MXU7A6.js";
import {
  readBacklinksIndex,
  rebuildBacklinksIndex,
  scanVaultLinks
} from "../chunk-4VQTUVH7.js";
import {
  getVaultPath
} from "../chunk-4KDZZW4X.js";
import {
  buildEntityIndex
} from "../chunk-J7ZWCI2C.js";

// src/commands/link.ts
import * as fs from "fs";
import * as path from "path";
async function linkCommand(file, options) {
  const vaultPath = getVaultPath();
  const index = buildEntityIndex(vaultPath);
  const suggestionIndex = filterIndex(index, /* @__PURE__ */ new Set(["people", "projects", "decisions"]));
  const modeCount = [options.backlinks ? 1 : 0, options.orphans ? 1 : 0, options.rebuild ? 1 : 0].reduce((sum, value) => sum + value, 0);
  if (modeCount > 1) {
    console.error("Error: Use only one of --backlinks, --orphans, or --rebuild");
    process.exit(1);
  }
  if (options.rebuild) {
    const result = rebuildBacklinksIndex(vaultPath, { entityIndex: index });
    const orphanSuffix = result.orphans.length > 0 ? `, ${result.orphans.length} orphan(s)` : "";
    console.log(`\u2713 Rebuilt backlinks (${result.backlinks.size} targets, ${result.linkCount} links${orphanSuffix})`);
    return;
  }
  if (options.backlinks) {
    if (file) {
      console.error("Error: Use --backlinks without a file argument");
      process.exit(1);
    }
    const target = resolveBacklinkTarget(options.backlinks, vaultPath, index);
    if (!target) {
      console.error("Error: Invalid target for --backlinks");
      process.exit(1);
    }
    const backlinks = readBacklinksIndex(vaultPath) ?? rebuildBacklinksIndex(vaultPath, { entityIndex: index }).backlinks;
    const sources = backlinks.get(target) || [];
    if (sources.length === 0) {
      console.log(`No backlinks found for ${target}`);
      return;
    }
    console.log(`Backlinks \u2192 ${target}`);
    for (const source of sources.sort()) {
      console.log(`  - ${source}`);
    }
    return;
  }
  if (options.orphans) {
    if (file || options.all) {
      console.error("Error: --orphans does not accept a file or --all");
      process.exit(1);
    }
    const result = scanVaultLinks(vaultPath, { entityIndex: index });
    if (result.orphans.length === 0) {
      console.log("\u2713 No orphan links found");
      return;
    }
    const orphans = result.orphans.slice().sort((a, b) => a.target.localeCompare(b.target) || a.source.localeCompare(b.source));
    console.log(`\u26A0 ${orphans.length} orphan link(s) found`);
    for (const orphan of orphans) {
      console.log(`  - ${orphan.source} \u2192 [[${orphan.target}]]`);
    }
    return;
  }
  if (options.all) {
    await linkAllFiles(vaultPath, index, suggestionIndex, options.dryRun);
    return;
  }
  if (!file) {
    console.error("Error: Specify a file or use --all");
    process.exit(1);
  }
  const filePath = path.isAbsolute(file) ? file : path.join(process.cwd(), file);
  if (!fs.existsSync(filePath)) {
    console.error(`Error: File not found: ${filePath}`);
    process.exit(1);
  }
  await linkFile(filePath, index, suggestionIndex, options.dryRun);
}
function filterIndex(index, categories) {
  const entries = /* @__PURE__ */ new Map();
  const byPath = /* @__PURE__ */ new Map();
  for (const [alias, targetPath] of index.entries) {
    const category = targetPath.split("/")[0];
    if (categories.has(category)) {
      entries.set(alias, targetPath);
    }
  }
  for (const [targetPath, entry] of index.byPath) {
    const category = targetPath.split("/")[0];
    if (categories.has(category)) {
      byPath.set(targetPath, entry);
    }
  }
  return { entries, byPath };
}
function resolveBacklinkTarget(input, vaultPath, index) {
  let target = input.trim();
  if (!target) return null;
  if (target.startsWith("[[") && target.endsWith("]]")) {
    target = target.slice(2, -2);
  }
  const pipeIndex = target.indexOf("|");
  if (pipeIndex !== -1) {
    target = target.slice(0, pipeIndex);
  }
  const hashIndex = target.indexOf("#");
  if (hashIndex !== -1) {
    target = target.slice(0, hashIndex);
  }
  target = target.trim();
  if (!target) return null;
  if (target.endsWith(".md")) {
    target = target.slice(0, -3);
  }
  if (target.startsWith("/")) {
    target = target.slice(1);
  }
  const candidate = path.isAbsolute(target) ? target : path.join(vaultPath, target);
  const withExtension = candidate.endsWith(".md") ? candidate : `${candidate}.md`;
  if (fs.existsSync(candidate) && candidate.endsWith(".md")) {
    return toVaultId(vaultPath, candidate);
  }
  if (fs.existsSync(withExtension)) {
    return toVaultId(vaultPath, withExtension);
  }
  const aliasKey = target.toLowerCase();
  if (index.entries.has(aliasKey)) {
    return index.entries.get(aliasKey);
  }
  return target.replace(/\\/g, "/");
}
function toVaultId(vaultPath, filePath) {
  const relative2 = path.relative(vaultPath, filePath).replace(/\.md$/, "");
  return relative2.split(path.sep).join("/");
}
function logSuggestions(filePath, suggestions) {
  if (suggestions.length === 0) return;
  console.log(`
\u{1F4A1} Suggested links in ${path.basename(filePath)}`);
  for (const suggestion of suggestions) {
    console.log(`  Line ${suggestion.line}: "${suggestion.alias}" \u2192 [[${suggestion.path}]]`);
  }
}
async function linkFile(filePath, index, suggestionIndex, dryRun) {
  const content = fs.readFileSync(filePath, "utf-8");
  const linkedContent = autoLink(content, index);
  const suggestions = findUnlinkedMentions(linkedContent, suggestionIndex);
  if (dryRun) {
    const matches = dryRunLink(content, index);
    if (matches.length > 0) {
      console.log(`
\u{1F4C4} ${filePath}`);
      for (const m of matches) {
        console.log(`  Line ${m.line}: "${m.alias}" \u2192 [[${m.path}]]`);
      }
    }
    logSuggestions(filePath, suggestions);
    return matches.length;
  }
  if (linkedContent !== content) {
    fs.writeFileSync(filePath, linkedContent);
    const matches = dryRunLink(content, index);
    console.log(`\u2713 Linked ${matches.length} entities in ${path.basename(filePath)}`);
    logSuggestions(filePath, suggestions);
    return matches.length;
  }
  logSuggestions(filePath, suggestions);
  return 0;
}
async function linkAllFiles(vaultPath, index, suggestionIndex, dryRun) {
  const files = [];
  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!entry.name.startsWith(".") && entry.name !== "archive" && entry.name !== "templates") {
          walk(fullPath);
        }
      } else if (entry.name.endsWith(".md")) {
        files.push(fullPath);
      }
    }
  }
  walk(vaultPath);
  let totalLinks = 0;
  let filesModified = 0;
  for (const file of files) {
    const links = await linkFile(file, index, suggestionIndex, dryRun);
    if (links > 0) {
      totalLinks += links;
      filesModified++;
    }
  }
  console.log(`
${dryRun ? "(dry run) " : ""}${totalLinks} links in ${filesModified} files`);
}
export {
  linkCommand
};
