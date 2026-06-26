const os = require("os");
const path = require("path");

function isWindowsDrivePath(input) {
  return /^[A-Za-z]:[\\/]/.test(input);
}

function toWslPath(input) {
  const driveLetter = input[0].toLowerCase();
  const rest = input.slice(2).replace(/\\/g, "/").replace(/^\/+/, "");
  return `/mnt/${driveLetter}/${rest}`;
}

function expandHome(inputPath) {
  if (!inputPath.startsWith("~")) {
    return inputPath;
  }
  if (inputPath === "~") {
    return os.homedir();
  }
  if (inputPath.startsWith("~/")) {
    return path.join(os.homedir(), inputPath.slice(2));
  }
  return inputPath;
}

function normalizeLocalPath(inputPath) {
  if (!inputPath || typeof inputPath !== "string") {
    throw new Error("Path must be a non-empty string.");
  }

  let normalized = inputPath.trim();
  if (!normalized) {
    throw new Error("Path cannot be empty.");
  }

  if (isWindowsDrivePath(normalized)) {
    normalized = toWslPath(normalized);
  }

  normalized = expandHome(normalized);

  if (!path.isAbsolute(normalized)) {
    normalized = path.resolve(process.cwd(), normalized);
  }

  return path.normalize(normalized);
}

module.exports = {
  isWindowsDrivePath,
  normalizeLocalPath,
  toWslPath,
};
