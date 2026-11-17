#!/usr/bin/env node
// lbuild-epub.mjs
//
// LLM-driven MDX → EPUB3 转换器。
// 核心思路：逐个读取 mdx/*.mdx 文件，通过 LLM 子 agent 智能转换为 XHTML 章节，
// 然后组装 EPUB3 包（OPF/NCX/NAV/CSS/Fonts），最后用 Python zipfile 打包为合规 EPUB。
//
// 用法（CLI）：node lbuild-epub.mjs [--title "书名"]
//   - 输入：工作目录下 mdx/*.mdx
//   - 输出：epub/book.epub

import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";
import { parseFrontmatter } from "./lib/mdx-utils.mjs";
import { extractDiagramBlocks, renderAll, replaceBlocks } from "./lib/diagram-renderer.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_ROOT = path.resolve(__dirname, "..");

// ---------- CLI 参数 ----------
const args = process.argv.slice(2);
function getArg(name, def) {
  const i = args.indexOf(`--${name}`);
  if (i >= 0 && i + 1 < args.length) return args[i + 1];
  return def;
}
const BOOK_TITLE = getArg("title", "CookBook");
const BOOK_LANG = getArg("lang", "zh-CN");

// ---------- 目录配置 ----------
const mdxDir = path.resolve("mdx");
const outDir = path.resolve("epub");
const buildDir = path.join(outDir, "build");
const OEBPS = path.join(buildDir, "OEBPS");

await fs.mkdir(path.join(OEBPS, "Text"), { recursive: true });
await fs.mkdir(path.join(OEBPS, "Images"), { recursive: true });
await fs.mkdir(path.join(OEBPS, "css"), { recursive: true });
await fs.mkdir(path.join(OEBPS, "Fonts"), { recursive: true });
await fs.mkdir(path.join(buildDir, "META-INF"), { recursive: true });

// ---------- 工具 ----------
function escHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ---------- 读取 Prompt 模板 ----------
const promptTemplatePath = path.join(SKILL_ROOT, "assets", "prompts", "mdx-to-epub.md");
const PROMPT_TEMPLATE = await fs.readFile(promptTemplatePath, "utf8");

// ---------- 主流程 ----------
console.log("=== LLM-driven MDX → EPUB3 转换器 ===\n");

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

const chapterFiles = [];
const pendingTasks = [];

for (const entry of mdxEntries) {
  const f = entry.file;
  const mdxPath = entry.mdxPath;
  const raw = entry.raw;
  const title = entry.title;
  const slug = entry.slug;
  const xhtmlName = f.replace(/\.mdx$/, ".xhtml");
  const xhtmlPath = path.join(OEBPS, "Text", xhtmlName);

  console.log(`\n━━━ 转换章节: ${f} (${title}) ━━━`);

  // ---------- 处理 mermaid/plantuml 代码块：先渲染成 SVG ----------
  const blocks = extractDiagramBlocks(raw);
  let mdxForLlm = raw;
  if (blocks.length > 0) {
    console.log(`  提取到 ${blocks.length} 个 mermaid/plantuml 代码块，渲染中...`);
    const results = await renderAll(path.resolve("."), blocks, {
      onProgress: (m) => console.log("   ", m),
    });
    for (const r of results) {
      try {
        await fs.copyFile(r.svgAbsPath, path.join(imgDir, r.svgFileName));
      } catch {}
    }
    mdxForLlm = replaceBlocks(raw, results, (r) => {
      const alt = r.caption.replace(/"/g, "&quot;");
      return `\n\n![${r.caption}](/figures/${r.svgFileName})\n\n图：${r.caption}\n\n`;
    });
    console.log(`  ✓ 已替换 ${blocks.length} 个图表代码块为 Markdown 图片引用`);
  }

  // 构造 LLM prompt
  const prompt = `${PROMPT_TEMPLATE}

---

## 待转换的 MDX 文件（${f}）：

\`\`\`mdx
${mdxForLlm}
\`\`\`

---

请立即开始转换。只输出完整的 XHTML 文档，不要任何解释。输出必须以 <?xml 开头。
注意：mermaid/plantuml 代码块已被预处理为 ![caption](/figures/diagram-<hash>.svg) 图片语法，请把这些图片转换为 <figure><img src="../Images/<svg-file>"/></figure>，不要保留 mermaid 源码。`;

  const promptFile = path.join(OEBPS, "Text", `._prompt_${slug}.txt`);
  await fs.writeFile(promptFile, prompt, "utf8");

  console.log(`  PROMPT_FILE: ${promptFile}`);
  console.log(`  OUTPUT_FILE: ${xhtmlPath}`);

  let xhtmlContent = null;
  try {
    xhtmlContent = await fs.readFile(xhtmlPath, "utf8");
    if (!xhtmlContent.includes("<?xml")) {
      xhtmlContent = null;
    } else {
      console.log(`  ✓ 使用缓存结果`);
    }
  } catch {}

  if (!xhtmlContent) {
    pendingTasks.push({
      format: "epub-xhtml",
      mdxFile: f,
      mdxPath,
      promptFile,
      outputFile: xhtmlPath,
      slug,
      title,
      validation: { mustStartWith: "<?xml" },
    });

    // 生成占位 XHTML
    const placeholder = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<title>${escHtml(title)}</title>
<link rel="stylesheet" type="text/css" href="../css/stylesheet.css"/>
</head>
<body>
<h1>${escHtml(title)}</h1>
<p><em>此章节需要 LLM 转换。任务清单见 ${escHtml("epub/.conversion-plan.json")}。</em></p>
</body>
</html>`;
    await fs.writeFile(xhtmlPath, placeholder, "utf8");
    xhtmlContent = placeholder;
    console.log(`  ⚠ 写入占位符 — 待 LLM 转换`);
  }

  chapterFiles.push({
    id: slug,
    href: `Text/${xhtmlName}`,
    title,
    f,
  });
}

// ---------- 拷贝图片 ----------
console.log("\n━━━ 拷贝图片资源 ━━━");
const manifestExtra = [];
const figSrcDir = path.resolve(mdxDir, "public", "figures");
try {
  const figs = await fs.readdir(figSrcDir);
  let idx = 0;
  for (const fn of figs) {
    const src = path.join(figSrcDir, fn);
    if (!(await fs.stat(src)).isFile()) continue;
    await fs.copyFile(src, path.join(OEBPS, "Images", fn));
    const ext = path.extname(fn).slice(1).toLowerCase();
    const mime = ext === "svg" ? "image/svg+xml"
               : ext === "png" ? "image/png"
               : ext === "jpg" || ext === "jpeg" ? "image/jpeg"
               : ext === "gif" ? "image/gif"
               : "application/octet-stream";
    manifestExtra.push(`<item id="img-${idx++}" href="Images/${fn}" media-type="${mime}"/>`);
  }
  console.log(`  拷贝了 ${figs.length} 个图片到 OEBPS/Images/`);
} catch {
  console.log("  未找到图片目录，跳过");
}

manifestExtra.push(`<item id="css" href="css/stylesheet.css" media-type="text/css"/>`);

// ---------- 生成 content.opf ----------
console.log("\n━━━ 生成 EPUB 元数据文件 ━━━");

const manifestItems = [
  `<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>`,
  ...manifestExtra,
  ...chapterFiles.map(c =>
    `<item id="${c.id}" href="${c.href}" media-type="application/xhtml+xml"/>`),
].join("\n");
const spineItems = chapterFiles.map(c => `<itemref idref="${c.id}"/>`).join("\n");

const opf = `<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>${escHtml(BOOK_TITLE)}</dc:title>
<dc:language>${BOOK_LANG}</dc:language>
<dc:identifier id="uid">urn:cookbook:${Date.now()}</dc:identifier>
<dc:creator>Cookbook Forge</dc:creator>
<meta property="dcterms:modified">${new Date().toISOString().replace(/\.\d{3}Z$/, 'Z')}</meta>
</metadata>
<manifest>
${manifestItems}
</manifest>
<spine>
${spineItems}
</spine>
</package>`;
await fs.writeFile(path.join(OEBPS, "content.opf"), opf, "utf8");
console.log("  ✓ content.opf");

// ---------- container.xml ----------
const container = `<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>`;
await fs.writeFile(path.join(buildDir, "META-INF", "container.xml"), container, "utf8");
console.log("  ✓ META-INF/container.xml");

// ---------- nav.xhtml (EPUB3 导航) ----------
const navItems = chapterFiles.map(c =>
  `      <li><a href="${c.href}">${escHtml(c.title)}</a></li>`
).join("\n");
const nav = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><title>目录</title></head>
<body>
<nav epub:type="toc">
<h2>目录</h2>
<ol>
${navItems}
</ol>
</nav>
</body></html>`;
await fs.writeFile(path.join(OEBPS, "nav.xhtml"), nav, "utf8");
console.log("  ✓ nav.xhtml");

// ---------- mimetype ----------
await fs.writeFile(path.join(buildDir, "mimetype"), "application/epub+zip", "ascii");
console.log("  ✓ mimetype");

// ---------- CSS ----------
// 优先使用优化过的 CSS（llm 生成的 EPUB 会用 cookbook-forge 的标准 CSS）
const cssSrc = path.join(SKILL_ROOT, "assets", "stylesheet.template.css");
let css = await fs.readFile(cssSrc, "utf8");

// 追加 CookBook 专用样式
css += `
/* === CookBook Forge LLM Converter 追加样式 === */
.callout {
  margin: 1em 0;
  padding: 0.75em 1em;
  border-radius: 4px;
  page-break-inside: avoid;
  break-inside: avoid;
}
.callout-chapteroutline { border-left: 4px solid #3b82f6; background: rgba(59,130,246,0.08); }
.callout-recipe         { border-left: 4px solid #f59e0b; background: rgba(245,158,11,0.08); }
.callout-pitfall        { border-left: 4px solid #ef4444; background: rgba(239,68,68,0.08); }
.callout-keypoints      { border-left: 4px solid #22c55e; background: rgba(34,197,94,0.08); }
.callout h4 { margin-top: 0; color: #000000 !important; }

table.gfm-table {
  display: table;
  border-collapse: collapse;
  margin: 1em auto;
  width: auto;
  max-width: 100%;
  border-top: 2px solid #000000;
  border-bottom: 2px solid #000000;
}
table.gfm-table th {
  font-weight: 700;
  color: #000000 !important;
  border-bottom: 1.5px solid #000000;
  padding: 0.45em 0.8em;
  text-align: left;
}
table.gfm-table td {
  padding: 0.45em 0.8em;
  border-bottom: 1px solid #cccccc;
  vertical-align: top;
}
table.gfm-table thead { border-top: none; }
table.gfm-table tbody tr:last-child td { border-bottom: none; }

.math-inline {
  font-family: "Cambria Math", "Latin Modern Math", "Times New Roman", serif;
  font-style: italic;
}
.math-block {
  text-align: center;
  margin: 1em 0;
  font-family: "Cambria Math", "Latin Modern Math", "Times New Roman", serif;
  font-style: italic;
  overflow-x: auto;
}

figure {
  display: block;
  text-align: center;
  margin: 1.2em auto;
  page-break-inside: avoid;
}
figure img {
  display: block;
  max-width: 100% !important;
  height: auto;
  margin: 0.5em auto;
}
figcaption {
  display: block;
  font-size: 0.95em;
  color: #000000 !important;
  text-align: center;
  margin: 0.4em auto 0.8em;
}

.diagram-placeholder {
  text-align: center;
  color: #666;
  font-size: 0.9em;
  border: 1px dashed #aaa;
  padding: 1.5em;
  margin: 1em 0;
  background: #f9f9f9;
}

pre.code-block {
  display: block;
  background: #f8f9fb !important;
  border: 1px solid #d4d8de !important;
  border-left: 4px solid #4a90d9 !important;
  border-radius: 6px;
  padding: 0.8em 1em;
  margin: 1em 0;
  font-family: "LXGW WenKai Mono", "Source Code Pro", Consolas, monospace !important;
  font-size: 0.92em !important;
  line-height: 1.6;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #2d2d2d !important;
  page-break-inside: avoid;
}
pre.code-block code {
  display: inline;
  border: none !important;
  background: transparent !important;
  padding: 0;
  font-size: inherit;
  font-family: inherit;
}
code:not(pre code) {
  font-family: "LXGW WenKai Mono", "Source Code Pro", Consolas, monospace !important;
  font-size: 0.93em;
  background: #f0f2f5 !important;
  padding: 0.1em 0.3em;
  border-radius: 3px;
}

hr {
  border: none;
  border-top: 1px solid #ccc;
  margin: 1.5em 0;
}
`;
await fs.writeFile(path.join(OEBPS, "css", "stylesheet.css"), css, "utf8");
console.log("  ✓ css/stylesheet.css (EpubReaderOptimizer + CookBook 样式)");

// ---------- 打包前清理临时 prompt 文件 ----------
for (const c of chapterFiles) {
  const pf = path.join(OEBPS, "Text", `._prompt_${c.id}.txt`);
  try { await fs.unlink(pf); } catch {}
}

// ---------- 打包 EPUB（使用 Python zipfile）----------
console.log("\n━━━ 打包 EPUB ━━━");

const epubOut = path.join(outDir, "book.epub");
const buildScript = `
import os, zipfile
from pathlib import Path

SRC = Path(r"${buildDir.replace(/\\/g, "\\\\")}")
OUT = Path(r"${epubOut.replace(/\\/g, "\\\\")}")

if OUT.exists():
    OUT.unlink()

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
    zi = zipfile.ZipInfo("mimetype")
    zi.compress_type = zipfile.ZIP_STORED
    zi.external_attr = 0o644 << 16
    zf.writestr(zi, "application/epub+zip")

    added = {"mimetype"}
    for root, _, files in os.walk(SRC):
        for name in sorted(files):
            full = Path(root) / name
            rel = full.relative_to(SRC).as_posix()
            if rel in added:
                continue
            zf.write(full, rel, compress_type=zipfile.ZIP_DEFLATED)
            added.add(rel)

# 自检
z = zipfile.ZipFile(OUT)
assert z.namelist()[0] == "mimetype", "mimetype must be first entry"
assert z.getinfo("mimetype").compress_type == zipfile.ZIP_STORED
assert z.read("mimetype") == b"application/epub+zip"
print(f"EPUB OK: {len(z.namelist())} entries, {OUT.stat().st_size / 1024:.1f} KB")
`;

const tmpScript = path.join(outDir, "_pack_epub.py");
await fs.writeFile(tmpScript, buildScript, "utf8");
try {
  execSync(`python "${tmpScript}"`, { stdio: "inherit" });
} finally {
  try { await fs.unlink(tmpScript); } catch {}
}

// ---------- 输出结构化任务清单（供 TRAE agent 编排）----------
const planPath = path.join(outDir, ".conversion-plan.json");
const plan = {
  format: "epub",
  bookTitle: BOOK_TITLE,
  totalChapters: chapterFiles.length,
  pendingCount: pendingTasks.length,
  pending: pendingTasks,
  cached: chapterFiles
    .filter(c => !pendingTasks.some(p => p.slug === c.id))
    .map(c => ({ slug: c.id, file: c.f, title: c.title, href: c.href })),
  instructions: pendingTasks.length
    ? [
        "For each task in `pending`, invoke a Task/sub-agent with these instructions:",
        "  1. Read `promptFile` (full conversion rules + MDX source).",
        "  2. Convert the MDX chapter to EPUB3 XHTML per those rules.",
        "  3. Write ONLY the complete XHTML document to `outputFile` (no markdown fences, no prose).",
        "  4. Output must start with `<?xml` and have <h1>chapter title</h1> as the first element in <body>.",
        "After all tasks complete, re-run `node lbuild-epub.mjs` to regenerate content.opf/nav.xhtml and re-zip book.epub.",
      ]
    : ["All chapters already converted; book.epub is ready."],
};
await fs.writeFile(planPath, JSON.stringify(plan, null, 2), "utf8");

// ---------- 清理临时 prompt 文件（仅对已缓存章节）----------
for (const c of chapterFiles) {
  if (pendingTasks.some(p => p.slug === c.id)) continue;
  const pf = path.join(OEBPS, "Text", `._prompt_${c.id}.txt`);
  try { await fs.unlink(pf); } catch {}
}

console.log(`\n━━━ 完成 ━━━`);
console.log(`EPUB 输出: ${epubOut}`);
if (pendingTasks.length > 0) {
  console.log(`\n⚠ 有 ${pendingTasks.length} 个章节需要 LLM 转换：`);
  for (const t of pendingTasks) {
    console.log(`    • ${t.slug}  →  ${t.outputFile}`);
  }
  console.log(`\n任务清单已写入: ${planPath}`);
  console.log(`主 agent（TRAE）读取该 JSON 后可并发调度 Task 逐章转换。`);
  console.log(`全部转换完成后重新运行: node lbuild-epub.mjs`);
} else {
  console.log(`\n✓ 所有章节已转换完成，EPUB 可直接分发。`);
}
