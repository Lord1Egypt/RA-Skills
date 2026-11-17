import { randomBytes } from "node:crypto";
import { copyFileSync, closeSync, fsyncSync, mkdirSync, openSync, readFileSync, readlinkSync, renameSync, rmSync, statSync, utimesSync, writeFileSync } from "node:fs";
import { homedir, hostname } from "node:os";
import { dirname, join } from "node:path";

import type { Hex } from "viem";

import type { Network } from "./network.js";
import { startTime } from "./proc.js";

export interface TaskState {
  /** Kept across retries and restarts, so a failed upload or submit does not run the paid command again. */
  result?: string;
  stored?: { uri: string; hash: Hex };
  /** The submit sent for the stored result, waited on before another is sent. */
  tx?: Hex;
  failures: number;
  /** Chain time, in seconds, before which the task is not tried again. */
  nextAt: number;
}

/** A delivered task: watched until it settles, then, when paid, minted for at most once an hour. */
export interface ProofTask {
  /** Wall-clock seconds when the result was delivered. */
  deliveredAt: number;
  /** When the task was paid, by the time of the block that paid it. */
  paidAt?: number;
  /** Wall-clock seconds before which the task is not looked at again. */
  nextAt: number;
  /** Set once the service has listed the task as waiting for its Proof. */
  listed?: true;
  /** Set once the worker has said the service does not list the task yet. */
  waited?: true;
  /** Set once the worker has said, on testnet, that it has no ETH to mint with. */
  told?: true;
}

export interface State {
  /** The task board the rest belongs to; state kept for another board is dropped. */
  board: string;
  tasks: Record<string, TaskState>;
  /** Tasks finished or given up, which stay hired on chain until they settle. */
  done: string[];
  /** The last block scanned for WorkerHired, and the tasks found that are still hired. */
  hired?: { block: number; tasks: string[] };
  /** The command running for a task, so the next run can stop it if this one dies first. */
  command?: { pgid: number; startedAt: number };
  /** Delivered tasks watched until they settle and, when paid, until their Proof is minted, by task id. */
  proofs?: Record<string, ProofTask>;
}

export interface Store {
  state: State;
  save(): void;
}

export const stateDir = () => join(homedir(), ".config", "brainchain-worker");

/** The decision count a one-shot watch run stopped at, kept per decision log; undefined when there is none or it cannot be read. */
export function readWatched(log: string, dir = stateDir()): bigint | undefined {
  try {
    const { seen } = JSON.parse(readFileSync(join(dir, `watch.${log.toLowerCase()}.json`), "utf8")) as { seen?: unknown };
    return typeof seen === "string" && /^\d+$/.test(seen) ? BigInt(seen) : undefined;
  } catch {
    return undefined;
  }
}

export function writeWatched(log: string, seen: bigint, dir = stateDir()): void {
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  const file = join(dir, `watch.${log.toLowerCase()}.json`);
  // Each write its own temp file: runs from cron overlap, and nothing else keeps them apart.
  const temp = `${file}.${process.pid}.${randomBytes(4).toString("hex")}.tmp`;
  writeFileSync(temp, JSON.stringify({ seen: seen.toString() }), { mode: 0o600 });
  renameSync(temp, file);
}

const empty = (board: string): State => ({ board: board.toLowerCase(), tasks: {}, done: [] });

export function memoryStore(board = ""): Store {
  return { state: empty(board), save: () => undefined };
}

const isObject = (value: unknown): value is Record<string, unknown> => typeof value === "object" && value !== null && !Array.isArray(value);
const isCount = (value: unknown): value is number => Number.isSafeInteger(value) && (value as number) >= 0;
const isHash = (value: unknown) => typeof value === "string" && /^0x[0-9a-fA-F]{64}$/.test(value);
const isIds = (value: unknown) => Array.isArray(value) && value.every((id) => typeof id === "string" && /^\d+$/.test(id));

function isTask(value: unknown): value is TaskState {
  if (!isObject(value) || !isCount(value.failures) || !isCount(value.nextAt)) return false;
  if (value.result !== undefined && typeof value.result !== "string") return false;
  if (value.tx !== undefined && !isHash(value.tx)) return false;
  return value.stored === undefined || (isObject(value.stored) && typeof value.stored.uri === "string" && isHash(value.stored.hash));
}

const isFlag = (value: unknown) => value === undefined || value === true;

function isProofs(value: unknown): boolean {
  if (!isObject(value) || !isIds(Object.keys(value))) return false;
  return Object.values(value).every(
    (p) => isObject(p) && isCount(p.deliveredAt) && isCount(p.nextAt) && (p.paidAt === undefined || isCount(p.paidAt)) && isFlag(p.listed) && isFlag(p.waited) && isFlag(p.told),
  );
}

/** Whether a parsed file is a state this worker can go on from; any other shape fails every round that reads it. */
function isState(value: unknown): value is State {
  if (!isObject(value) || typeof value.board !== "string" || !isObject(value.tasks) || !isIds(value.done)) return false;
  if (!Object.values(value.tasks).every(isTask)) return false;
  const { hired, command, proofs } = value;
  if (hired !== undefined && !(isObject(hired) && isCount(hired.block) && isIds(hired.tasks))) return false;
  if (proofs !== undefined && !isProofs(proofs)) return false;
  // Group 0 is this process's own and -1 is every process, so only a real command's group is signalled.
  return command === undefined || (isObject(command) && isCount(command.pgid) && command.pgid > 1 && isCount(command.startedAt));
}

function parse(text: string): State | undefined {
  try {
    const value: unknown = JSON.parse(text);
    return isState(value) ? value : undefined;
  } catch {
    return undefined;
  }
}

/** State in a 0600 JSON file, replaced whole on every save so a crash never leaves half a file. */
export function fileStore(file: string, board: string, warn: (message: string) => void = console.warn): Store {
  let state = empty(board);
  let text: string | undefined;
  try {
    text = readFileSync(file, "utf8");
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== "ENOENT") throw error;
  }
  const saved = text === undefined ? undefined : parse(text);
  if (saved?.board === state.board) state = saved;
  else if (saved) {
    // Task ids restart with each board, so none of this can carry over, but it must not vanish in silence.
    const left = [
      [Object.keys(saved.tasks).length, "tasks with results"],
      [saved.hired?.tasks.length ?? 0, "hired tasks"],
      [Object.keys(saved.proofs ?? {}).length, "tasks waiting to settle or mint"],
    ].flatMap(([count, what]) => (count ? [`${count} ${what}`] : []));
    if (left.length > 0) {
      const aside = `${file}.${saved.board}`;
      copyFileSync(file, aside);
      warn(`${file} holds work for the task board ${saved.board}, not this one: ${left.join(", ")}. This run starts without it, and a copy is at ${aside}.`);
    }
  }
  if (text !== undefined && saved === undefined) {
    // Refusing to start would turn one bad file into a crash loop under a supervisor.
    const aside = `${file}.corrupt-${new Date().toISOString().replace(/\.\d+Z$/, "Z").replace(/[-:]/g, "")}`;
    renameSync(file, aside);
    warn(`${file} could not be read as saved worker state, so it was moved to ${aside} and this run starts with no saved work`);
  }
  return {
    state,
    save() {
      mkdirSync(dirname(file), { recursive: true, mode: 0o700 });
      const temp = `${file}.${process.pid}.tmp`;
      const fd = openSync(temp, "w", 0o600);
      try {
        writeFileSync(fd, JSON.stringify(state));
        // On disk before the rename, so a power loss leaves the old file or the new one, never an empty one.
        fsyncSync(fd);
      } finally {
        closeSync(fd);
      }
      renameSync(temp, file);
    },
  };
}

/** How often a run touches its lock. */
const LOCK_BEAT_MS = 5_000;
/** With no touch for this long a lock was left behind, whatever process now has its pid. */
const LOCK_STALE_MS = 15_000;
/** How long a lock from another PID namespace is watched for a touch, a little over one beat. */
const LOCK_WATCH_MS = 7_000;
/** A takeover takes a few system calls, so one marker older than this was left by a crash. */
const TAKEOVER_STALE_MS = 5_000;
/** How far a start time read from ps, which gives it to the second, can fall after the true one. */
const START_SLACK_MS = 2_000;

/**
 * Where a pid means something. Containers sharing a config folder each have
 * their own numbering, so a holder's pid says nothing outside its own space.
 */
function pidSpace(): string {
  try {
    return `${readFileSync("/proc/sys/kernel/random/boot_id", "utf8").trim()}/${readlinkSync("/proc/self/ns/pid")}`;
  } catch {
    return hostname();
  }
}

function alive(pid: number): boolean {
  // A container restarts its process with the same pid, so our own pid in the file is a stale lock.
  if (!Number.isInteger(pid) || pid <= 0 || pid === process.pid) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return (error as NodeJS.ErrnoException).code === "EPERM";
  }
}

const sleep = (ms: number) => void Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);

function readIfThere(file: string): string | undefined {
  try {
    return readFileSync(file, "utf8");
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return undefined;
    throw error;
  }
}

function touchedAt(file: string): number | undefined {
  try {
    return statSync(file).mtimeMs;
  } catch {
    return undefined;
  }
}

/** Who a lock's text names. A bare pid is a lock from 0.12 or earlier; text that is neither is a lock still being written. */
function holderOf(text: string): { pid: number; space?: string } {
  try {
    const value: unknown = JSON.parse(text);
    if (typeof value === "number") return { pid: value };
    if (isObject(value) && typeof value.pid === "number" && typeof value.space === "string") return { pid: value.pid, space: value.space };
  } catch {
    // Handled below.
  }
  return { pid: 0, space: "" };
}

/**
 * Whether the run that wrote a bare-pid lock is still going. 0.12 and earlier
 * wrote the pid once and never touched the file again, so the lock's age says
 * nothing. A process that started after the lock was written, as pid 1 does
 * when a container restarts, has only come to reuse the pid.
 */
function bareHeld(pid: number, writtenAt: number): boolean {
  if (!alive(pid)) return false;
  const started = startTime(pid);
  return started === undefined || started <= writtenAt + START_SLACK_MS;
}

/** Whether the run that wrote a lock is still going. */
function isHeld(file: string, { pid, space }: ReturnType<typeof holderOf>, watchMs: number): boolean {
  const touched = touchedAt(file);
  if (touched === undefined) return false;
  if (space === undefined) return bareHeld(pid, touched);
  if (Date.now() - touched >= LOCK_STALE_MS) return false;
  if (pid === 0) return true;
  if (space === pidSpace()) return alive(pid);
  // A recent touch can be a run that just died, and a restarted container is one more pid namespace: a live run touches its lock again within a beat.
  sleep(watchMs);
  return touchedAt(file) !== touched;
}

const held = (pid: number, space: string | undefined, file: string) =>
  new Error(
    `Another run (pid ${pid}${space === undefined || space === pidSpace() ? "" : " in another container or PID namespace"}) is already working for this worker. ` +
      `Stop it before starting another; ${file} holds its lock.`,
  );

/**
 * Replaces a lock left behind. The marker lets one start at a time judge and
 * replace it, since removing the file another start has just written would give
 * the lock to both.
 */
function takeOver(file: string, mine: string, judged: string): boolean {
  const marker = `${file}.takeover`;
  try {
    writeFileSync(marker, "", { flag: "wx", mode: 0o600 });
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw error;
    const at = touchedAt(marker);
    if (at !== undefined && Date.now() - at >= TAKEOVER_STALE_MS) rmSync(marker, { force: true });
    sleep(20);
    return false;
  }
  try {
    if (readIfThere(file) !== judged) return false;
    const temp = `${file}.${process.pid}.${randomBytes(4).toString("hex")}.tmp`;
    writeFileSync(temp, mine, { mode: 0o600 });
    renameSync(temp, file);
    return true;
  } finally {
    rmSync(marker, { force: true });
  }
}

/**
 * Takes the lock in `file` for this process until it exits; refuses while another
 * run holds it, in this PID namespace or another sharing the folder. The run
 * touches the lock every few seconds, and `lost` is called if another took it
 * over, as can happen to a run frozen for longer than a lock lasts.
 */
export function lock(file: string, lost: () => void = () => process.exit(1), watchMs = LOCK_WATCH_MS): () => void {
  mkdirSync(dirname(file), { recursive: true, mode: 0o700 });
  const mine = JSON.stringify({ pid: process.pid, space: pidSpace(), run: randomBytes(4).toString("hex") });
  for (;;) {
    try {
      writeFileSync(file, mine, { flag: "wx", mode: 0o600 });
      break;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw error;
    }
    const text = readIfThere(file);
    // The holder released it since the write failed, so the next try takes it.
    if (text === undefined) continue;
    const holder = holderOf(text);
    if (isHeld(file, holder, watchMs)) throw held(holder.pid, holder.space, file);
    if (takeOver(file, mine, text)) break;
  }
  const beat = setInterval(() => {
    try {
      if (readIfThere(file) !== mine) {
        clearInterval(beat);
        return lost();
      }
      const now = new Date();
      utimesSync(file, now, now);
    } catch {
      // A disk that fails for a moment is no reason to drop a task; the next beat tries again.
    }
  }, LOCK_BEAT_MS);
  beat.unref();
  const release = () => {
    clearInterval(beat);
    if (readIfThere(file) === mine) rmSync(file, { force: true });
  };
  process.once("exit", release);
  return release;
}

/**
 * Moves the state 0.3.0 and earlier kept per address alone to `file`, once,
 * when it was kept for `board`, and says whether it did. State for the other
 * network stays where it is until a run there moves it.
 */
function migrate(old: string, file: string, board: string): boolean {
  let text: string;
  try {
    text = readFileSync(`${old}.json`, "utf8");
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return false;
    throw error;
  }
  if (parse(text)?.board !== board.toLowerCase()) return false;
  // A run from before the move may still be working on this network's tasks from the old file.
  const left = readIfThere(`${old}.lock`);
  const holder = left === undefined ? undefined : holderOf(left);
  if (holder && isHeld(`${old}.lock`, holder, LOCK_WATCH_MS)) throw held(holder.pid, holder.space, `${old}.lock`);
  if (readIfThere(`${file}.json`) !== undefined) return false;
  // Removed rather than moved: this run already holds the new lock.
  rmSync(`${old}.lock`, { force: true });
  renameSync(`${old}.json`, `${file}.json`);
  return true;
}

/**
 * Takes the worker's lock on one network and loads its saved state. Each
 * network has its own `<address>.<network>.json` and `.lock`, so one key can
 * run on testnet and mainnet at once without sharing cursors or tasks.
 */
export function openStore(address: string, network: Network, log: (line: string) => void = console.log, dir = stateDir()): Store {
  const old = join(dir, address);
  const file = `${old}.${network.id}`;
  lock(`${file}.lock`, () => {
    log(`another run took over ${file}.lock, so this one stops`);
    process.exit(1);
  });
  if (migrate(old, file, network.contracts.taskBoard)) log(`moved ${old}.json to ${file}.json`);
  return fileStore(`${file}.json`, network.contracts.taskBoard, (message) => log(`warning: ${message}`));
}
