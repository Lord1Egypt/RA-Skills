#!/usr/bin/env node
import { apiCall, parseArgs, checkResponse } from "./ftp-api.mjs";

const args = parseArgs(process.argv);
const srcPath = args._[0];
const destPath = args._[1];

if (!srcPath || !destPath) {
  console.error("用法: node copy.mjs <源文件路径> <目标文件路径>");
  process.exit(1);
}

try {
  console.error(`正在复制: ${srcPath} → ${destPath} ...`);

  const result = await apiCall("copy", { from: srcPath, to: destPath });
  checkResponse(result, "复制");

  console.log(`已复制: ${srcPath} → ${destPath}`);
} catch (err) {
  console.error(`错误: ${err.message}`);
  process.exit(1);
}