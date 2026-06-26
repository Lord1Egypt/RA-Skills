#!/usr/bin/env node
/**
 * 查询文章列表。支持 routeCode / categoryId / tag / slug / publishStatus
 * 多条件组合 + 分页。
 *
 * 用途：
 * - 列出自己的草稿或已发布文章
 * - 检查 slug 是否已被占用（传 --slug 时只按 slug 查）
 * - 按分类或标签浏览
 * - 给 Claude 一个查看后端已有内容的能力
 *
 * Usage:
 *   node scripts/api/list-articles.mjs [options]
 *
 * Options:
 *   --route <BLOG|NEWS>          按路由筛选
 *   --category-id <id>           按分类 id 筛选
 *   --tag <tagName>              按标签名（不是 id）筛选
 *   --slug <slug>                按 slug 精确查（传了这个会忽略其他条件）
 *   --publish-status <0|1>       0=只看草稿，1=只看已发布，不传=全部
 *   --page <n>                   页码，默认 1
 *   --size <n>                   每页大小，默认 10
 *   --format <json|table>        输出格式，默认 json
 *   --help, -h                   显示帮助
 *
 * Env: FX_AI_API_KEY 必填
 *
 * Output (json):
 *   { list: [...], totalCount, currentPage, endPage }
 *
 * Exit: 0 success / 1 error
 */
import { apiGet, failWith, parseCliArgs, printJson } from './_lib.mjs';

const HELP = `查询 feima-lab 文章列表

Usage:
  node scripts/api/list-articles.mjs [options]

Filters (可组合):
  --route <BLOG|NEWS>       按路由筛选
  --category-id <id>        按分类 id 筛选
  --tag <tagName>           按标签名筛选
  --slug <slug>             按 slug 精确查（传了这个会忽略其他筛选）
  --publish-status <0|1>    0=草稿 / 1=已发布 / 不传=全部

Pagination:
  --page <n>                页码（默认 1）
  --size <n>                每页大小（默认 10）

Output:
  --format <json|table>     默认 json
  --help, -h                显示此帮助

典型用法：
  # 列出所有已发布博客
  node scripts/api/list-articles.mjs --route BLOG --publish-status 1 --format table

  # 判断 slug 是否已被占用
  node scripts/api/list-articles.mjs --slug 2026-04-10-xxx
  # → totalCount=0 说明未占用，>0 说明已占用

  # 查某标签下所有文章
  node scripts/api/list-articles.mjs --tag Agent --format table
`;

function validateRoute(r) {
  if (!r) return undefined;
  const upper = String(r).toUpperCase();
  if (upper !== 'BLOG' && upper !== 'NEWS') {
    failWith('invalid_argument', `--route 必须是 BLOG 或 NEWS，收到: ${r}`);
  }
  return upper;
}

function validatePublishStatus(s) {
  if (s === undefined || s === null || s === '') return undefined;
  const n = Number(s);
  if (n !== 0 && n !== 1) {
    failWith('invalid_argument', `--publish-status 必须是 0 或 1，收到: ${s}`);
  }
  return n;
}

function renderTable(pageData) {
  const rows = (pageData && pageData.list) || [];
  if (rows.length === 0) {
    return `(no articles)\ntotalCount=${pageData?.totalCount || 0}`;
  }
  const cols = [
    { key: 'id', head: 'id' },
    { key: 'slug', head: 'slug' },
    { key: 'title', head: 'title' },
    { key: 'publishStatusName', head: 'status' },
    { key: 'categoryName', head: 'category' },
    { key: 'author', head: 'author' },
    { key: 'updateTime', head: 'updated' },
  ];
  const widths = cols.map(c =>
    Math.max(c.head.length, ...rows.map(r => String(r[c.key] ?? '').length))
  );
  const fmt = (cells) =>
    cells.map((c, i) => String(c ?? '').padEnd(widths[i])).join('  ');
  const header = fmt(cols.map(c => c.head));
  const sep = widths.map(w => '-'.repeat(w)).join('  ');
  const lines = rows.map(r => fmt(cols.map(c => r[c.key] ?? '')));
  return (
    [header, sep, ...lines].join('\n') +
    `\n\n页 ${pageData.currentPage} / 共 ${pageData.totalCount} 条` +
    (pageData.endPage ? '（已是最后一页）' : '')
  );
}

async function main() {
  const args = parseCliArgs(process.argv.slice(2));
  if (args.help) { process.stdout.write(HELP); return; }

  const query = {};
  const route = validateRoute(args.route);
  if (route) query.routeCode = route;
  if (args['category-id']) query.categoryId = args['category-id'];
  if (args.tag) query.tag = args.tag;
  if (args.slug) query.slug = args.slug;
  const ps = validatePublishStatus(args['publish-status']);
  if (ps !== undefined) query.publishStatus = ps;
  query.pageNum = args.page || 1;
  query.pageSize = args.size || 10;

  const data = await apiGet('/content/api/article/list', query);
  // data is CmsPageData<ArticleListResult>: { list, totalCount, currentPage, endPage }
  const pageData = data || { list: [], totalCount: 0, currentPage: 1, endPage: true };

  if (args.format === 'table') {
    process.stdout.write(renderTable(pageData) + '\n');
  } else {
    printJson(pageData);
  }
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
