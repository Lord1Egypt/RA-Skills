#!/usr/bin/env node
import { createFtpClient, parseArgs } from "./ftp-utils.mjs";
import { tmpdir } from "os";
import { join, basename } from "path";
import { unlink } from "fs/promises";

const args = parseArgs(process.argv);
const srcPath = args._[0];
const destPath = args._[1];

if (!srcPath || !destPath) {
  console.error("Usage: node copy.mjs <remote-source> <remote-dest>");
  process.exit(1);
}

try {
  const { client } = await createFtpClient({ verbose: args.verbose });

  // FTP doesn't support server-side copy, so download then re-upload
  const tempFile = join(tmpdir(), `ftp-copy-${Date.now()}-${basename(srcPath)}`);

  process.stderr.write(`Downloading ${srcPath} to temp...\n`);
  await client.downloadTo(tempFile, srcPath);

  process.stderr.write(`Uploading to ${destPath}...\n`);
  await client.uploadFrom(tempFile, destPath);

  client.close();

  // Clean up temp file
  try {
    await unlink(tempFile);
  } catch {
    // Ignore cleanup errors
  }

  console.log(`Copied: ${srcPath} → ${destPath}`);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}