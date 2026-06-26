import {
  getSortedAliases
} from "./chunk-J7ZWCI2C.js";

// src/lib/auto-linker.ts
function findProtectedRanges(content) {
  const ranges = [];
  const fmMatch = content.match(/^---\n[\s\S]*?\n---/);
  if (fmMatch) {
    ranges.push({ start: 0, end: fmMatch[0].length });
  }
  const codeBlockRegex = /```[\s\S]*?```|~~~[\s\S]*?~~~/g;
  let match;
  while ((match = codeBlockRegex.exec(content)) !== null) {
    ranges.push({ start: match.index, end: match.index + match[0].length });
  }
  const inlineCodeRegex = /`[^`]+`/g;
  while ((match = inlineCodeRegex.exec(content)) !== null) {
    ranges.push({ start: match.index, end: match.index + match[0].length });
  }
  const wikiLinkRegex = /\[\[[^\]]+\]\]/g;
  while ((match = wikiLinkRegex.exec(content)) !== null) {
    ranges.push({ start: match.index, end: match.index + match[0].length });
  }
  const urlRegex = /https?:\/\/[^\s)>\]]+/g;
  while ((match = urlRegex.exec(content)) !== null) {
    ranges.push({ start: match.index, end: match.index + match[0].length });
  }
  return ranges;
}
function isProtected(pos, ranges) {
  return ranges.some((r) => pos >= r.start && pos < r.end);
}
function createLineLookup(content) {
  const lines = content.split("\n");
  let charPos = 0;
  const lineStarts = [];
  for (const line of lines) {
    lineStarts.push(charPos);
    charPos += line.length + 1;
  }
  return (pos) => {
    for (let i = lineStarts.length - 1; i >= 0; i--) {
      if (pos >= lineStarts[i]) return i + 1;
    }
    return 1;
  };
}
function autoLink(content, index) {
  const protectedRanges = findProtectedRanges(content);
  const sortedAliases = getSortedAliases(index);
  const linkedEntities = /* @__PURE__ */ new Set();
  let result = content;
  let offset = 0;
  for (const { alias, path } of sortedAliases) {
    if (linkedEntities.has(path)) continue;
    const escapedAlias = alias.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(`\\b${escapedAlias}\\b`, "gi");
    let match;
    while ((match = regex.exec(content)) !== null) {
      const originalPos = match.index;
      const adjustedPos = originalPos + offset;
      if (isProtected(originalPos, protectedRanges)) continue;
      const beforeMatch = result.substring(0, adjustedPos);
      const openBrackets = (beforeMatch.match(/\[\[/g) || []).length;
      const closeBrackets = (beforeMatch.match(/\]\]/g) || []).length;
      if (openBrackets > closeBrackets) continue;
      const originalText = match[0];
      const replacement = originalText.toLowerCase() === path.split("/").pop()?.toLowerCase() ? `[[${path}]]` : `[[${path}|${originalText}]]`;
      result = result.substring(0, adjustedPos) + replacement + result.substring(adjustedPos + originalText.length);
      offset += replacement.length - originalText.length;
      linkedEntities.add(path);
      break;
    }
  }
  return result;
}
function dryRunLink(content, index) {
  const protectedRanges = findProtectedRanges(content);
  const sortedAliases = getSortedAliases(index);
  const linkedEntities = /* @__PURE__ */ new Set();
  const matches = [];
  const getLineNumber = createLineLookup(content);
  for (const { alias, path } of sortedAliases) {
    if (linkedEntities.has(path)) continue;
    const escapedAlias = alias.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(`\\b${escapedAlias}\\b`, "gi");
    let match;
    while ((match = regex.exec(content)) !== null) {
      if (isProtected(match.index, protectedRanges)) continue;
      matches.push({
        alias: match[0],
        path,
        line: getLineNumber(match.index)
      });
      linkedEntities.add(path);
      break;
    }
  }
  return matches;
}
function findUnlinkedMentions(content, index) {
  const protectedRanges = findProtectedRanges(content);
  const sortedAliases = getSortedAliases(index);
  const matches = [];
  const seen = /* @__PURE__ */ new Set();
  const getLineNumber = createLineLookup(content);
  for (const { alias, path } of sortedAliases) {
    if (seen.has(path)) continue;
    const escapedAlias = alias.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(`\\b${escapedAlias}\\b`, "gi");
    let match;
    while ((match = regex.exec(content)) !== null) {
      if (isProtected(match.index, protectedRanges)) continue;
      matches.push({
        alias: match[0],
        path,
        line: getLineNumber(match.index)
      });
      seen.add(path);
      break;
    }
  }
  return matches;
}

export {
  autoLink,
  dryRunLink,
  findUnlinkedMentions
};
