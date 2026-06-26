#!/usr/bin/env node
import { apiUploadFile, parseArgs, checkResponse } from "./ftp-api.mjs";
import { existsSync } from "fs";
import { basename } from "path";

const args = parseArgs(process.argv);
const localPath = args._[0];

if (!localPath) {
  console.error("用法: node upload.mjs <本地文件路径> --to <远程路径>");
  process.exit(1);
}

if (!existsSync(localPath)) {
  console.error(`本地文件不存在: ${localPath}`);
  process.exit(1);
}

const remotePath = args.to || ("/" + basename(localPath));

try {
  console.error(`正在上传: ${localPath} → ${remotePath} ...`);

  const result = await apiUploadFile(localPath, remotePath);
  checkResponse(result, "上传");

  console.log(`文件已上传到: ${remotePath}`);
} catch (err) {
  console.error(`错误: ${err.message}`);
  process.exit(1);
}