const fs = require("fs");
const fsp = fs.promises;
const path = require("path");
const crypto = require("crypto");

async function ensureDir(dirPath, mode = 0o700) {
  await fsp.mkdir(dirPath, { recursive: true, mode });
  try {
    await fsp.chmod(dirPath, mode);
  } catch (_) {
    // Ignore chmod failures on filesystems that do not support Unix mode bits.
  }
}

async function fileExists(filePath) {
  try {
    await fsp.access(filePath, fs.constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

async function readJson(filePath, fallback = null) {
  if (!(await fileExists(filePath))) {
    return fallback;
  }
  const text = await fsp.readFile(filePath, "utf8");
  return JSON.parse(text);
}

async function writeJsonAtomic(filePath, data, mode = 0o600) {
  const dir = path.dirname(filePath);
  await ensureDir(dir);

  const tempFile = `${filePath}.${process.pid}.${crypto.randomBytes(4).toString("hex")}.tmp`;
  const payload = `${JSON.stringify(data, null, 2)}\n`;
  await fsp.writeFile(tempFile, payload, { mode });
  await fsp.rename(tempFile, filePath);

  try {
    await fsp.chmod(filePath, mode);
  } catch (_) {
    // Ignore chmod failures on filesystems that do not support Unix mode bits.
  }
}

function maskSecret(value, keep = 4) {
  if (!value || typeof value !== "string") {
    return "";
  }
  if (value.length <= keep * 2) {
    return `${"*".repeat(Math.max(0, value.length - keep))}${value.slice(-keep)}`;
  }
  return `${value.slice(0, keep)}***${value.slice(-keep)}`;
}

module.exports = {
  ensureDir,
  fileExists,
  maskSecret,
  readJson,
  writeJsonAtomic,
};
