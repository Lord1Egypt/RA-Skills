#!/usr/bin/env node
// lmdx2tex.mjs
//
// LLM-driven MDX → ElegantBook LaTeX 转换器。
// 核心思路：逐个读取 mdx/*.mdx 文件，通过 LLM 子 agent 智能转换为 LaTeX 章节，
// 然后组装 main.tex（使用 ElegantBook 文档类）。
//
// 用法（CLI）：node lmdx2tex.mjs [--title "书名"] [--author "作者"]
//   - 输入：工作目录下 mdx/*.mdx
//   - 输出：latex/chapters/*.tex、latex/main.tex、latex/figures/（拷贝图）
//
// 与 mdx2tex.mjs 的区别：
//   - mdx2tex.mjs 使用正则替换（脆弱，容易转义错误）
//   - lmdx2tex.mjs 使用 LLM 逐章转换（语义理解，转换质量高）

import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";
import { parseFrontmatter } from "./lib/mdx-utils.mjs";
import { extractDiagramBlocks, renderAll, replaceBlocks } from "./lib/diagram-renderer.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_ROOT = path.resolve(__dirname, "..");

// ---------- CLI 参数解析 ----------
const args = process.argv.slice(2);
function getArg(name, def) {
  const i = args.indexOf(`--${name}`);
  if (i >= 0 && i + 1 < args.length) return args[i + 1];
  return def;
}
const BOOK_TITLE = getArg("title", "CookBook");
const BOOK_AUTHOR = getArg("author", "Cookbook Generator");
const BOOK_SUBTITLE = getArg("subtitle", "");
const BOOK_VERSION = getArg("version", "1.0");
const BOOK_INSTITUTE = getArg("institute", "");

// ---------- 目录配置 ----------
const mdxDir = path.resolve("mdx");
const texDir = path.resolve("latex/chapters");
const figDir = path.resolve("latex/figures");
const diagramSrcDir = path.resolve("latex/diagrams");

await fs.mkdir(texDir, { recursive: true });
await fs.mkdir(figDir, { recursive: true });
await fs.mkdir(diagramSrcDir, { recursive: true });

// ---------- 读取 Prompt 模板 ----------
const promptTemplatePath = path.join(SKILL_ROOT, "assets", "prompts", "mdx-to-latex.md");
const PROMPT_TEMPLATE = await fs.readFile(promptTemplatePath, "utf8");

// ---------- 主转换流程 ----------
console.log("=== LLM-driven MDX → ElegantBook LaTeX 转换器 ===\n");

const mdxEntries = [];
for (const f of (await fs.readdir(mdxDir)).filter(f => f.endsWith(".mdx")).sort()) {
  const mdxPath = path.join(mdxDir, f);
  const raw = await fs.readFile(mdxPath, "utf8");
  const fm = parseFrontmatter(raw);
  const chapNum = Number.parseInt(fm.fm.chapter, 10);
  mdxEntries.push({
    file: f,
    mdxPath,
    raw,
    title: fm.title,
    slug: fm.slug,
    fm: fm.fm,
    order: Number.isFinite(chapNum) ? chapNum : Number.MAX_SAFE_INTEGER,
  });
}
mdxEntries.sort((a, b) => a.order - b.order || a.file.localeCompare(b.file));

if (mdxEntries.length === 0) {
  console.error("错误：mdx/ 目录下没有找到 .mdx 文件");
  process.exit(1);
}

console.log(`找到 ${mdxEntries.length} 个 MDX 章节文件（按 chapter: 字段排序）:\n`);
for (const e of mdxEntries) console.log(`  [${e.order === Number.MAX_SAFE_INTEGER ? " -" : String(e.order).padStart(2)}] ${e.file}  →  ${e.title}`);
console.log("");

const chapterRefs = [];
const convertedSlugs = [];
const pendingTasks = [];

for (const entry of mdxEntries) {
  const f = entry.file;
  const mdxPath = entry.mdxPath;
  const raw = entry.raw;
  const title = entry.title;
  const slug = entry.slug;

  console.log(`\n━━━ 转换章节: ${f} (${title}) ━━━`);

  // ---------- 处理 mermaid/plantuml 代码块：先渲染成 SVG ----------
  // 抽取本章所有图表代码块，kroki 渲染到 mdx/public/figures/diagram-<hash>.svg，
  // 然后把 MDX 里的 ```mermaid/```plantuml 代码块替换为 LaTeX figure 引用。
  const blocks = extractDiagramBlocks(raw);
  let mdxForLlm = raw;
  if (blocks.length > 0) {
    console.log(`  提取到 ${blocks.length} 个 mermaid/plantuml 代码块，渲染中...`);
    const results = await renderAll(path.resolve("."), blocks, {
      onProgress: (m) => console.log("   ", m),
    });
    for (const r of results) {
      try {
        await fs.copyFile(r.svgAbsPath, path.join(figDir, r.svgFileName));
      } catch {}
    }
    mdxForLlm = replaceBlocks(raw, results, (r) => {
      const caption = r.caption.replace(/[\\{}%_#&$]/g, (c) => `\\${c}`);
      const fname = r.svgFileName.replace(/\.svg$/, "");
      return `\n\n\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=0.85\\textwidth]{${fname}}\n\\caption{${caption}}\n\\end{figure}\n\n`;
    });
    console.log(`  ✓ 已替换 ${blocks.length} 个图表代码块为 LaTeX figure 引用`);
  }

  // 构造 LLM prompt（写入 prompt 文件供 agent 读取）
  const prompt = `${PROMPT_TEMPLATE}

---

## 待转换的 MDX 文件（${f}）：

\`\`\`mdx
${mdxForLlm}
\`\`\`

---

请立即开始转换。只输出 LaTeX 代码，不要任何解释。输出文件第一行必须是 \\chapter{...} 或 \\chapter*{...}。
注意：mermaid/plantuml 代码块已被预处理为 \\begin{figure}...\\end{figure} 引用，请保留这些 LaTeX 代码原样，不要再尝试渲染或处理 mermaid 源码。`;

  const promptFile = path.join(texDir, `._prompt_${slug}.txt`);
  await fs.writeFile(promptFile, prompt, "utf8");

  const texOutputPath = path.join(texDir, `${slug}.tex`);

  console.log(`  PROMPT_FILE: ${promptFile}`);
  console.log(`  OUTPUT_FILE: ${texOutputPath}`);

  // 尝试读取已有缓存
  let texContent = null;
  try {
    texContent = await fs.readFile(texOutputPath, "utf8");
    if (!texContent.trim().startsWith("\\chapter")) {
      texContent = null;
    } else {
      console.log(`  ✓ 使用缓存结果`);
    }
  } catch {
    // 文件不存在
  }

  if (!texContent) {
    pendingTasks.push({
      format: "latex",
      mdxFile: f,
      mdxPath,
      promptFile,
      outputFile: texOutputPath,
      slug,
      title,
      validation: { mustStartWith: "\\chapter" },
    });

    const placeholder = `% LLM_CONVERSION_PENDING: ${f}
% This chapter needs to be converted by an LLM agent.
% Prompt file: ${promptFile}
% Output file: ${texOutputPath}
%
% After filling this file, re-run: node lmdx2tex.mjs
\\chapter{${title.replace(/[_#&%$]/g, '\\$&')}}
\\label{ch:${slug}}

% [LLM output will replace this block]
`;
    await fs.writeFile(texOutputPath, placeholder, "utf8");
    console.log(`  ⚠ 写入占位符 — 待 LLM 转换`);
  }

  chapterRefs.push({ slug, f, title, texPath: texOutputPath });
  convertedSlugs.push(slug);
}

// ---------- 拷贝图片资源 ----------
console.log("\n━━━ 拷贝资源文件 ━━━");

const figSrc = path.join(mdxDir, "public", "figures");
try {
  const figs = await fs.readdir(figSrc);
  let count = 0;
  for (const fn of figs) {
    const s = path.join(figSrc, fn);
    if ((await fs.stat(s)).isFile()) {
      await fs.copyFile(s, path.join(figDir, fn));
      count++;
    }
  }
  console.log(`  拷贝了 ${count} 个图片到 latex/figures/`);
} catch {
  console.log("  未找到 public/figures 目录，跳过图片拷贝");
}

const diagSrc = path.join(mdxDir, "public", "diagrams-src");
try {
  const diags = await fs.readdir(diagSrc);
  let count = 0;
  for (const fn of diags) {
    const s = path.join(diagSrc, fn);
    if ((await fs.stat(s)).isFile()) {
      await fs.copyFile(s, path.join(diagramSrcDir, fn));
      count++;
    }
  }
  console.log(`  拷贝了 ${count} 个图表源文件到 latex/diagrams/`);
} catch {
  // 可选目录，不存在则跳过
}

// ---------- 生成 main.tex ----------
console.log("\n━━━ 生成 main.tex ━━━");

const mainTemplatePath = path.join(SKILL_ROOT, "assets", "elegantbook-main.template.tex.txt");
let mainTemplate = await fs.readFile(mainTemplatePath, "utf8");

const inputs = chapterRefs.map(c => `\\input{chapters/${c.slug}}`).join("\n");

mainTemplate = mainTemplate
  .replace(/__BOOK_TITLE__/g, BOOK_TITLE)
  .replace(/__BOOK_SUBTITLE__/g, BOOK_SUBTITLE)
  .replace(/__BOOK_AUTHOR__/g, BOOK_AUTHOR)
  .replace(/__BOOK_INSTITUTE__/g, BOOK_INSTITUTE)
  .replace(/__BOOK_VERSION__/g, BOOK_VERSION)
  .replace("__CHAPTER_INPUTS__", inputs);

await fs.writeFile(path.resolve("latex/main.tex"), mainTemplate, "utf8");

// ---------- 输出结构化任务清单（供 TRAE agent 编排）----------
// 保留 prompt 文件以便 agent 读取（不删除），并写一份 JSON 清单。
const planPath = path.resolve("latex/.conversion-plan.json");
const plan = {
  format: "latex",
  bookTitle: BOOK_TITLE,
  totalChapters: chapterRefs.length,
  pendingCount: pendingTasks.length,
  pending: pendingTasks,
  cached: chapterRefs
    .filter(c => !pendingTasks.some(p => p.slug === c.slug))
    .map(c => ({ slug: c.slug, file: c.f, title: c.title, texPath: c.texPath })),
  instructions: pendingTasks.length
    ? [
        "For each task in `pending`, invoke a Task/sub-agent with these instructions:",
        "  1. Read `promptFile` (it contains full conversion rules + the MDX source).",
        "  2. Convert the MDX chapter to ElegantBook LaTeX per those rules.",
        "  3. Write ONLY raw LaTeX code to `outputFile` (no markdown fences, no prose).",
        "  4. First line must be \\chapter{...} or \\chapter*{...}.",
        "After all tasks complete, re-run `node lmdx2tex.mjs` to regenerate main.tex with final content.",
      ]
    : ["All chapters already converted; main.tex is ready for xelatex."],
};
await fs.writeFile(planPath, JSON.stringify(plan, null, 2), "utf8");

// ---------- 清理临时 prompt 文件（仅对已缓存章节） ----------
for (const c of chapterRefs) {
  if (pendingTasks.some(p => p.slug === c.slug)) continue;
  const pf = path.join(texDir, `._prompt_${c.slug}.txt`);
  try { await fs.unlink(pf); } catch {}
}

console.log(`\n━━━ 完成 ━━━`);
console.log(`\n已生成:`);
console.log(`  - latex/main.tex (主文件，使用 ElegantBook 文档类)`);
console.log(`  - latex/chapters/ (${chapterRefs.length} 个章节文件)`);
console.log(`  - latex/figures/ (图片资源)`);
if (pendingTasks.length > 0) {
  console.log(`\n⚠ 有 ${pendingTasks.length} 个章节需要 LLM 转换：`);
  for (const t of pendingTasks) {
    console.log(`    • ${t.slug}  →  ${t.outputFile}`);
  }
  console.log(`\n任务清单已写入: ${planPath}`);
  console.log(`主 agent（TRAE）读取该 JSON 后可并发调度 Task 逐章转换。`);
  console.log(`全部转换完成后重新运行: node lmdx2tex.mjs`);
} else {
  console.log(`\n✓ 所有章节已转换完成。`);
}
console.log(`\n编译方法:`);
console.log(`  1. 将 ElegantBook 的 elegantbook.cls 放入 latex/ 目录（TeXLive 用户已自带）`);
console.log(`  2. cd latex && xelatex main.tex && xelatex main.tex`);
