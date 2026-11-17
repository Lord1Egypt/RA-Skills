// scripts/lib/diagram-renderer.mjs
// 统一图表渲染 pipeline：
//   - 从 MDX 正文中提取 ```mermaid / ```plantuml 代码块
//   - 调用 https://kroki.io 渲染为 SVG（离线时跳过并返回 placeholder）
//   - 写入 mdx/public/figures/diagram-<hash>.svg
//   - 同时保留源码到 mdx/public/diagrams-src/diagram-<hash>.<ext>（供作者二次修改）
//   - 返回替换映射 { start, end, alt, svgFileName }，供各格式转换器把代码块替换为图片引用
import { promises as fs } from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import zlib from "node:zlib";
import https from "node:https";

const KROKI_TYPE_MAP = {
  mermaid: "mermaid",
  plantuml: "plantuml",
  puml: "plantuml",
  nomnoml: "nomnoml",
  svgbob: "svgbob",
  erd: "erd",
  ditaa: "ditaa",
  bytefield: "bytefield",
  seqdiag: "seqdiag",
  actdiag: "actdiag",
  nwdiag: "nwdiag",
  packetdiag: "packetdiag",
  rackdiag: "rackdiag",
};

const EXT_MAP = {
  mermaid: "mmd",
  plantuml: "puml",
  puml: "puml",
};

/**
 * 从 MDX 正文里抽取 ```mermaid / ```plantuml 围栏代码块。
 * 返回一个数组：{ lang, body, index, match, hash, svgFile, srcFile, caption }
 *   - index: 匹配在原文中的起始下标
 *   - match: 整个 ```...``` 匹配文本（含首尾 ``` 行）
 *   - hash: 内容稳定 hash（前 10 位 hex）
 *   - caption: 代码块下方紧邻的 "> ..." 引用/标题文本（如果有），否则 fallback 到 "<lang> diagram"
 */
export function extractDiagramBlocks(mdxBody) {
  const blocks = [];
  // 围栏代码块（支持 ``` 或 ~~~），语言标记 = mermaid / plantuml / puml
  const re = /(^|\n)(```|~~~)(mermaid|plantuml|puml)\s*\n([\s\S]*?)\n\2(\s*\n)?/g;
  let m;
  while ((m = re.exec(mdxBody)) !== null) {
    const lang = m[3];
    const body = m[4].replace(/\r\n/g, "\n");
    const fullMatch = m[0].replace(/^\n/, ""); // 去掉前导换行（匹配组1）
    const hash = crypto.createHash("sha1").update(`${lang}:${body}`).digest("hex").slice(0, 10);
    // 尝试在匹配结束位置后找一个形如 "> xxx" 或 "图 N-M xxx" 的标题
    let caption = null;
    const after = mdxBody.slice(m.index + m[0].length);
    const capMatch = after.match(/^\s*(?:>\s*([^\n]+)|(图[\s\S]*?))\s*\n/);
    if (capMatch) {
      caption = (capMatch[1] || capMatch[2] || "").trim().replace(/^图\s*/, "");
    }
    blocks.push({
      lang,
      body,
      index: m.index + (m[0].startsWith("\n") ? 1 : 0),
      match: fullMatch,
      hash,
      caption: caption || `${lang} diagram`,
    });
  }
  return blocks;
}

function krokiEncode(text) {
  const deflated = zlib.deflateSync(text, { level: 9 });
  return deflated.toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

function krokiFetch(type, fmt, encoded) {
  const url = `https://kroki.io/${type}/${fmt}/${encoded}`;
  return new Promise((resolve, reject) => {
    const req = https.request(url, { method: "GET", headers: { "User-Agent": "cookbook-forge" } }, (res) => {
      if (res.statusCode !== 200) {
        let body = "";
        res.on("data", (c) => (body += c));
        res.on("end", () => reject(new Error(`kroki HTTP ${res.statusCode}: ${body.slice(0, 300)}`)));
        return;
      }
      const chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => resolve(Buffer.concat(chunks)));
    });
    req.on("error", reject);
    req.setTimeout(30000, () => req.destroy(new Error("kroki request timeout")));
    req.end();
  });
}

/**
 * 渲染所有图表到 SVG，并拷贝/写入到 mdx/public/figures 与 mdx/public/diagrams-src。
 * 已存在的 SVG 不重复请求（按 hash 命中缓存）。
 *
 * @param {string} bookRoot  项目根（包含 mdx/ 子目录）
 * @param {Array} blocks     extractDiagramBlocks() 返回的 blocks 数组
 * @returns {Promise<Array>} 同 blocks 数组，每项增加 { svgFileName, svgAbsPath, srcAbsPath, rendered:bool, error?:string }
 */
export async function renderAll(bookRoot, blocks, { onProgress } = {}) {
  const figDir = path.join(bookRoot, "mdx", "public", "figures");
  const srcDir = path.join(bookRoot, "mdx", "public", "diagrams-src");
  await fs.mkdir(figDir, { recursive: true });
  await fs.mkdir(srcDir, { recursive: true });

  const results = [];
  for (const b of blocks) {
    const type = KROKI_TYPE_MAP[b.lang];
    const ext = EXT_MAP[b.lang] || b.lang;
    const svgFileName = `diagram-${b.hash}.svg`;
    const srcFileName = `diagram-${b.hash}.${ext}`;
    const svgAbsPath = path.join(figDir, svgFileName);
    const srcAbsPath = path.join(srcDir, srcFileName);
    const r = { ...b, svgFileName, svgAbsPath, srcAbsPath, rendered: false };

    // 始终写源码（方便作者修改后重渲染）
    await fs.writeFile(srcAbsPath, b.body, "utf8");

    try {
      let buf;
      try {
        buf = await fs.readFile(svgAbsPath);
        if (onProgress) onProgress(`cache ${svgFileName}`);
      } catch {
        const encoded = krokiEncode(b.body);
        buf = await krokiFetch(type, "svg", encoded);
        await fs.writeFile(svgAbsPath, buf);
        if (onProgress) onProgress(`rendered ${svgFileName} (${buf.length} bytes)`);
      }
      r.rendered = true;
    } catch (e) {
      r.error = e.message;
      if (onProgress) onProgress(`FAIL ${svgFileName}: ${e.message}`);
      // 写一个占位 SVG（含错误信息），下游格式不会因网络挂掉而崩
      const placeholder = `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="80" viewBox="0 0 600 80">
  <rect width="600" height="80" fill="#fff5f5" stroke="#fca5a5"/>
  <text x="20" y="30" font-family="sans-serif" font-size="14" fill="#991b1b">[diagram render failed] ${b.lang}</text>
  <text x="20" y="55" font-family="monospace" font-size="11" fill="#7f1d1d">${String(e.message).replace(/&/g,"&amp;").replace(/</g,"&lt;").slice(0,100)}</text>
</svg>`;
      await fs.writeFile(svgAbsPath, placeholder, "utf8");
    }
    results.push(r);
  }
  return results;
}

/**
 * 把 blocks 里的代码块从 mdxBody 中替换为 Markdown 图片语法。
 *
 * @param {string} mdxBody  原始 MDX 正文
 * @param {Array} results  renderAll() 返回的结果数组
 * @param {(r) => string} imgRef  生成图片 Markdown 的函数。默认：`![<lang> diagram](/figures/<svgFileName>)`
 *                                注意：替换后会在末尾补两个换行，保证与后续段落分隔。
 */
export function replaceBlocks(mdxBody, results, imgRef) {
  imgRef =
    imgRef ||
    ((r) => `![${r.lang} diagram](/figures/${r.svgFileName})`);
  // 按 index 倒序替换，避免偏移
  const sorted = [...results].sort((a, b) => b.index - a.index);
  let out = mdxBody;
  for (const r of sorted) {
    out =
      out.slice(0, r.index) +
      imgRef(r) +
      "\n\n" +
      out.slice(r.index + r.match.length);
  }
  return out;
}
