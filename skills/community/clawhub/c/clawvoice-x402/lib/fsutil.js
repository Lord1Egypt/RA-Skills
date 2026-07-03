"use strict";

const fs = require("fs");

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  try {
    fs.chmodSync(dir, 0o700);
  } catch (_) {}
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writePrivateJson(file, value) {
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + "\n", { mode: 0o600 });
  try {
    fs.chmodSync(file, 0o600);
  } catch (_) {}
}

module.exports = { ensureDir, readJson, writePrivateJson };
