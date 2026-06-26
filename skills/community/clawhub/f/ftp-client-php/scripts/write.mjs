#!/usr/bin/env node
import { apiUploadContent, parseArgs, checkResponse } from "./ftp-api.mjs";

const args = parseArgs(process.argv);
const remotePath = args._[0];

if (!remotePath) {
  console.error("用法: node write.mjs <远程文件路径> \"内容\"");
  console.error("  或: node write.mjs <远程文件路径> --stdin < 本地文件");
  process.exit(1);
}

try {
  let content;

  if (args.stdin) {
    // 从 stdin 读取
    const chunks = [];
    for await (const chunk of process.stdin) {
      chunks.push(chunk);
    }
    content = Buffer.concat(chunks).toString("utf-8");
  } else if (args._[1] !== undefined) {
    // 从命令行参数读取
    content = args._.slice(1).join(" ");
  } else {
    console.error("请提供文件内容（作为参数或使用 --stdin）");
    process.exit(1);
  }

  console.error(`正在写入: ${remotePath} (${content.length} 字符) ...`);

  const result = await apiUploadContent(content, remotePath);
  checkResponse(result, "写入");

  console.log(`文件已写入: ${remotePath}`);
} catch (err) {
  console.error(`错误: ${err.message}`);
  process.exit(1);
}