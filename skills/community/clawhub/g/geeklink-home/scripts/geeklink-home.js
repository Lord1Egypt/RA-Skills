#!/usr/bin/env node

const { existsSync } = require("node:fs");
const { join } = require("node:path");
const { spawnSync } = require("node:child_process");

const scriptDir = __dirname;
const skillDir = join(scriptDir, "..");
const vendorEntry = join(skillDir, "vendor", "geeklink-lan-cli.js");

if (!existsSync(vendorEntry)) {
  process.stderr.write(`geeklink-home vendor runtime not found: ${vendorEntry}\n`);
  process.exit(1);
}

const result = spawnSync(process.execPath, [vendorEntry, ...process.argv.slice(2)], {
  stdio: "inherit"
});

if (result.error) {
  process.stderr.write(`${result.error.message}\n`);
  process.exit(1);
}

process.exit(result.status === null ? 1 : result.status);
