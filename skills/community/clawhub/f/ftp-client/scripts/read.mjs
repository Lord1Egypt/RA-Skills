#!/usr/bin/env node
import { createFtpClient, parseArgs } from "./ftp-utils.mjs";
import { Writable } from "stream";

const args = parseArgs(process.argv);
const remotePath = args._[0];
const encoding = args.encoding || "utf8";

if (!remotePath) {
  console.error("Usage: node read.mjs <remote-file-path> [--encoding utf8]");
  process.exit(1);
}

try {
  const { client } = await createFtpClient({ verbose: args.verbose });

  // Collect file content into a buffer
  const chunks = [];
  const writableStream = new Writable({
    write(chunk, enc, callback) {
      chunks.push(chunk);
      callback();
    },
  });

  await client.downloadTo(writableStream, remotePath);
  client.close();

  const content = Buffer.concat(chunks).toString(encoding);
  console.log(content);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}