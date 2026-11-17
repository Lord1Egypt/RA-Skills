#!/usr/bin/env node
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { contentTypeFor, parseServeArgs, publicUrl, USAGE } from "./lib/pure.mjs";

let args;
try {
  args = parseServeArgs(process.argv.slice(2));
} catch (error) {
  process.stderr.write(`${error.message}\n${USAGE}`);
  process.exit(2);
}
if (args.help) {
  process.stdout.write(USAGE);
  process.exit(0);
}

const file = path.resolve(args.file);
if (!fs.existsSync(file) || !fs.statSync(file).isFile()) {
  process.stderr.write(`Not a file: ${file}\n`);
  process.exit(2);
}

const leaf = args.name || path.basename(file);
const type = contentTypeFor(leaf);
const bytes = fs.statSync(file).size;
const server = http.createServer((req, res) => {
  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS",
      "Access-Control-Allow-Headers": "*",
    });
    res.end();
    return;
  }
  res.writeHead(200, {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": type,
    "Content-Length": bytes,
    "Cache-Control": "no-store",
  });
  if (req.method === "HEAD") {
    res.end();
    return;
  }
  fs.createReadStream(file).pipe(res);
});

server.listen(args.port, "127.0.0.1", () => {
  const url = publicUrl(args.port, leaf);
  process.stdout.write(
    `${JSON.stringify({ ok: true, url, file, bytes, port: args.port, leaf }, null, 2)}\n`,
  );
});

const shutdown = () => {
  server.close(() => process.exit(0));
};
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
