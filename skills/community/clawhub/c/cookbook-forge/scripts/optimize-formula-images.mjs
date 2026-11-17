#!/usr/bin/env node
// optimize-formula-images.mjs
//
// 处理"公式即图片"型 EPUB（出版社/Sigil 流水线产出，公式被栅格化为 GIF/PNG 图片）。
//
// 主要工作：
// 1. 识别 <img> 是公式还是普通插图（看 alt 属性）。
// 2. 把公式 img 包裹成 <span class="math-inline" data-latex="...">，CSS 即可按行内/块级双轨渲染。
// 3. 给非公式 img 加 class="content-img"，由 CSS 控制响应式尺寸。
// 4. 给 <pre> 加 class="code-block"，由 CSS 加边框/等宽字体。
// 5. 给"段落只含一个公式 img"的孤立公式段加 class="formula-block"，由 CSS 居中独占一行。
//
// 用法（CLI）：
//   node optimize-formula-images.mjs <xhtml_file_or_dir>
//
// 用法（API）：
//   import { processHtml, processPath } from "./optimize-formula-images.mjs";
//   const out = processHtml(htmlStr);

import { promises as fs } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

// ---------- 公式识别 ----------

const MATH_CHARS = "=+\u2212\u00D7\u00F7\u2264\u2265\u2260\u2248\u221E\u221A\u2211\u222B\u2208\u2282\u2286\u2229\u222A\u03C3\u03BC\u03B8\u03B2\u03B1\u03BB\u03B3\u03B4\u03C0\u03C9\u03B5\u2202";

function hasMathFormula(altText) {
  if (altText == null) return false;
  const s = String(altText).trim();
  if (s === "" || s === "{%}") return false;
  // LaTeX 命令、上下标、大括号
  if (/\\[a-zA-Z]+|[\\{}_^]/.test(s)) return true;
  // 常见数学符号 / 运算符 / 希腊字母
  for (const ch of MATH_CHARS) if (s.includes(ch)) return true;
  // 短(≤4)的纯字母/数字/空白/逗号/点/分号 — 视为数学符号
  if (s.length <= 4 && /^[A-Za-z\u03B1-\u03C9\u0391-\u03A90-9\s,.;]+$/.test(s)) return true;
  // 单字母 + 1 位下标 (如 x1, N2)
  if (/^[A-Za-z]\d?$/.test(s)) return true;
  return false;
}

// ---------- HTML 转义 ----------

function htmlEscape(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function appendClass(attrStr, klass) {
  // attrStr 是开标签里 attribute 部分（含前导空格或空串），返回改写后 attribute 串
  if (/class\s*=\s*"/.test(attrStr)) {
    return attrStr.replace(/class\s*=\s*"([^"]*)"/, (_m, existing) =>
      `class="${existing} ${klass}"`);
  }
  return attrStr + ` class="${klass}"`;
}

// ---------- 主处理 ----------

export function processHtml(html) {
  // 1) 处理所有 <img .../> —— 区分公式 vs 内容图
  html = html.replace(/<img[^>]+\/>/g, (full) => {
    const altM = full.match(/alt="([^"]*)"/);
    const srcM = full.match(/src="([^"]*)"/);
    if (!srcM) return full;
    const src = srcM[1];
    const alt = altM ? altM[1] : "";

    if (hasMathFormula(alt)) {
      return (
        `<span class="math-inline" data-latex="${htmlEscape(alt)}">` +
        `<img src="${src}" alt="${htmlEscape(alt)}" class="formula-img" />` +
        `</span>`
      );
    }
    // 普通内容图：加 content-img 类
    if (/class\s*=\s*"/.test(full)) {
      return full.replace(/class\s*=\s*"([^"]*)"/, (_m, e) => `class="${e} content-img"`);
    }
    return full.replace("<img ", '<img class="content-img" ');
  });

  // 2) <pre ...> 加 code-block 类
  html = html.replace(/<pre(\s[^>]*)?>/g, (full, attrs = "") => {
    return `<pre${appendClass(attrs, "code-block")}>`;
  });

  // 3) 给"段落只含一个公式 img/span"的孤立段落加 formula-block 类
  html = html.replace(
    /<p(\s[^>]*)?>(\s*<span class="math-inline"[^>]*>.*?<\/span>\s*)<\/p>/gs,
    (_m, attrs = "", inner) => {
      return `<p${appendClass(attrs, "formula-block")}>${inner}</p>`;
    }
  );

  return html;
}

export async function processPath(target) {
  const abs = path.resolve(target);
  let st;
  try { st = await fs.stat(abs); } catch { throw new Error(`路径不存在：${abs}`); }

  let files;
  if (st.isFile()) {
    files = [abs];
  } else {
    const all = [];
    async function walk(dir) {
      const ents = await fs.readdir(dir, { withFileTypes: true });
      for (const e of ents) {
        const f = path.join(dir, e.name);
        if (e.isDirectory()) await walk(f);
        else if (/\.x?html?$/i.test(e.name)) all.push(f);
      }
    }
    await walk(abs);
    files = all;
  }

  for (const f of files) {
    const src = await fs.readFile(f, "utf8");
    const dst = processHtml(src);
    await fs.writeFile(f, dst, "utf8");
    console.log(`  \u2713 ${f}  (${src.length.toLocaleString()} \u2192 ${dst.length.toLocaleString()} bytes)`);
  }
  return files.length;
}

// ---------- CLI ----------
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const target = process.argv[2];
  if (!target) {
    console.error("用法：node optimize-formula-images.mjs <xhtml_file_or_dir>");
    process.exit(1);
  }
  processPath(target)
    .then((n) => console.log(`完成，共处理 ${n} 个文件。`))
    .catch((err) => { console.error("\u2717 失败：", err.message); process.exit(1); });
}
