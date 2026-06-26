#!/usr/bin/env node
import { createFtpClient, parseArgs } from "./ftp-utils.mjs";
import { basename } from "path";

const args = parseArgs(process.argv);
const localPath = args._[0];

if (!localPath) {
  console.error("Usage: node upload.mjs <local-path> [--to <remote-path>] [--dir]");
  process.exit(1);
}

try {
  const { client } = await createFtpClient({ verbose: args.verbose });

  // Track progress
  client.trackProgress((info) => {
    if (info.bytes > 0) {
      process.stderr.write(`\rUploading ${info.name}: ${(info.bytes / 1024).toFixed(1)} KB`);
    }
  });

  if (args.dir) {
    // Upload entire directory
    const remoteDirPath = args.to || "/";
    await client.uploadFromDir(localPath, remoteDirPath);
    client.close();
    process.stderr.write("\n");
    console.log(`Directory uploaded to: ${remoteDirPath}`);
  } else {
    // Upload single file
    const remotePath = args.to || ("/" + basename(localPath));
    await client.uploadFrom(localPath, remotePath);
    client.close();
    process.stderr.write("\n");
    console.log(`File uploaded to: ${remotePath}`);
  }
} catch (err) {
  console.error(`\nError: ${err.message}`);
  process.exit(1);
}