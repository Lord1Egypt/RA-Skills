import { promises as fs } from "node:fs";
import path from "node:path";

const pagesDir = path.resolve("pages/zh");
const metaPath = path.join(pagesDir, "_meta.ts");

const GROUP_SEPARATORS = [
  { before: "ch00", title: "📖 前言与全景" },
  { before: "ch04", title: "I · 核心概念" },
  { before: "ch07", title: "II · 架构与实现" },
  { before: "ch10", title: "III · 实战 Recipes" },
  { before: "ch13", title: "IV · 生产实践" },
  { before: "appendix", title: "📚 附录" },
];

const TITLE_MAP = {
  index: "🏠 首页",
  preface: "前言",
  references: "参考文献",
  downloads: "📥 下载",
};

function chapNum(slug) {
  const m = slug.match(/^ch(\d+)/);
  return m ? parseInt(m[1], 10) : null;
}

function humanTitle(slug) {
  if (TITLE_MAP[slug]) return TITLE_MAP[slug];
  return slug
    .replace(/^ch\d+-/, "")
    .replace(/^appendix-([a-z])-/, (_, l) => `附录 ${l.toUpperCase()}：`)
    .split("-")
    .map(w => w[0].toUpperCase() + w.slice(1))
    .join(" ");
}

const files = (await fs.readdir(pagesDir))
  .filter(f => f.endsWith(".mdx"))
  .map(f => f.replace(/\.mdx$/, ""));

const chapters = files.filter(f => /^ch\d+/.test(f)).sort((a, b) => chapNum(a) - chapNum(b));
const others = files.filter(f => !/^ch\d+/.test(f));

const ordered = [];
if (others.includes("index")) ordered.push("index");
if (others.includes("preface")) ordered.push("preface");

let sepIdx = 0;
for (const ch of chapters) {
  while (sepIdx < GROUP_SEPARATORS.length) {
    const g = GROUP_SEPARATORS[sepIdx];
    const gNum = g.before === "appendix" ? Infinity : chapNum(g.before) ?? 0;
    if (chapNum(ch) >= gNum && g.before !== "appendix") {
      ordered.push(`---sep-${sepIdx}`);
      sepIdx++;
    } else break;
  }
  ordered.push(ch);
}

if (chapters.length > 0) {
  ordered.push(`---sep-${sepIdx}`);
  sepIdx++;
}
for (const o of others) {
  if (o === "index" || o === "preface" || o === "downloads" || o === "references") continue;
  ordered.push(o);
}
if (others.includes("references")) ordered.push("references");
if (others.includes("downloads")) ordered.push("downloads");

const lines = ["// 自动生成 - 如需调整顺序/标题请修改 scripts/build-meta.mjs", "export default {"];
for (const key of ordered) {
  if (key.startsWith("---sep-")) {
    const idx = parseInt(key.split("-")[2], 10);
    lines.push(`  "${key}": { type: "separator", title: ${JSON.stringify(GROUP_SEPARATORS[idx]?.title ?? "")} },`);
  } else {
    lines.push(`  ${JSON.stringify(key)}: ${JSON.stringify(humanTitle(key))},`);
  }
}
lines.push("};");

await fs.writeFile(metaPath, lines.join("\n"), "utf8");
console.log(`Wrote ${metaPath}`);
