#!/usr/bin/env node
import { apiCall, parseArgs, checkResponse } from "./ftp-api.mjs";

const args = parseArgs(process.argv);
const remotePath = args._[0];

if (!remotePath) {
  console.error("用法: node mkdir.mjs <远程目录路径>");
  process.exit(1);
}

try {
  console.error(`正在创建目录: ${remotePath} ...`);

  const result = await apiCall("mkdir", { path: remotePath });
  checkResponse(result, "创建目录");

  console.log(`目录已创建: ${remotePath}`);
} catch (err) {
  console.error(`错误: ${err.message}`);
  process.exit(1);
}