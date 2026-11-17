import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
export const hash = (file) =>
  "sha256:" + crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
export const statePath = (args) =>
  path.resolve(
    args.state ||
      (args["state-dir"] ? path.join(args["state-dir"], "runs.json") : null) ||
      path.join(
        process.env.CALIBRE_METADATA_APPLY_STATE_DIR ||
          path.join(
            process.env.XDG_STATE_HOME || path.join(os.homedir(), ".local", "state"),
            "calibre-metadata-apply",
          ),
        "runs.json",
      ),
  );
export function readState(file) {
  if (!fs.existsSync(file)) return { version: 3, runs: {}, completed: {} };
  const s = JSON.parse(fs.readFileSync(file, "utf8"));
  if (
    s?.version !== 3 ||
    !s.runs ||
    typeof s.runs !== "object" ||
    Array.isArray(s.runs) ||
    !s.completed ||
    typeof s.completed !== "object" ||
    Array.isArray(s.completed)
  )
    throw new Error(
      "invalid/legacy state: preserved unchanged; re-prepare legacy runs in a new state file",
    );
  return s;
}
export function writeState(file, s) {
  const tmp = file + ".tmp-" + process.pid + "-" + crypto.randomBytes(6).toString("hex");
  let fd;
  try {
    fd = fs.openSync(tmp, "wx", 0o600);
    fs.writeFileSync(fd, JSON.stringify(s, null, 2) + "\n");
    fs.fsyncSync(fd);
    fs.closeSync(fd);
    fd = undefined;
    fs.renameSync(tmp, file);
  } finally {
    if (fd !== undefined) fs.closeSync(fd);
    if (fs.existsSync(tmp)) fs.unlinkSync(tmp);
  }
}
export function withStateLock(file, fn) {
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  const lock = file + ".lock";
  let fd;
  try {
    fd = fs.openSync(lock, "wx", 0o600);
  } catch (e) {
    if (e.code === "EEXIST")
      throw new Error("state locked; inspect live work before manual lock recovery");
    throw e;
  }
  try {
    return fn(readState(file));
  } finally {
    fs.closeSync(fd);
    fs.unlinkSync(lock);
  }
}
export function runId(value) {
  if (typeof value !== "string" || !/^[A-Za-z0-9][A-Za-z0-9_.-]{0,100}$/.test(value))
    throw new Error("invalid run id");
  return value;
}
