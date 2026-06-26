#!/usr/bin/env node
/**
 * 创建一个新标签。
 *
 * 用途：
 * - save-article 的 tags 闭环在遇到新标签名时会自动调
 * - 用户想手动创建一个标签（运营/初始化场景）
 *
 * Usage:
 *   node scripts/api/save-tag.mjs --name <tagName>
 *
 * Env: FX_AI_API_KEY 必填
 *
 * Output (json on success):
 *   { "id": 12, "tagName": "Agent" }
 *
 * Exit: 0 success / 1 error
 *
 * 后端约束：tagName 非空 ≤64 字符
 */
import { apiPostJson, failWith, parseCliArgs, printJson } from './_lib.mjs';

const HELP = `创建 feima-lab 标签

Usage:
  node scripts/api/save-tag.mjs --name <tagName>

Options:
  --name <tagName>   标签名（必填，非空，≤64 字符）
  --help, -h         显示此帮助

Output (json):
  { "id": 12, "tagName": "Agent" }
`;

async function main() {
  const args = parseCliArgs(process.argv.slice(2));
  if (args.help) { process.stdout.write(HELP); return; }

  const name = args.name;
  if (!name || !String(name).trim()) {
    failWith('invalid_argument', '缺少 --name 参数', HELP);
  }
  const trimmed = String(name).trim();
  if (trimmed.length > 64) {
    failWith('invalid_argument', `tagName 长度 ${trimmed.length} 超过 64 字符上限`, '截断或改名');
  }

  const id = await apiPostJson('/content/api/tag/save', { tagName: trimmed });
  if (id == null) {
    failWith('api_error', '后端返回 id 为 null', '检查后端日志');
  }

  printJson({ id: Number(id), tagName: trimmed });
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
