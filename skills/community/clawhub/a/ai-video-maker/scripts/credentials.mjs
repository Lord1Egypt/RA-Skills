import { constants, lstatSync, fstatSync, readFileSync, openSync, closeSync } from "node:fs";
import { mkdir, lstat, open, rename, rm } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import { randomUUID } from "node:crypto";

export const credentialsDirectory = () => join(homedir(), ".aivideo-maker");

// Windows has no owner/group/other mode bits: Node reports every file there as 0666 or 0444,
// so the Unix check would reject each one. The folder sits in the user's own profile instead.
export function checkPrivate(stat, directory = false, platform = process.platform) {
  // A link, or a file where a folder belongs, is not something permissions can fix.
  if (directory ? !stat.isDirectory() : !stat.isFile()) {
    throw Object.assign(
      new Error("Saved credentials must be a regular folder and file, not a link."),
      { code: "WRONG_TYPE" },
    );
  }
  if (
    platform !== "win32" &&
    ((stat.mode & 0o077) !== 0 || (process.getuid && stat.uid !== process.getuid()))
  ) {
    throw Object.assign(
      new Error(
        "Saved credentials must be owned by you and accessible only to you. Run connect again after fixing file permissions.",
      ),
      { code: "NOT_PRIVATE" },
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
    // Running plain connect again would stop here every time, so each message names a way out.
    throw new Error(
      error.code === "NOT_PRIVATE"
        ? "Cannot read private AI Video Maker credentials: ~/.aivideo-maker and its credentials.json must be owned by you with owner-only access (folder 700, file 600). Fix the permissions and run connect again, or set AIVIDEO_API_KEY."
        : error.code === "WRONG_TYPE"
          ? "Cannot read private AI Video Maker credentials: ~/.aivideo-maker must be a real folder and its credentials.json a regular file, not a link or another kind of entry. Replace it with a real one and run connect again, or set AIVIDEO_API_KEY."
          : "Cannot read private AI Video Maker credentials. Run connect.mjs --reconnect to replace them, or set AIVIDEO_API_KEY.",
    );
  } finally {
    if (fd !== undefined) closeSync(fd);
  }
}

async function writePrivate(directory, name, value) {
  await mkdir(directory, { recursive: true, mode: 0o700 });
  checkPrivate(await lstat(directory), true);
  const temporary = join(directory, `.credentials-${randomUUID()}`);
  try {
    const file = await open(temporary, "wx", 0o600);
    try {
      await file.writeFile(JSON.stringify(value) + "\n");
    } finally {
      await file.close();
    }
    // Atomic replacement never follows an existing symlink at the destination.
    await rename(temporary, join(directory, name));
  } finally {
    await rm(temporary, { force: true });
  }
}

// Proves a key can be stored here before a browser approval is requested: a key the server
// has already issued cannot be handed over a second time once this process is gone.
export async function checkPrivateStorage(
  directory = credentialsDirectory(),
  platform = process.platform,
) {
  const probe = `.probe-${randomUUID()}`;
  try {
    await writePrivate(directory, probe, {});
  } finally {
    await rm(join(directory, probe), { force: true }).catch(() => {});
  }
  // Writing a new file is not the same as replacing the saved key: a folder under that name,
  // or a read-only file on Windows, lets the probe through and then rejects the real key.
  const saved = await lstat(join(directory, "credentials.json")).catch((error) => {
    if (error.code === "ENOENT") return null;
    throw error;
  });
  if (saved && (saved.isDirectory() || (platform === "win32" && (saved.mode & 0o200) === 0))) {
    throw Object.assign(new Error("The saved credentials file cannot be replaced."), {
      code: "NOT_REPLACEABLE",
    });
  }
}

export async function saveKey(apiKey, directory = credentialsDirectory()) {
  await writePrivate(directory, "credentials.json", { apiKey });
}

// A browser approval in progress. Kept on disk so a helper that was stopped before the
// user approved can pick up the same link and code instead of stranding the approval.
const PENDING_CONNECTION = "pending-connection.json";

export function loadPendingConnection(directory = credentialsDirectory()) {
  let fd;
  try {
    checkPrivate(lstatSync(directory), true);
    const path = join(directory, PENDING_CONNECTION);
    checkPrivate(lstatSync(path));
    fd = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW);
    checkPrivate(fstatSync(fd));
    const value = JSON.parse(readFileSync(fd, "utf8"));
    return /^[a-f0-9]{64}$/.test(value?.deviceCode || "") &&
      /^[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}$/.test(value?.userCode || "") &&
      Number.isFinite(value?.expiresAt)
      ? {
          deviceCode: value.deviceCode,
          userCode: value.userCode,
          expiresAt: value.expiresAt,
          // Started with --reconnect: it replaces a saved key instead of filling a gap.
          replacing: value.replacing === true,
        }
      : null;
  } catch {
    // Missing, unreadable or unsafe state is never trusted; connect starts a new approval.
    return null;
  } finally {
    if (fd !== undefined) closeSync(fd);
  }
}

export async function savePendingConnection(pending, directory = credentialsDirectory()) {
  await writePrivate(directory, PENDING_CONNECTION, pending);
}

export async function clearPendingConnection(directory = credentialsDirectory()) {
  await rm(join(directory, PENDING_CONNECTION), { force: true }).catch(() => {});
}
