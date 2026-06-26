#!/usr/bin/env node
import { apiCall, parseArgs, checkResponse } from "./ftp-api.mjs";

const args = parseArgs(process.argv);
const remotePath = args._[0];

if (!remotePath) {
  console.error("用法: node delete.mjs <远程路径> [--dir]");
  process.exit(1);
}

try {
  console.error(`正在删除: ${remotePath}${args.dir ? " (目录)" : ""} ...`);

  const result = await apiCall("delete", {
    path: remotePath,
    is_dir: args.dir ? true : false,
  });

  checkResponse(result, "删除");
  console.log(`已删除: ${remotePath}`);
} catch (err) {
  console.error(`错误: ${err.message}`);
  process.exit(1);
}