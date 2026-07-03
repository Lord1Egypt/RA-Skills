"use strict";

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const pkg = require("../package.json");

const root = path.resolve(__dirname, "..");
const outDir = path.join(root, "dist", "release");

function run(cmd, args) {
  const result = spawnSync(cmd, args, { cwd: root, stdio: "inherit" });
  if (result.status !== 0) process.exit(result.status || 1);
}

fs.mkdirSync(outDir, { recursive: true });
run("npm", ["test"]);
run("npm", ["pack", "--pack-destination", outDir]);

const expectedName = `${pkg.name.replace("@", "").replace("/", "-")}-${pkg.version}.tgz`;
const latest = path.join(outDir, expectedName);
if (latest) {
  console.log("");
  console.log(`Release package ready: ${latest}`);
  console.log("");
  console.log("Install:");
  console.log(`  npm install -g ${latest}`);
  console.log("  clawvoice init --mode hybrid --mic");
}
