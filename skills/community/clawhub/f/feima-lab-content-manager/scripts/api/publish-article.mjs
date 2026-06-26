#!/usr/bin/env node
/**
 * 发布已保存的文章（草稿 → 已发布）。
 *
 * 必须先跑过 save-article.mjs，meta.json 里会有 publish.remote_id；
 * 本脚本从 meta 读 id 然后调 POST /content/api/article/publish/{id}。
 *
 * 也支持直接传 --id 或 --slug（slug 模式会先调 by-slug 查 id）。
 *
 * Usage:
 *   node scripts/api/publish-article.mjs --post-dir <path>
 *   node scripts/api/publish-article.mjs --id <articleId>
 *   node scripts/api/publish-article.mjs --slug <slug>
 *
 * Env:
 *   FX_AI_API_KEY   必填
 *
 * Output (json): { "articleId": 123, "status": "published", "slug": "..." }
 *
 * Exit: 0 success / 1 error (JSON to stderr)
 */
import { resolve } from 'node:path';
import {
  apiGet,
  apiPostJson,
  failWith,
  loadMeta,
  parseCliArgs,
  printJson,
  saveMeta,
} from './_lib.mjs';

const HELP = `发布文章（草稿 → 已发布）

Usage:
  node scripts/api/publish-article.mjs --post-dir <path>   # 从 meta.json 读 remote_id
  node scripts/api/publish-article.mjs --id <articleId>    # 直接指定 id
  node scripts/api/publish-article.mjs --slug <slug>       # 先按 slug 查 id 再发布

Options:
  --post-dir <path>   posts/<slug>/ 目录（需要 meta.publish.remote_id 已填）
  --id <number>       后端 articleId
  --slug <slug>       按 slug 查询后再发布
  --help, -h          显示此帮助

前置条件：
  通常先跑 save-article.mjs 得到 remote_id，再跑本脚本发布。
  首次保存+发布的典型流程：
    node scripts/api/save-article.mjs   --post-dir posts/2026-04-09-xxx
    node scripts/api/publish-article.mjs --post-dir posts/2026-04-09-xxx

Output (json):
  { "articleId": 123, "status": "published", "slug": "..." }

Auth:
  export FX_AI_API_KEY=<your-key>
`;

async function resolveArticleIdAndPostDir(args) {
  // Priority 1: --id
  if (args.id) {
    const id = Number(args.id);
    if (!Number.isInteger(id) || id <= 0) {
      failWith('invalid_argument', `--id 不是合法整数: ${args.id}`);
    }
    return { articleId: id, postDir: null, slug: null };
  }

  // Priority 2: --post-dir
  if (args['post-dir']) {
    const postDir = resolve(String(args['post-dir']));
    const meta = await loadMeta(postDir);
    const id = meta.publish?.remote_id;
    if (!id || !Number.isInteger(id)) {
      failWith(
        'invalid_meta',
        'meta.publish.remote_id 未填。说明这篇文章还没 save 过。',
        '先跑：node scripts/api/save-article.mjs --post-dir ' + postDir
      );
    }
    return { articleId: id, postDir, slug: meta.slug };
  }

  // Priority 3: --slug
  if (args.slug) {
    const slug = String(args.slug);
    const data = await apiGet(`/content/api/article/by-slug/${encodeURIComponent(slug)}`);
    if (!data || !data.id) {
      failWith('not_found', `slug "${slug}" 在后端不存在`, '检查拼写或先 save。');
    }
    return { articleId: data.id, postDir: null, slug };
  }

  failWith('invalid_argument', '需要 --post-dir / --id / --slug 之一', HELP);
}

async function main() {
  const args = parseCliArgs(process.argv.slice(2));
  if (args.help) { process.stdout.write(HELP); return; }

  const { articleId, postDir, slug } = await resolveArticleIdAndPostDir(args);

  process.stderr.write(`[publish] articleId=${articleId} slug=${slug || '(unknown)'}\n`);
  await apiPostJson(`/content/api/article/publish/${articleId}`, null);

  // If we have a postDir, update meta.json publish status
  if (postDir) {
    const meta = await loadMeta(postDir);
    meta.publish = meta.publish || {};
    meta.publish.status = 'published';
    meta.publish.published_at = new Date().toISOString();
    meta.publish.published_slug = meta.slug;
    await saveMeta(postDir, meta);
  }

  printJson({
    articleId,
    status: 'published',
    slug: slug || null,
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
