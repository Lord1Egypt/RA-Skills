import { constants, lstatSync, fstatSync, readFileSync, openSync, closeSync } from "node:fs";
import { mkdir, lstat, open, rename, rm } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import { randomUUID } from "node:crypto";

export const credentialsDirectory = () => join(homedir(), ".aivideo-maker");

function checkPrivate(stat, directory = false) {
  if (
    (directory ? !stat.isDirectory() : !stat.isFile()) ||
    (stat.mode & 0o077) !== 0 ||
    (process.getuid && stat.uid !== process.getuid())
  ) {
    throw new Error(
      "Saved credentials must be owned by you and accessible only to you. Run connect again after fixing file permissions.",
    );
  }
}

export function loadSavedKey(directory = credentialsDirectory()) {
  let fd;
  try {
    checkPrivate(lstatSync(directory), true);
    const path = join(directory, "credentials.json");
    checkPrivate(lstatSync(path));
    fd = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW);
    checkPrivate(fstatSync(fd));
    const value = JSON.parse(readFileSync(fd, "utf8"));
    if (typeof value.apiKey !== "string" || !value.apiKey.trim()) throw new Error();
    return value.apiKey;
  } catch (error) {
    if (error.code === "ENOENT") return "";
    throw new Error(
      "Cannot read private AI Video Maker credentials. Run connect again or set AIVIDEO_API_KEY.",
    );
  } finally {
    if (fd !== undefined) closeSync(fd);
  }
}

export async function saveKey(apiKey, directory = credentialsDirectory()) {
  await mkdir(directory, { recursive: true, mode: 0o700 });
  checkPrivate(await lstat(directory), true);
  const temporary = join(directory, `.credentials-${randomUUID()}`);
  try {
    const file = await open(temporary, "wx", 0o600);
    try {
      await file.writeFile(JSON.stringify({ apiKey }) + "\n");
    } finally {
      await file.close();
    }
    // Atomic replacement never follows an existing credentials-file symlink.
    await rename(temporary, join(directory, "credentials.json"));
  } finally {
    await rm(temporary, { force: true });
  }
}
