#!/usr/bin/env node
import { apiCall, parseArgs, formatSize, checkResponse } from "./ftp-api.mjs";

const args = parseArgs(process.argv);
const remotePath = args._[0];

if (!remotePath) {
  console.error("用法: node info.mjs <远程文件路径>");
  process.exit(1);
}

try {
  const result = await apiCall("info", { path: remotePath });
  const data = checkResponse(result, "获取文件信息");

  console.log(`文件: ${data.path}`);
  console.log(`大小: ${data.size !== null ? formatSize(data.size) + ` (${data.size} 字节)` : "N/A"}`);
  console.log(`修改时间: ${data.modified || "N/A"}`);
} catch (err) {
  console.error(`错误: ${err.message}`);
  process.exit(1);
}