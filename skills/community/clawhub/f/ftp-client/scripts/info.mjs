#!/usr/bin/env node
import { createFtpClient, parseArgs, formatSize, formatDate } from "./ftp-utils.mjs";

const args = parseArgs(process.argv);
const remotePath = args._[0];

if (!remotePath) {
  console.error("Usage: node info.mjs <remote-file-path>");
  process.exit(1);
}

try {
  const { client } = await createFtpClient({ verbose: args.verbose });

  let size = null;
  let lastMod = null;

  try {
    size = await client.size(remotePath);
  } catch {
    // size command may not be supported
  }

  try {
    lastMod = await client.lastMod(remotePath);
  } catch {
    // lastMod command may not be supported
  }

  client.close();

  console.log(`File: ${remotePath}`);
  console.log(`Size: ${size !== null ? formatSize(size) + ` (${size} bytes)` : "N/A (server may not support SIZE)"}`);
  console.log(`Last Modified: ${lastMod ? formatDate(lastMod) : "N/A (server may not support MDTM)"}`);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}