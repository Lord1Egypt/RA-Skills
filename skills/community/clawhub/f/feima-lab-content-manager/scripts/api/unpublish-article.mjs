#!/usr/bin/env node
/**
 * 取消发布一篇已发布的文章（回到草稿状态）。
 *
 * 语义（来自后端文档）：
 * - 把 publishStatus 从 1 改回 0
 * - publishTime 保留不变（不会清空）
 * - 前端展示页立即看不到这篇文章
 *
 * Usage:
 *   node scripts/api/unpublish-article.mjs --post-dir <path>
 *   node scripts/api/unpublish-article.mjs --id <articleId>
 *   node scripts/api/unpublish-article.mjs --slug <slug>
 *
 * Env: FX_AI_API_KEY 必填
 *
 * Output (json): { "articleId": 123, "status": "draft", "slug": "..." }
 *
 * Exit: 0 success / 1 error
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

const HELP = `取消发布文章（已发布 → 草稿）

Usage:
  node scripts/api/unpublish-article.mjs --post-dir <path>   # 从 meta.json 读 remote_id
  node scripts/api/unpublish-article.mjs --id <articleId>    # 直接指定 id
  node scripts/api/unpublish-article.mjs --slug <slug>       # 按 slug 查 id 再取消

Options:
  --post-dir <path>   posts/<slug>/ 目录
  --id <number>       后端 articleId
  --slug <slug>       按 slug 查询后取消
  --help, -h          显示此帮助

语义：
  - publishStatus 从 1 改回 0
  - publishTime 保留不变（不会清空）
  - 前端展示页立即看不到这篇

Output (json):
  { "articleId": 123, "status": "draft", "slug": "..." }
`;

async function resolveArticleId(args) {
  if (args.id) {
    const id = Number(args.id);
    if (!Number.isInteger(id) || id <= 0) {
      failWith('invalid_argument', `--id 不是合法整数: ${args.id}`);
    }
    return { articleId: id, postDir: null, slug: null };
  }

  if (args['post-dir']) {
    const postDir = resolve(String(args['post-dir']));
    const meta = await loadMeta(postDir);
    const id = meta.publish?.remote_id;
    if (!id || !Number.isInteger(id)) {
      failWith(
        'invalid_meta',
        'meta.publish.remote_id 未填。这篇文章还没 save 过。',
        '先跑 save-article.mjs 再取消发布（虽然没意义，但流程需要）。'
      );
    }
    return { articleId: id, postDir, slug: meta.slug };
  }

  if (args.slug) {
    const slug = String(args.slug);
    const data = await apiGet(`/content/api/article/by-slug/${encodeURIComponent(slug)}`);
    if (!data || !data.id) {
      failWith('not_found', `slug "${slug}" 在后端不存在`, '检查拼写。');
    }
    return { articleId: data.id, postDir: null, slug };
  }

  failWith('invalid_argument', '需要 --post-dir / --id / --slug 之一', HELP);
}

async function main() {
  const args = parseCliArgs(process.argv.slice(2));
  if (args.help) { process.stdout.write(HELP); return; }

  const { articleId, postDir, slug } = await resolveArticleId(args);

  process.stderr.write(`[unpublish] articleId=${articleId} slug=${slug || '(unknown)'}\n`);
  await apiPostJson(`/content/api/article/unpublish/${articleId}`, null);

  if (postDir) {
    const meta = await loadMeta(postDir);
    meta.publish = meta.publish || {};
    meta.publish.status = 'draft';
    // 不清 published_at / published_slug —— 和后端 publishTime 不清的语义对齐
    await saveMeta(postDir, meta);
  }

  printJson({
    articleId,
    status: 'draft',
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
