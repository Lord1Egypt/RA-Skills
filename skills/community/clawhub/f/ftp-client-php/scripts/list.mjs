#!/usr/bin/env node
import { apiCall, parseArgs, formatSize, checkResponse } from "./ftp-api.mjs";

const args = parseArgs(process.argv);
const remotePath = args._[0] || "/";

try {
  const result = await apiCall("list", {
    path: remotePath,
    detailed: args.detailed ? true : false,
  });

  const data = checkResponse(result, "列出目录");
  const items = data.items || [];

  if (items.length === 0) {
    console.log(`目录 "${remotePath}" 为空。`);
    process.exit(0);
  }

  if (args.detailed) {
    const header = `${"类型".padEnd(6)} ${"大小".padStart(12)} ${"日期".padEnd(20)} 名称`;
    console.log(header);
    console.log("-".repeat(70));
    for (const item of items) {
      const type = item.type === "dir" ? "DIR" : item.type === "link" ? "LINK" : "FILE";
      const size = item.type === "dir" ? "-" : formatSize(item.size);
      const date = item.date || "";
      const name = item.name || item.raw || "";
      console.log(
        `${type.padEnd(6)} ${size.padStart(12)} ${date.padEnd(20)} ${name}`
      );
    }
  } else {
    for (const item of items) {
      const prefix = item.type === "dir" ? "[DIR]  " : "       ";
      console.log(`${prefix}${item.name}`);
    }
  }

  console.log(`\n共 ${items.length} 个项目，路径: ${data.path}`);
} catch (err) {
  console.error(`错误: ${err.message}`);
  process.exit(1);
}