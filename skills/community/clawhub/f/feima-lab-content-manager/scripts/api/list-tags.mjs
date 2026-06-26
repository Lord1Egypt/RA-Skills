#!/usr/bin/env node
/**
 * 列出 feima-lab 后端所有启用的标签。
 *
 * 用途：
 * - save-article 的 tags 闭环内部会调
 * - 用户想看"后端已有哪些标签可以复用"
 *
 * Usage:
 *   node scripts/api/list-tags.mjs [--format json|table]
 *
 * Env: FX_AI_API_KEY 必填
 *
 * Output (json):
 *   [ { "id": 1, "tagName": "Agent" }, ... ]
 *
 * Exit: 0 success / 1 error
 */
import { apiGet, parseCliArgs, printJson } from './_lib.mjs';

const HELP = `列出 feima-lab 标签

Usage:
  node scripts/api/list-tags.mjs [--format json|table]

Options:
  --format <json|table>   输出格式，默认 json
  --help, -h              显示此帮助

Output (json):
  [ { "id": 1, "tagName": "Agent" }, ... ]
`;

function renderTable(rows) {
  if (!rows || rows.length === 0) {
    return '(no tags)';
  }
  const idWidth = Math.max(2, ...rows.map(r => String(r.id).length));
  const nameWidth = Math.max(7, ...rows.map(r => String(r.tagName || '').length));
  const header = `${'id'.padEnd(idWidth)}  ${'tagName'.padEnd(nameWidth)}`;
  const sep = `${'-'.repeat(idWidth)}  ${'-'.repeat(nameWidth)}`;
  const lines = rows.map(r => `${String(r.id).padEnd(idWidth)}  ${String(r.tagName || '').padEnd(nameWidth)}`);
  return [header, sep, ...lines].join('\n');
}

async function main() {
  const args = parseCliArgs(process.argv.slice(2));
  if (args.help) { process.stdout.write(HELP); return; }

  const data = await apiGet('/content/api/tag/list');
  const list = Array.isArray(data) ? data : [];

  if (args.format === 'table') {
    process.stdout.write(renderTable(list) + '\n');
  } else {
    printJson(list);
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
