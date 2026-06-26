#!/usr/bin/env node
/**
 * 上传单个文件到 feima-lab 后端 OSS。
 *
 * 返回一个远程 URL，save-article.mjs 在上传封面图时会调用这个脚本；
 * 用户也可以直接跑来手工上传文件。
 *
 * Usage:
 *   node scripts/api/upload-file.mjs --file <local-path>
 *
 * Env:
 *   FX_AI_API_KEY     必填
 *
 * Output (json to stdout on success):
 *   { "url": "https://cdn.fenxianglife.com/xxx.webp" }
 *
 * Exit: 0 success / 1 error (JSON to stderr)
 */
import { resolve } from 'node:path';
import { apiPostMultipart, failWith, parseCliArgs, printJson } from './_lib.mjs';

const HELP = `上传文件到 feima-lab OSS

Usage:
  node scripts/api/upload-file.mjs --file <path>

Options:
  --file <path>   待上传的本地文件路径（必填）
  --help, -h      显示此帮助

Output (json):
  { "url": "https://cdn.fenxianglife.com/xxx" }

Auth:
  设置环境变量 FX_AI_API_KEY=<your-key>
`;

async function main() {
  const args = parseCliArgs(process.argv.slice(2));
  if (args.help) { process.stdout.write(HELP); return; }
  if (!args.file) {
    failWith('invalid_argument', '缺少 --file 参数', '用法：node scripts/api/upload-file.mjs --file <path>');
  }

  const absPath = resolve(String(args.file));
  const result = await apiPostMultipart('/content/api/upload', absPath);

  // result is UploadFileResult { url }
  if (!result || !result.url) {
    failWith('api_error', '后端返回缺少 url 字段', `原始响应: ${JSON.stringify(result)}`);
  }

  printJson({ url: result.url });
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
