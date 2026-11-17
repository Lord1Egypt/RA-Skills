import { promises as fs } from "node:fs";
import path from "node:path";

const pagesDir = path.resolve("pages/zh");

const re = new RegExp(
  "第\\s*((?:\\d+)(?:\\s*(?:[-–—、,，]|与|和)\\s*\\d+)*)\\s*章",
  "g",
);

function parseNums(s) {
  return s
    .split(/\s*(?:[-–—、,，]|与|和)\s*/)
    .map(x => parseInt(x.trim(), 10))
    .filter(n => !isNaN(n));
}

function mergeRanges(nums) {
  const sorted = [...new Set(nums)].sort((a, b) => a - b);
  const out = [];
  let i = 0;
  while (i < sorted.length) {
    let j = i;
    while (j + 1 < sorted.length && sorted[j + 1] === sorted[j] + 1) j++;
    if (j > i) out.push(`${sorted[i]}–${sorted[j]}`);
    else out.push(String(sorted[i]));
    i = j + 1;
  }
  return out.join("、");
}

async function processFile(file) {
  const full = path.join(pagesDir, file);
  let text = await fs.readFile(full, "utf8");

  const fmEnd = text.indexOf("\n---", 4);
  const fm = fmEnd >= 0 ? text.slice(0, fmEnd + 4) : "";
  let body = fmEnd >= 0 ? text.slice(fmEnd + 4) : text;

  const masks = [];
  let m;
  const fenceRe = /```[\s\S]*?```/g;
  while ((m = fenceRe.exec(body)) !== null) masks.push([m.index, m.index + m[0].length]);
  const codeRe = /`[^`\n]+`/g;
  while ((m = codeRe.exec(body)) !== null) masks.push([m.index, m.index + m[0].length]);
  const linkRe = /\[[^\]]*\]\([^)]*\)/g;
  while ((m = linkRe.exec(body)) !== null) masks.push([m.index, m.index + m[0].length]);
  masks.sort((a, b) => a[0] - b[0]);

  function inMask(pos) {
    for (const [s, e] of masks) if (pos >= s && pos < e) return true;
    return false;
  }

  body = body.replace(re, (match, expr, offset) => {
    if (inMask(offset)) return match;
    const nums = parseNums(expr);
    if (nums.length === 0) return match;
    return `**${match}**`;
  });

  await fs.writeFile(full, fm + body, "utf8");
  console.log(`Processed ${file}`);
}

const files = (await fs.readdir(pagesDir)).filter(f => f.endsWith(".mdx"));
for (const f of files) await processFile(f);
console.log("renumber-content done (linking hook: customize mapping before running)");
