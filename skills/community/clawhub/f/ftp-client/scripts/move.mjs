#!/usr/bin/env node
import { createFtpClient, parseArgs } from "./ftp-utils.mjs";

const args = parseArgs(process.argv);
const srcPath = args._[0];
const destPath = args._[1];

if (!srcPath || !destPath) {
  console.error("Usage: node move.mjs <source-path> <dest-path>");
  process.exit(1);
}

try {
  const { client } = await createFtpClient({ verbose: args.verbose });

  await client.rename(srcPath, destPath);
  console.log(`Moved: ${srcPath} → ${destPath}`);

  client.close();
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}