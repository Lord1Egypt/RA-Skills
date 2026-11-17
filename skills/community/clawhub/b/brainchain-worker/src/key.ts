import { randomBytes } from "node:crypto";
import { accessSync, constants, mkdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { basename, dirname, join } from "node:path";

import { stateDir } from "./state.js";

/** Names the file a run passes its key through when it restarts itself without the key in its environment. */
const HANDOFF = "BRAINCHAIN_WORKER_KEY_HANDOFF";
const HANDOFF_NAME = /^brainchain-worker-key-[0-9a-f]{32}$/;

export const expandHome = (path: string) => (path === "~" || path.startsWith("~/") ? join(homedir(), path.slice(1)) : path);

/** Whether the environment names a key, without reading it: a key file can be a pipe, which reads only once. */
export const keyConfigured = (env: NodeJS.ProcessEnv = process.env) =>
  Boolean(env[HANDOFF] || env.BRAINCHAIN_WORKER_KEY?.trim() || env.BRAINCHAIN_WORKER_KEY_FILE?.trim());

/** What is wrong with a key file's text, in words that never repeat any of it. */
function keyFileProblem(text: string): string | undefined {
  if (text === "") return "is empty";
  if (/^(0x)?[0-9a-f]{64}$/i.test(text)) return undefined;
  if (/[\r\n]/.test(text)) return "holds more than one line";
  if (/^(export\s+)?[A-Za-z_][A-Za-z0-9_]*\s*=/.test(text)) return "holds a line in the form NAME=value";
  if (/^["'`]|["'`]$/.test(text)) return "holds the key in quotes";
  const hex = text.replace(/^0x/i, "");
  if (/^[0-9a-fA-F]+$/.test(hex)) return `holds ${hex.length} hex characters where a key has 64`;
  return "holds characters that are not hex digits";
}

function fromFile(path: string, warn: (message: string) => void): string {
  const file = expandHome(path);
  let text: string;
  try {
    const stat = statSync(file);
    // Windows reports no owner-only mode for any file: access there follows the folder's permissions, so there is nothing to warn about or chmod.
    if (process.platform !== "win32" && stat.isFile() && (stat.mode & 0o077) !== 0) warn(`warning: other users can read ${file}; run chmod 600 on it`);
    text = readFileSync(file, "utf8");
  } catch (error) {
    throw new Error(`BRAINCHAIN_WORKER_KEY_FILE names ${file}, which could not be read (${(error as NodeJS.ErrnoException).code ?? "unknown error"})`);
  }
  const key = text.trim();
  const problem = keyFileProblem(key);
  if (problem) throw new Error(`BRAINCHAIN_WORKER_KEY_FILE names ${file}, which ${problem}. It must hold the key alone: 64 hex characters, with or without 0x`);
  return key;
}

/** The text of the worker's key, from wherever the environment says it is; undefined when it names none. */
export function keyText(env: NodeJS.ProcessEnv = process.env, warn: (message: string) => void = console.warn): string | undefined {
  const handoff = env[HANDOFF];
  if (handoff !== undefined) {
    delete env[HANDOFF];
    if (!HANDOFF_NAME.test(basename(handoff))) throw new Error(`${HANDOFF} is for the worker's own use; unset it`);
    const text = readFileSync(handoff, "utf8");
    rmSync(handoff, { force: true });
    return text;
  }
  const inline = env.BRAINCHAIN_WORKER_KEY?.trim();
  const file = env.BRAINCHAIN_WORKER_KEY_FILE?.trim();
  if (inline && file) throw new Error("Set BRAINCHAIN_WORKER_KEY or BRAINCHAIN_WORKER_KEY_FILE, not both");
  return file ? fromFile(file, warn) : inline || undefined;
}

/** Writes a new key to a file only its owner can read; an existing file is left alone, since it may hold a wallet's only key. */
export function writeKeyFile(path: string, key: string): void {
  const file = expandHome(path);
  mkdirSync(dirname(file), { recursive: true, mode: 0o700 });
  try {
    writeFileSync(file, `${key}\n`, { flag: "wx", mode: 0o600 });
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "EEXIST") throw new Error(`${file} already exists, and new-key never replaces a key`);
    throw error;
  }
}

/** Memory rather than disk where the system offers it. The file lives for the milliseconds a restart takes. */
function handoffDir(): string {
  try {
    accessSync("/dev/shm", constants.W_OK);
    return "/dev/shm";
  } catch {
    mkdirSync(stateDir(), { recursive: true, mode: 0o700 });
    return stateDir();
  }
}

/** A variable that holds a key or says where one is: the worker's and the Solana wallet's, which `run` never uses. Windows reads names without regard to case. */
const KEY_VARIABLE = /^BRAINCHAIN_(WORKER|SOLANA)_KEY(_FILE)?$/i;

/** A key file that is a pipe has been read and holds nothing, so its name can stay: a restart would put a key piped in to stay out of files in one for a moment. */
function namesOnlyAPipe(names: string[], env: NodeJS.ProcessEnv): boolean {
  if (names.length !== 1 || names[0] !== "BRAINCHAIN_WORKER_KEY_FILE") return false;
  try {
    return !statSync(expandHome(env.BRAINCHAIN_WORKER_KEY_FILE!.trim())).isFile();
  } catch {
    return false;
  }
}

/**
 * Restarts this process in place without any key variable in its environment.
 * Deleting them would not do: `ps eww` and /proc read the block the process
 * started with, and a command run by `run` can reach both. The pid, the output
 * and the supervisor's view all stay as they were. Returns when there is
 * nothing to clear, or when it could not be cleared.
 */
export function clearKeyFromEnvironment(
  key: string,
  warn: (message: string) => void,
  env: NodeJS.ProcessEnv = process.env,
  execve = process.execve,
  platform: NodeJS.Platform = process.platform,
): void {
  const names = Object.keys(env).filter((name) => KEY_VARIABLE.test(name));
  if (names.length === 0 || namesOnlyAPipe(names, env)) return;
  // Windows cannot replace a running process, so trying would only put the key in a file for a moment.
  if (platform === "win32") return warn("warning: on Windows the key variables stay in this process's environment; give the key through BRAINCHAIN_WORKER_KEY_FILE and keep that file in your own user folder");
  if (typeof execve !== "function") return warn(`warning: Node.js ${process.version} cannot clear the key variables from this process's environment; Node.js 22.15 or later can`);
  const rest = Object.fromEntries(Object.entries(env).filter(([name]) => !KEY_VARIABLE.test(name)));
  let file: string | undefined;
  try {
    file = join(handoffDir(), `brainchain-worker-key-${randomBytes(16).toString("hex")}`);
    writeFileSync(file, key, { flag: "wx", mode: 0o600 });
    execve(process.execPath, [process.execPath, ...process.execArgv, process.argv[1]!, ...process.argv.slice(2)], { ...rest, [HANDOFF]: file } as Record<string, string>);
  } catch (error) {
    if (file !== undefined) rmSync(file, { force: true });
    warn(`warning: could not clear the key variables from this process's environment (${(error as Error).message})`);
  }
}
