#!/usr/bin/env node
/**
 * 保存（创建/更新）文章到 feima-lab 后端。
 *
 * 工作流程：
 *   1. 读 posts/<slug>/meta.json 和 article.mdx
 *   2. 如果 meta.categoryId 为空，用 meta.category 名字查 list-categories
 *      得到对应 id；找不到报错并列出可选分类
 *   3. 如果 meta.coverImageUrl 为空且 meta.coverImage 是本地路径，
 *      自动上传该图片，并把返回的 URL 写回 meta.coverImageUrl
 *   3b. 扫描 article.mdx 中所有 ./images/ 本地引用，逐张上传到 OSS，
 *       在内存中替换为远程 URL（磁盘上的 mdx 文件保持本地路径不变）
 *   4. 构造 SaveArticleRequest 并 POST /content/api/article/save
 *   5. 把返回的 articleId 写回 meta.publish.remote_id
 *
 * v1 限制（有意简化）：
 * - tags: 完全忽略 meta.tags 字段，不上传 tagIds。v2 再加。
 * - subCategory: 不上传（API 无对应字段）
 * - contentHtml: 不传（服务端自己渲染 markdown）
 *
 * Usage:
 *   node scripts/api/save-article.mjs --post-dir <path-to-posts/slug>
 *   node scripts/api/save-article.mjs --post-dir <path> --dry-run
 *
 * Env:
 *   FX_AI_API_KEY   必填
 *
 * Output (json to stdout on success):
 *   { "articleId": 123, "slug": "...", "mode": "create|update" }
 *
 * Exit: 0 success / 1 error (JSON to stderr)
 */
import { readFile, stat } from 'node:fs/promises';
import { resolve, join, isAbsolute } from 'node:path';
import {
  apiGet,
  apiPostJson,
  apiPostMultipart,
  failWith,
  loadMeta,
  parseCliArgs,
  printJson,
  saveMeta,
} from './_lib.mjs';

const HELP = `保存文章到 feima-lab 后端

Usage:
  node scripts/api/save-article.mjs --post-dir <path> [--dry-run]

Options:
  --post-dir <path>   posts/<slug>/ 目录路径（必填）
  --dry-run           只打印将要发送的请求体，不实际调用
  --help, -h          显示此帮助

前置条件：
  1. posts/<slug>/meta.json 已包含 title / description / author / category / slug
  2. posts/<slug>/article.mdx 已存在（作为 contentMarkdown 上传）
  3. 封面图本地路径 meta.coverImage（./images/xxx）会自动上传到 OSS

v1.3 自动逻辑：
  - categoryId 空 → 按 meta.route (BLOG/NEWS) + meta.category 名字查 id
  - coverImageUrl 空 → 自动上传 coverImage 本地文件
  - 正文图片闭环：扫描 article.mdx 中所有 ./images/ 引用，逐张上传 OSS，替换为远程 URL
  - tags 数组会闭环处理：查已有 tag → 缺失的自动建 → 收集 tagIds 传给 save
  - tint 默认 bg-tint-blue（必须带 bg- 前缀）
  - 返回的 articleId / tagIds 写回 meta.json（publish.remote_id / publish.last_saved_tag_ids）

Output (json):
  { "articleId": 123, "slug": "2026-04-09-x", "mode": "create", "tagIds": [1,3] }

Auth:
  export FX_AI_API_KEY=<your-key>（必须是 internal 类型的 key）
`;

/**
 * Resolve meta.category (name) to a categoryId by listing from the backend.
 * If meta.route is set, only categories matching that route are considered.
 * Exits with invalid_meta on mismatch.
 */
async function resolveCategoryId(meta) {
  if (meta.categoryId && Number.isInteger(meta.categoryId)) {
    return meta.categoryId;
  }
  if (!meta.category || !String(meta.category).trim()) {
    failWith(
      'invalid_meta',
      'meta.json 缺少 category 或 categoryId 字段',
      '在 meta.json 填 `"category": "技术探索"`（名字）或 `"categoryId": 5`（数字）'
    );
  }
  const route = meta.route ? String(meta.route).toUpperCase() : undefined;
  const list = await apiGet('/content/api/category/list', route ? { routeCode: route } : undefined);
  const rows = Array.isArray(list) ? list : [];
  const match = rows.find(r => r.categoryName === meta.category);
  if (!match) {
    const available = rows.map(r => `  - ${r.categoryName} (id=${r.id}, route=${r.routeCode || '?'})`).join('\n');
    failWith(
      'invalid_meta',
      `meta.category "${meta.category}" 在后端分类列表中不存在${route ? `（route=${route}）` : ''}`,
      `可选分类：\n${available || '  (后端返回空列表——请先在后台新建分类)'}`
    );
  }
  return match.id;
}

/**
 * Resolve meta.tags (string array) to a numeric tagIds array.
 *
 * Flow:
 *   1. If meta.tags is empty → return []
 *   2. GET /content/api/tag/list once to get existing tags
 *   3. For each name in meta.tags:
 *      - if exists → use existing id
 *      - if missing → POST /content/api/tag/save to create, use new id
 *   4. Return the collected tagIds (in the same order as meta.tags)
 *
 * Exits with invalid_meta if any tagName > 64 chars.
 */
async function resolveTagIds(meta) {
  const raw = Array.isArray(meta.tags) ? meta.tags : [];
  const names = raw
    .map(t => (t == null ? '' : String(t).trim()))
    .filter(t => t.length > 0);
  if (names.length === 0) return [];

  for (const n of names) {
    if (n.length > 64) {
      failWith(
        'invalid_meta',
        `meta.tags 中的标签名 "${n.slice(0, 20)}..." 超过 64 字符上限`,
        '截断或改名后重试'
      );
    }
  }

  // Fetch existing tags once
  const existingList = await apiGet('/content/api/tag/list');
  const existing = new Map(); // lowercased name → { id, tagName }
  if (Array.isArray(existingList)) {
    for (const row of existingList) {
      if (row && row.tagName) {
        existing.set(String(row.tagName).toLowerCase(), { id: row.id, tagName: row.tagName });
      }
    }
  }

  const tagIds = [];
  for (const name of names) {
    const hit = existing.get(name.toLowerCase());
    if (hit) {
      tagIds.push(hit.id);
      continue;
    }
    // Create new
    process.stderr.write(`[tags] 创建新标签: ${name}\n`);
    const newId = await apiPostJson('/content/api/tag/save', { tagName: name });
    if (newId == null) {
      failWith('api_error', `创建标签 "${name}" 失败：后端返回 id 为 null`);
    }
    tagIds.push(Number(newId));
    // Cache it so duplicates in the same meta.tags array don't re-create
    existing.set(name.toLowerCase(), { id: Number(newId), tagName: name });
  }

  return tagIds;
}

/**
 * If meta.coverImageUrl is empty AND meta.coverImage is a local path,
 * upload the local file and return the remote url. Otherwise return
 * meta.coverImageUrl as-is (may be empty string).
 *
 * Mutates meta.coverImageUrl on successful upload.
 */
async function resolveCoverImageUrl(meta, postDir) {
  if (meta.coverImageUrl && String(meta.coverImageUrl).trim()) {
    return meta.coverImageUrl;
  }
  const local = meta.coverImage;
  if (!local || !String(local).trim()) {
    return ''; // no cover image at all — that's fine, it's optional
  }
  // Normalize local path (relative to postDir)
  const absLocal = isAbsolute(local) ? local : resolve(postDir, local);
  try {
    await stat(absLocal);
  } catch {
    failWith(
      'file_not_found',
      `meta.coverImage 指向的本地文件不存在: ${absLocal}`,
      '先跑 scripts/image-localize.mjs 拷贝图片到 posts/<slug>/images/，或手动填 meta.coverImageUrl 为远程 URL。'
    );
  }
  process.stderr.write(`[upload] 自动上传封面图: ${absLocal}\n`);
  const result = await apiPostMultipart('/content/api/upload', absLocal);
  if (!result || !result.url) {
    failWith('api_error', '封面图上传响应缺少 url 字段', `原始响应: ${JSON.stringify(result)}`);
  }
  meta.coverImageUrl = result.url;
  return result.url;
}

/**
 * Scan article MDX content for local ./images/ references,
 * upload each unique file to OSS, and replace paths with remote URLs.
 *
 * Matched patterns (all share the ./images/ prefix):
 *   - Markdown:   ![alt](./images/xxx.png)
 *   - JSX attr:   src="./images/xxx.png"  poster="./images/xxx.png"
 *   - JSON prop:  "src":"./images/xxx.png"
 *
 * Only modifies the in-memory content — article.mdx on disk keeps local paths.
 */
async function resolveContentImages(content, postDir, dryRun = false) {
  const localImageRegex = /\.\/images\/[^\s"')\]},]+/g;
  const refs = [...new Set(content.match(localImageRegex) || [])];
  if (refs.length === 0) return content;

  process.stderr.write(`[upload] 扫描到 ${refs.length} 张正文图片需要上传\n`);

  if (dryRun) {
    for (const r of refs) process.stderr.write(`[dry-run]   ${r}\n`);
    return content;
  }

  const pathToUrl = new Map();
  for (const localRef of refs) {
    const absPath = resolve(postDir, localRef);
    try {
      await stat(absPath);
    } catch {
      failWith(
        'file_not_found',
        `正文图片不存在: ${absPath}（引用路径: ${localRef}）`,
        '先跑 scripts/image-localize.mjs 确保所有图片已本地化到 images/ 目录。'
      );
    }
    process.stderr.write(`[upload] 上传正文图片: ${localRef}\n`);
    const result = await apiPostMultipart('/content/api/upload', absPath);
    if (!result || !result.url) {
      failWith('api_error', `正文图片上传响应缺少 url 字段: ${localRef}`, `原始响应: ${JSON.stringify(result)}`);
    }
    pathToUrl.set(localRef, result.url);
  }

  let resolved = content;
  for (const [localRef, remoteUrl] of pathToUrl) {
    resolved = resolved.split(localRef).join(remoteUrl);
  }
  process.stderr.write(`[upload] 正文图片全部上传完成，共 ${pathToUrl.size} 张\n`);
  return resolved;
}

async function loadArticleMarkdown(postDir) {
  const mdxPath = join(postDir, 'article.mdx');
  try {
    return await readFile(mdxPath, 'utf8');
  } catch (e) {
    if (e.code === 'ENOENT') {
      failWith(
        'file_not_found',
        `article.mdx 不存在: ${mdxPath}`,
        '先写 article.mdx 再调用 save-article。'
      );
    }
    throw e;
  }
}

function validateRequiredMetaFields(meta) {
  const required = ['slug', 'title', 'description', 'author'];
  const missing = required.filter(k => !meta[k] || !String(meta[k]).trim());
  if (missing.length > 0) {
    failWith(
      'invalid_meta',
      `meta.json 缺少必填字段: ${missing.join(', ')}`,
      '补全后重试。参考 references/meta-schema.md'
    );
  }
}

async function main() {
  const args = parseCliArgs(process.argv.slice(2));
  if (args.help) { process.stdout.write(HELP); return; }
  if (!args['post-dir']) {
    failWith('invalid_argument', '缺少 --post-dir 参数', HELP);
  }

  const postDir = resolve(String(args['post-dir']));
  const meta = await loadMeta(postDir);
  validateRequiredMetaFields(meta);

  const categoryId = await resolveCategoryId(meta);
  const coverImageUrl = await resolveCoverImageUrl(meta, postDir);
  const rawMarkdown = await loadArticleMarkdown(postDir);
  const contentMarkdown = await resolveContentImages(rawMarkdown, postDir, !!args['dry-run']);
  const tagIds = await resolveTagIds(meta);

  const existingRemoteId = meta.publish?.remote_id;
  const mode = existingRemoteId ? 'update' : 'create';

  const request = {
    articleId: existingRemoteId || null,
    categoryId,
    slug: meta.slug,
    title: meta.title,
    description: meta.description,
    coverImageUrl,
    contentMarkdown,
    author: meta.author,
    tint: meta.tint || 'bg-tint-blue',
    sortOrder: meta.sortOrder ?? null,
    tagIds: tagIds.length > 0 ? tagIds : null,
  };

  if (args['dry-run']) {
    process.stderr.write('[dry-run] 将要发送的请求体：\n');
    printJson(request);
    return;
  }

  process.stderr.write(
    `[save] mode=${mode} slug=${meta.slug} categoryId=${categoryId} tagIds=[${tagIds.join(',')}]\n`
  );
  const articleId = await apiPostJson('/content/api/article/save', request);
  if (articleId == null) {
    failWith('api_error', '后端返回 articleId 为 null', '检查后端日志');
  }

  // Write back to meta.json
  meta.categoryId = categoryId;
  meta.coverImageUrl = coverImageUrl;
  meta.publish = meta.publish || {};
  meta.publish.remote_id = Number(articleId);
  meta.publish.last_saved_at = new Date().toISOString();
  meta.publish.last_saved_tag_ids = tagIds.length > 0 ? tagIds : null;
  await saveMeta(postDir, meta);

  printJson({
    articleId: Number(articleId),
    slug: meta.slug,
    mode,
    tagIds,
  });
}

main().catch((e) => {
  process.stderr.write(JSON.stringify({
    status: 'error',
    error_type: 'unexpected',
    message: e.message,
    stack: e.stack,
  }) + '\n');
  process.exit(1);
});
