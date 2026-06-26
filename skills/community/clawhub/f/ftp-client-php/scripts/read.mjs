#!/usr/bin/env node
import { apiCall, parseArgs, checkResponse } from "./ftp-api.mjs";

const args = parseArgs(process.argv);
const remotePath = args._[0];

if (!remotePath) {
  console.error("用法: node read.mjs <远程文件路径>");
  process.exit(1);
}

try {
  const result = await apiCall("read", { path: remotePath });
  const data = checkResponse(result, "读取文件");

  // 优先使用 content 字段（文本），否则解码 base64
  if (data.content !== undefined && data.content !== null) {
    console.log(data.content);
  } else if (data.content_base64) {
    const buf = Buffer.from(data.content_base64, "base64");
    console.log(buf.toString(args.encoding || "utf-8"));
  } else {
    console.log("（文件内容为空）");
  }
} catch (err) {
  console.error(`错误: ${err.message}`);
  process.exit(1);
}