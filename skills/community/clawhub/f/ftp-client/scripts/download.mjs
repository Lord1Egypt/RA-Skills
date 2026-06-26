#!/usr/bin/env node
import { createFtpClient, parseArgs } from "./ftp-utils.mjs";
import { tmpdir } from "os";
import { join, basename } from "path";

const args = parseArgs(process.argv);
const remotePath = args._[0];

if (!remotePath) {
  console.error("Usage: node download.mjs <remote-path> [--out <local-path>] [--dir]");
  process.exit(1);
}

try {
  const { client } = await createFtpClient({ verbose: args.verbose });

  // Track progress
  client.trackProgress((info) => {
    if (info.bytes > 0) {
      process.stderr.write(`\rDownloading ${info.name}: ${(info.bytes / 1024).toFixed(1)} KB`);
    }
  });

  if (args.dir) {
    // Download entire directory
    const localDir = args.out || join(tmpdir(), `ftp-download-${Date.now()}`);
    await client.downloadToDir(localDir, remotePath);
    client.close();
    process.stderr.write("\n");
    console.log(`Directory downloaded to: ${localDir}`);
  } else {
    // Download single file
    const localPath = args.out || join(tmpdir(), basename(remotePath));
    await client.downloadTo(localPath, remotePath);
    client.close();
    process.stderr.write("\n");
    console.log(`File downloaded to: ${localPath}`);
  }
} catch (err) {
  console.error(`\nError: ${err.message}`);
  process.exit(1);
}