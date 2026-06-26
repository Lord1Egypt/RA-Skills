#!/usr/bin/env node
import { apiDownloadFile, parseArgs, formatSize } from "./ftp-api.mjs";
import { writeFileSync } from "fs";
import { tmpdir } from "os";
import { join, basename } from "path";

const args = parseArgs(process.argv);
const remotePath = args._[0];

if (!remotePath) {
  console.error("用法: node download.mjs <远程文件路径> [--out <本地保存路径>]");
  process.exit(1);
}

try {
  console.error(`正在下载: ${remotePath} ...`);

  const { buffer, filename, size } = await apiDownloadFile(remotePath);

  const localPath = args.out || join(tmpdir(), filename || basename(remotePath));
  writeFileSync(localPath, buffer);

  console.log(`文件已下载到: ${localPath}`);
  console.log(`文件大小: ${formatSize(buffer.length)}`);
} catch (err) {
  console.error(`错误: ${err.message}`);
  process.exit(1);
}