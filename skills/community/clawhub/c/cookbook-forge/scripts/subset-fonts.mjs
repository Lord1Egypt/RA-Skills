#!/usr/bin/env node
// subset-fonts.mjs
//
// 从 EPUB 的 xhtml 章节中收集实际用到的字符，将 TTF 字体子集化后转成 WOFF2 嵌入。
//
// 实现策略：
//   优先使用纯 JS 的 `fonteditor-core`（ECOM 出品，支持 TTF/WOFF/WOFF2 读写 + 子集化）。
//   如果用户未安装 fonteditor-core，脚本会提示 `npm install fonteditor-core` 并给出
//   Python (fonttools+brotli) 的兜底命令作为"无 JS 方案时的 fallback"。
//
// 用法（CLI）：
//   node subset-fonts.mjs <epub_OEBPS_dir>
//
// 用法（API）：
//   import { collectChars, subsetFont } from "./subset-fonts.mjs";
//
// 会在 OEBPS_DIR/Fonts 下产出 LXGWWenKai.woff2 和 LXGWWenKaiMono.woff2。
// 前提：OEBPS_DIR/Fonts 下已有完整版的 LXGWWenKaiLite-Regular.ttf
//       和 LXGWWenKaiMonoLite-Regular.ttf。

import { promises as fs } from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);

const FONT_MAP = [
  { src: "LXGWWenKaiLite-Regular.ttf",     out: "LXGWWenKai.woff2" },
  { src: "LXGWWenKaiMonoLite-Regular.ttf", out: "LXGWWenKaiMono.woff2" },
];

export async function collectChars(oebpsDir) {
  const chars = new Set();
  const textDir = path.join(oebpsDir, "Text");
  let entries;
  try {
    entries = await fs.readdir(textDir);
  } catch {
    return chars;
  }
  for (const name of entries) {
    if (!/\.x?html?$/i.test(name)) continue;
    const txt = await fs.readFile(path.join(textDir, name), "utf8");
    const stripped = txt.replace(/<[^>]+>/g, " ");
    for (const ch of stripped) chars.add(ch);
  }
  // 兜底：ASCII 可见字符 (0x20–0x7E)
  for (let c = 0x20; c < 0x7F; c++) chars.add(String.fromCharCode(c));
  // CJK 标点
  for (let c = 0x3000; c < 0x3040; c++) chars.add(String.fromCharCode(c));
  // 全角 ASCII
  for (let c = 0xFF00; c < 0xFFF0; c++) chars.add(String.fromCharCode(c));
  return chars;
}

async function loadFonteditor() {
  try {
    return require("fonteditor-core");
  } catch {
    return null;
  }
}

export async function subsetFont(ttfPath, outPath, charSet) {
  const FE = await loadFonteditor();
  if (!FE) {
    throw new Error(
      "未安装 fonteditor-core。请执行：\n" +
        "  npm install fonteditor-core\n" +
        "或退回到 Python 方案：\n" +
        "  pip install fonttools brotli\n" +
        "  python scripts/subset_fonts.py <OEBPS_DIR>"
    );
  }
  const { Font } = FE;
  const buf = await fs.readFile(ttfPath);
  const font = Font.create(buf, { type: "ttf", subset: [...charSet].join(""), hinting: true });
  const woff2Buf = font.write({ type: "woff2" });
  await fs.writeFile(outPath, woff2Buf);
  const before = (await fs.stat(ttfPath)).size;
  const after = (await fs.stat(outPath)).size;
  console.log(`  \u2705 ${path.basename(ttfPath)} (${before.toLocaleString()} \u2192 ${after.toLocaleString()} bytes, ${(before / after).toFixed(1)}\u00D7)`);
}

export async function subsetFonts(oebpsDir) {
  const abs = path.resolve(oebpsDir);
  try {
    if (!(await fs.stat(abs)).isDirectory()) throw new Error();
  } catch {
    throw new Error(`目录不存在：${abs}`);
  }

  const chars = await collectChars(abs);
  console.log(`\u{1F4CA} 共收集 ${chars.size} 个唯一字符`);

  const fontsDir = path.join(abs, "Fonts");
  await fs.mkdir(fontsDir, { recursive: true });

  for (const { src, out } of FONT_MAP) {
    const srcPath = path.join(fontsDir, src);
    const outPath = path.join(fontsDir, out);
    try {
      await fs.access(srcPath);
    } catch {
      console.log(`  \u26A0\uFE0F  跳过，未找到 ${src}`);
      continue;
    }
    await subsetFont(srcPath, outPath, chars);
    await fs.unlink(srcPath); // EPUB 只带 WOFF2
  }
  console.log(`\n完成。子集中字体在：${fontsDir}`);
}

// ---------- CLI ----------
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const dir = process.argv[2];
  if (!dir) {
    console.error("用法：node subset-fonts.mjs <epub_OEBPS_dir>");
    process.exit(1);
  }
  subsetFonts(dir).catch((err) => {
    console.error("\u2717 失败：", err.message);
    process.exit(1);
  });
}
