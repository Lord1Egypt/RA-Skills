import { promises as fs } from "node:fs";
import path from "node:path";

// 计数 GFM 表格数：连续 ≥2 行 `|...|` 且第 2 行是分隔行 `| --- | --- |` 才算一张表。
function countGfmTables(text) {
  const lines = text.split("\n");
  let count = 0;
  let i = 0;
  const sepRe = /^\|\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$/;
  const rowRe = /^\s*\|.*\|\s*$/;
  while (i < lines.length) {
    if (rowRe.test(lines[i]) && i + 1 < lines.length && sepRe.test(lines[i + 1])) {
      count++;
      i += 2;
      while (i < lines.length && rowRe.test(lines[i])) i++;
    } else {
      i++;
    }
  }
  return count;
}

const mdxDir = path.resolve("mdx");
const outFile = path.resolve("metadata/word-count.txt");
await fs.mkdir(path.dirname(outFile), { recursive: true });

const files = (await fs.readdir(mdxDir)).filter(f => f.endsWith(".mdx"));
let totalCjk = 0, totalEn = 0, totalRecipes = 0, totalTables = 0, totalCodeBlocks = 0, totalFigs = 0;
const perChapter = [];

for (const f of files) {
  const raw = await fs.readFile(path.join(mdxDir, f), "utf8");
  let text = raw.replace(/^---[\s\S]*?---/, "");
  const codeBlocks = (text.match(/```[\s\S]*?```/g) || []).length;
  totalCodeBlocks += codeBlocks;
  text = text.replace(/```[\s\S]*?```/g, " ");
  const tables = countGfmTables(text);
  totalTables += tables;
  const figs = (text.match(/!\[[^\]]*\]\([^)]+\)/g) || []).length;
  totalFigs += figs;
  const recipes = (text.match(/🍳 Recipe/g) || []).length;
  totalRecipes += recipes;
  const cjk = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const en = (text.match(/[a-zA-Z]+/g) || []).length;
  totalCjk += cjk;
  totalEn += en;
  perChapter.push({ file: f, cjk, en, est: cjk + en });
}

const totalEst = totalCjk + totalEn;
const lines = [];
lines.push("# Word Count Report");
lines.push("");
lines.push(`Generated: ${new Date().toISOString()}`);
lines.push(`Total CJK characters: ${totalCjk}`);
lines.push(`Total English words: ${totalEn}`);
lines.push(`Estimated total word count: ${totalEst}`);
lines.push(`Chapters: ${files.length}`);
lines.push(`Recipes: ${totalRecipes}`);
lines.push(`Tables: ${totalTables}`);
lines.push(`Code blocks: ${totalCodeBlocks}`);
lines.push(`Figures/images: ${totalFigs}`);
lines.push("");
lines.push("## Per-chapter breakdown");
lines.push("");
lines.push("| File | CJK | EN | Est. words |");
lines.push("|---|---|---|---|");
for (const c of perChapter) {
  lines.push(`| ${c.file} | ${c.cjk} | ${c.en} | ${c.est} |`);
}

await fs.writeFile(outFile, lines.join("\n"), "utf8");
console.log(`Wrote ${outFile}`);
console.log(`Total est. words: ${totalEst} (CJK ${totalCjk}, EN ${totalEn})`);
