#!/usr/bin/env node
import { createFtpClient, parseArgs } from "./ftp-utils.mjs";

const args = parseArgs(process.argv);
const remotePath = args._[0];

if (!remotePath) {
  console.error("Usage: node mkdir.mjs <remote-dir-path>");
  process.exit(1);
}

try {
  const { client } = await createFtpClient({ verbose: args.verbose });

  await client.ensureDir(remotePath);
  console.log(`Directory created (or already exists): ${remotePath}`);

  // Return to root after ensureDir changes cwd
  await client.cd("/");
  client.close();
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}