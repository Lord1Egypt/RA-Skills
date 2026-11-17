// scripts/lib/mdx-utils.mjs
// 共享的 MDX frontmatter 解析工具，被 lmdx2tex.mjs / lbuild-epub.mjs 等复用。

export function normalizeNewlines(raw) {
  return String(raw).replace(/\r\n/g, "\n");
}

/**
 * 解析 MDX frontmatter。支持：
 *   key: value           简单键值
 *   key: "quoted value"  带引号（自动去引号）
 *   key:                 列表，后跟 "  - item" 行，收集为数组
 * @param {string} raw  MDX 原文
 * @returns {{ title: string, slug: string, fm: Record<string, string|string[]>, body: string }}
 */
export function parseFrontmatter(raw) {
  const normalized = normalizeNewlines(raw);
  const m = normalized.match(/^---\n([\s\S]*?)\n---\n/);
  if (!m) return { title: "Chapter", slug: "chapter", fm: {}, body: normalized };

  const fm = {};
  const lines = m[1].split("\n");
  let currentKey = null;
  for (const line of lines) {
    const kv = line.match(/^(\w+):\s*(.*)$/);
    if (kv) {
      const key = kv[1];
      const val = kv[2].trim();
      currentKey = key;
      if (val === "" || val === "[]") {
        fm[key] = [];
      } else {
        fm[key] = val.replace(/^["']|["']$/g, "");
      }
      continue;
    }
    const item = line.match(/^\s+-\s+(.+)$/);
    if (item && currentKey) {
      if (!Array.isArray(fm[currentKey])) fm[currentKey] = [];
      fm[currentKey].push(item[1].trim().replace(/^["']|["']$/g, ""));
    }
  }

  return {
    title: (typeof fm.title === "string" && fm.title) || "Chapter",
    slug: (typeof fm.slug === "string" && fm.slug) || "chapter",
    fm,
    body: normalized.slice(m[0].length),
  };
}
