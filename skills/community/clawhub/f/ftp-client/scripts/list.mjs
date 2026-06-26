#!/usr/bin/env node
import { createFtpClient, parseArgs, formatSize, formatDate } from "./ftp-utils.mjs";

const args = parseArgs(process.argv);
const remotePath = args._[0] || "/";

try {
  const { client } = await createFtpClient({ verbose: args.verbose });

  const list = await client.list(remotePath);
  client.close();

  if (list.length === 0) {
    console.log(`Directory "${remotePath}" is empty.`);
    process.exit(0);
  }

  if (args.long) {
    // Detailed listing
    const header = `${"Type".padEnd(6)} ${"Size".padStart(12)} ${"Modified".padEnd(20)} Name`;
    console.log(header);
    console.log("-".repeat(header.length + 10));
    for (const item of list) {
      const type = item.isDirectory ? "DIR" : item.isSymbolicLink ? "LINK" : "FILE";
      const size = item.isDirectory ? "-" : formatSize(item.size);
      const date = formatDate(item.modifiedAt || item.rawModifiedAt);
      console.log(`${type.padEnd(6)} ${size.padStart(12)} ${date.padEnd(20)} ${item.name}`);
    }
  } else {
    // Simple listing
    for (const item of list) {
      const prefix = item.isDirectory ? "[DIR]  " : "       ";
      console.log(`${prefix}${item.name}`);
    }
  }

  console.log(`\nTotal: ${list.length} items in "${remotePath}"`);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}