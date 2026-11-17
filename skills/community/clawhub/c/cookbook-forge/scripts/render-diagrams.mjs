#!/usr/bin/env node
// render-diagrams.mjs
// 扫描 mdx/*.mdx 中所有 ```mermaid / ```plantuml 代码块，
// 调用 kroki.io 渲染为 SVG，写入 mdx/public/figures/diagram-<hash>.svg，
// 同时把源码保存到 mdx/public/diagrams-src/diagram-<hash>.<ext>（保留原文件便于修改），
// 再把原 mdx 里的代码块原地替换为 ![caption](/figures/diagram-<hash>.svg) 图片语法。
//
// 用法：
//   node scripts/render-diagrams.mjs            # 扫描 cwd/mdx
//   node scripts/render-diagrams.mjs <bookDir>  # 指定项目根
//
// 特性：
//   - 幂等：已有 SVG 不重复请求（按 hash 命中缓存）
//   - 不修改用户手写的 .mmd/.puml 源文件（只把从 mdx 中抽取的代码块写入 diagrams-src/）
//   - 同时渲染 mdx/public/diagrams-src/*.puml / *.mmd 独立源文件（之前的用法）
import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  extractDiagramBlocks,
  renderAll,
  replaceBlocks,
} from "./lib/diagram-renderer.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const bookRoot = path.resolve(process.argv[2] || process.cwd());
const mdxDir = path.join(bookRoot, "mdx");

console.log("=== Diagram Renderer (mermaid/plantuml → kroki SVG) ===\n");
console.log("book root:", bookRoot);

let totalBlocks = 0;
let totalFiles = 0;

// 1) 处理 mdx 文件里的内嵌代码块
const mdxFiles = (await fs.readdir(mdxDir)).filter((f) => f.endsWith(".mdx"));
for (const f of mdxFiles) {
  const fp = path.join(mdxDir, f);
  const raw = await fs.readFile(fp, "utf8");
  const blocks = extractDiagramBlocks(raw);
  if (blocks.length === 0) continue;

  console.log(`\n• ${f}: 发现 ${blocks.length} 个图表代码块`);
  const results = await renderAll(bookRoot, blocks, {
    onProgress: (msg) => console.log("   ", msg),
  });
  const newBody = replaceBlocks(raw, results);

  if (newBody !== raw) {
    await fs.writeFile(fp, newBody, "utf8");
    totalFiles++;
  }
  totalBlocks += blocks.length;
}

// 2) 处理 mdx/public/diagrams-src/ 下的独立 .puml / .mmd 文件（与历史 kroki-render.mjs 用法兼容）
const srcDir = path.join(mdxDir, "public", "diagrams-src");
const figDir = path.join(mdxDir, "public", "figures");
await fs.mkdir(figDir, { recursive: true });
try {
  const standalone = (await fs.readdir(srcDir)).filter((f) =>
    /\.(puml|plantuml|mmd|mermaid)$/i.test(f)
  );
  const typeMap = { puml: "plantuml", plantuml: "plantuml", mmd: "mermaid", mermaid: "mermaid" };
  for (const fn of standalone) {
    const body = await fs.readFile(path.join(srcDir, fn), "utf8");
    const ext = path.extname(fn).slice(1).toLowerCase();
    const type = typeMap[ext];
    if (!type) continue;
    // 独立文件：hash 基于文件内容，输出 <basename>.svg
    const outName = fn.replace(/\.[^.]+$/, "") + ".svg";
    const outPath = path.join(figDir, outName);
    try {
      await fs.access(outPath);
      console.log(`\n• standalone ${fn}: cache hit (${outName})`);
    } catch {
      const { default: kry } = await import("./lib/diagram-renderer.mjs");
      // 直接复用 kroki 逻辑：encode + fetch
      const zlib = await import("node:zlib");
      const https = await import("node:https");
      const deflated = zlib.deflateSync(body, { level: 9 });
      const b64 = deflated.toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
      const url = `https://kroki.io/${type}/svg/${b64}`;
      await new Promise((resolve, reject) => {
        const req = https.request(url, { method: "GET", headers: { "User-Agent": "cookbook-forge" } }, (res) => {
          if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}`));
          const chunks = [];
          res.on("data", (c) => chunks.push(c));
          res.on("end", async () => {
            await fs.writeFile(outPath, Buffer.concat(chunks));
            console.log(`\n• standalone ${fn}: rendered → ${outName}`);
            resolve();
          });
        });
        req.on("error", reject);
        req.setTimeout(30000, () => req.destroy(new Error("timeout")));
        req.end();
      });
    }
    totalBlocks++;
  }
} catch {
  // diagrams-src 目录可能不存在，忽略
}

console.log(`\n━━━ 完成 ━━━`);
console.log(`处理 ${mdxFiles.length} 个 MDX 文件，替换 ${totalBlocks} 个图表代码块，修改 ${totalFiles} 个 MDX 文件。`);
console.log(`SVG 输出目录: ${figDir}`);
console.log(`源码保留目录: ${srcDir}`);
