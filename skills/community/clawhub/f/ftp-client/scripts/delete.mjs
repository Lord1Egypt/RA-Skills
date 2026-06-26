#!/usr/bin/env node
import { createFtpClient, parseArgs } from "./ftp-utils.mjs";

const args = parseArgs(process.argv);
const remotePath = args._[0];

if (!remotePath) {
  console.error("Usage: node delete.mjs <remote-path> [--dir]");
  process.exit(1);
}

try {
  const { client } = await createFtpClient({ verbose: args.verbose });

  if (args.dir) {
    await client.removeDir(remotePath);
    console.log(`Directory removed: ${remotePath}`);
  } else {
    await client.remove(remotePath);
    console.log(`File removed: ${remotePath}`);
  }

  client.close();
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}