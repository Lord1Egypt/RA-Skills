#!/usr/bin/env node
import { apiCall, parseArgs, checkResponse } from "./ftp-api.mjs";

const args = parseArgs(process.argv);
const srcPath = args._[0];
const destPath = args._[1];

if (!srcPath || !destPath) {
  console.error("用法: node move.mjs <源路径> <目标路径>");
  process.exit(1);
}

try {
  console.error(`正在移动: ${srcPath} → ${destPath} ...`);

  const result = await apiCall("move", { from: srcPath, to: destPath });
  checkResponse(result, "移动");

  console.log(`已移动: ${srcPath} → ${destPath}`);
} catch (err) {
  console.error(`错误: ${err.message}`);
  process.exit(1);
}