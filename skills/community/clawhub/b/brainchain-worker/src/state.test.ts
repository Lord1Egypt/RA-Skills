import { spawn, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, statSync, utimesSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { beforeAll, describe, expect, it, vi } from "vitest";

import { MAINNET, TESTNET } from "./network.js";
import { fileStore, lock, openStore, readWatched, writeWatched } from "./state.js";

const BOARD = "0xC74564F100e70F95346A6e399ebf1Ce14309C8B6";
// Several tests overwrite a lock this process holds, which a run answers by exiting at its next touch.
beforeAll(() => void vi.spyOn(process, "exit").mockImplementation((() => undefined) as never));
const dir = () => mkdtempSync(join(tmpdir(), "brainchain-worker-"));

describe("fileStore", () => {
  it("says what it leaves behind when the board changes, and keeps a copy", () => {
    const file = join(mkdtempSync(join(tmpdir(), "state-")), "state.json");
    const oldBoard = MAINNET.retired![0]!.taskBoard.toLowerCase();
    const saved = JSON.stringify({ board: oldBoard, tasks: {}, done: [], hired: { block: 5, tasks: ["70"] } });
    writeFileSync(file, saved);
    const warn = vi.fn();
    const store = fileStore(file, MAINNET.contracts.taskBoard, warn);
    expect(store.state.hired).toBeUndefined();
    expect(warn).toHaveBeenCalledWith(expect.stringContaining("1 hired tasks"));
    expect(readFileSync(`${file}.${oldBoard}`, "utf8")).toBe(saved);
  });

  it("says nothing when the state left on another board holds no work", () => {
    const file = join(mkdtempSync(join(tmpdir(), "state-")), "state.json");
    writeFileSync(file, JSON.stringify({ board: MAINNET.retired![0]!.taskBoard.toLowerCase(), tasks: {}, done: [] }));
    const warn = vi.fn();
    fileStore(file, MAINNET.contracts.taskBoard, warn);
    expect(warn).not.toHaveBeenCalled();
  });

  it("keeps state in a file only its owner can read", () => {
    const file = join(dir(), "worker.json");
    const store = fileStore(file, BOARD);
    store.state.tasks["7"] = { result: "done", failures: 1, nextAt: 1_060 };
    store.state.hired = { block: 1_234, tasks: ["7"] };
    store.save();
    expect(statSync(file).mode & 0o777).toBe(0o600);
    expect(fileStore(file, BOARD).state).toMatchObject({ tasks: { "7": { result: "done", nextAt: 1_060 } }, hired: { block: 1_234 } });
  });

  it("drops state kept for another task board", () => {
    const file = join(dir(), "worker.json");
    const store = fileStore(file, BOARD);
    store.state.done.push("7");
    store.save();
    expect(fileStore(file, "0x0000000000000000000000000000000000000001").state.done).toEqual([]);
  });

  it("moves a file that is not a saved state aside and starts with no saved work", () => {
    const board = BOARD.toLowerCase();
    const state = (fields: object) => JSON.stringify({ board, tasks: {}, done: [], ...fields });
    const wrong = [
      "{",
      "",
      "null",
      "[]",
      "42",
      '"text"',
      JSON.stringify({ tasks: {}, done: [] }),
      JSON.stringify({ board, done: {} }),
      state({ board: 7 }),
      state({ done: {} }),
      state({ done: ["7", 8] }),
      state({ tasks: "x" }),
      state({ tasks: { "7": { failures: "1", nextAt: 0 } } }),
      state({ tasks: { "7": { failures: 0, nextAt: 1.5 } } }),
      state({ tasks: { "7": { failures: 0, nextAt: 0, stored: { uri: "https://brain.example/7", hash: "0x12" } } } }),
      state({ hired: 5 }),
      state({ hired: { block: 10, tasks: ["abc"] } }),
      state({ command: { pgid: "abc", startedAt: 0 } }),
      state({ command: { pgid: 1, startedAt: 0 } }),
      state({ proofs: [] }),
      state({ proofs: { abc: { deliveredAt: 1, nextAt: 2 } } }),
      state({ proofs: { "7": { deliveredAt: 1, nextAt: "2" } } }),
      state({ proofs: { "7": { deliveredAt: 1, nextAt: 2, paidAt: -1 } } }),
      state({ proofs: { "7": { deliveredAt: 1, nextAt: 2, told: false } } }),
      state({ proofs: { "7": { deliveredAt: 1, nextAt: 2, listed: "yes" } } }),
    ];
    for (const text of wrong) {
      const folder = dir();
      const file = join(folder, "worker.json");
      writeFileSync(file, text);
      const warn = vi.fn();
      const store = fileStore(file, BOARD, warn);
      expect(store.state).toEqual({ board: BOARD.toLowerCase(), tasks: {}, done: [] });
      expect(warn).toHaveBeenCalledOnce();
      expect(warn.mock.calls[0]![0]).toMatch(/could not be read as saved worker state, so it was moved to .*worker\.json\.corrupt-\d{8}T\d{6}Z and this run starts with no saved work$/);
      const [aside] = readdirSync(folder).filter((name) => name.startsWith("worker.json.corrupt-"));
      expect(readFileSync(join(folder, aside!), "utf8")).toBe(text);
      expect(existsSync(file)).toBe(false);
      store.save();
      expect(fileStore(file, BOARD, warn).state.done).toEqual([]);
      expect(warn).toHaveBeenCalledOnce();
    }
  });

  it("keeps a saved state with every field it can hold", () => {
    const file = join(dir(), "worker.json");
    const hash = `0x${"ab".repeat(32)}`;
    const saved = {
      board: BOARD.toLowerCase(),
      tasks: { "7": { result: "done", stored: { uri: "https://brain.example/7", hash }, tx: hash, failures: 2, nextAt: 1_060 } },
      done: ["5"],
      hired: { block: 1_234, tasks: ["7"] },
      command: { pgid: 4_242, startedAt: 1_700_000_000_000 },
      proofs: {
        "7": { deliveredAt: 1_700_000_000, paidAt: 1_700_003_600, nextAt: 1_700_007_200, listed: true, waited: true, told: true },
        "8": { deliveredAt: 1_700_000_100, nextAt: 1_700_000_400 },
      },
    };
    writeFileSync(file, JSON.stringify(saved));
    const warn = vi.fn();
    expect(fileStore(file, BOARD, warn).state).toEqual(saved);
    expect(warn).not.toHaveBeenCalled();
  });
});

const lockPid = (file: string) => (JSON.parse(readFileSync(file, "utf8")) as { pid: number }).pid;
const minuteAgo = () => new Date(Date.now() - 60_000);
/** The PID space this process writes into a lock. */
function ownSpace(): string {
  const file = join(dir(), "probe.lock");
  const release = lock(file);
  const { space } = JSON.parse(readFileSync(file, "utf8")) as { space: string };
  release();
  return space;
}

describe("lock", () => {
  it("refuses while a live process holds it", () => {
    const file = join(dir(), "worker.lock");
    writeFileSync(file, JSON.stringify({ pid: process.ppid, space: ownSpace() }));
    expect(() => lock(file)).toThrow(`pid ${process.ppid}`);
  });

  it("refuses while a live process holds a lock written before locks were touched", () => {
    const file = join(dir(), "worker.lock");
    writeFileSync(file, String(process.ppid));
    expect(() => lock(file)).toThrow(`pid ${process.ppid}`);
  });

  it("refuses while a run from 0.12 or earlier holds its lock, however long ago it wrote it", () => {
    // Pid 1 started before the lock was written, as a 0.12 run did, and 0.12 never touched its lock again.
    const file = join(dir(), "worker.lock");
    writeFileSync(file, "1");
    utimesSync(file, new Date(Date.now() - 20_000), new Date(Date.now() - 20_000));
    expect(() => lock(file)).toThrow("pid 1)");
  });

  it("takes over a bare-pid lock whose pid a process took up after it was written, as pid 1 does after a container restarts", () => {
    const later = spawn("sleep", ["30"], { stdio: "ignore" });
    try {
      const file = join(dir(), "worker.lock");
      writeFileSync(file, String(later.pid));
      utimesSync(file, minuteAgo(), minuteAgo());
      const release = lock(file);
      expect(lockPid(file)).toBe(process.pid);
      release();
    } finally {
      later.kill("SIGKILL");
    }
  });

  it("takes over a lock its holder left behind, and releases it", () => {
    const file = join(dir(), "worker.lock");
    writeFileSync(file, String(spawnSync("true").pid));
    const release = lock(file);
    expect(lockPid(file)).toBe(process.pid);
    release();
    expect(existsSync(file)).toBe(false);
  });

  it("takes over a lock nobody has touched, though some process now has its pid", () => {
    const file = join(dir(), "worker.lock");
    writeFileSync(file, JSON.stringify({ pid: process.ppid, space: ownSpace() }));
    utimesSync(file, minuteAgo(), minuteAgo());
    lock(file)();
  });

  it("refuses while a run in another PID namespace keeps touching its lock, whatever its pid means here", async () => {
    const file = join(dir(), "worker.lock");
    writeFileSync(file, JSON.stringify({ pid: spawnSync("true").pid, space: "another-namespace" }));
    const toucher = spawn("sh", ["-c", `while :; do touch '${file}'; sleep 0.05; done`], { stdio: "ignore" });
    await new Promise((resolve) => setTimeout(resolve, 100));
    try {
      expect(() => lock(file, undefined, 300)).toThrow("in another container or PID namespace");
    } finally {
      toucher.kill("SIGKILL");
    }
  });

  it("takes over at once a lock from another PID namespace that is long untouched, and after a beat one just left", () => {
    const old = join(dir(), "worker.lock");
    writeFileSync(old, JSON.stringify({ pid: process.ppid, space: "another-namespace" }));
    utimesSync(old, minuteAgo(), minuteAgo());
    const started = Date.now();
    lock(old, undefined, 60_000)();
    expect(Date.now() - started).toBeLessThan(5_000);

    const recent = join(dir(), "worker.lock");
    writeFileSync(recent, JSON.stringify({ pid: process.ppid, space: "another-namespace" }));
    lock(recent, undefined, 50)();
  });

  it("counts a lock still being written as held, until it is left long enough to be stale", () => {
    const file = join(dir(), "worker.lock");
    writeFileSync(file, "");
    expect(() => lock(file)).toThrow("Another run");
    utimesSync(file, minuteAgo(), minuteAgo());
    lock(file)();
  });

  it("gets past a takeover marker a crash left behind", () => {
    const file = join(dir(), "worker.lock");
    writeFileSync(file, String(spawnSync("true").pid));
    writeFileSync(`${file}.takeover`, "");
    utimesSync(`${file}.takeover`, minuteAgo(), minuteAgo());
    lock(file)();
    expect(existsSync(`${file}.takeover`)).toBe(false);
  });

  it("touches its lock while it runs, and says so when another run has taken it", () => {
    vi.useFakeTimers({ toFake: ["setInterval", "clearInterval"] });
    try {
      const file = join(dir(), "worker.lock");
      const lost = vi.fn();
      lock(file, lost);
      utimesSync(file, minuteAgo(), minuteAgo());
      vi.advanceTimersByTime(5_000);
      expect(Date.now() - statSync(file).mtimeMs).toBeLessThan(5_000);
      expect(lost).not.toHaveBeenCalled();
      writeFileSync(file, JSON.stringify({ pid: process.ppid, space: "another-namespace" }));
      vi.advanceTimersByTime(5_000);
      expect(lost).toHaveBeenCalledOnce();
    } finally {
      vi.useRealTimers();
    }
  });
});

describe("writeWatched", () => {
  it("keeps the place, each write through a temp file of its own, since runs can overlap", () => {
    const folder = dir();
    const log = "0xABC";
    // A fixed temp name is what two runs would fight over.
    mkdirSync(join(folder, "watch.0xabc.json.tmp"));
    writeWatched(log, 7n, folder);
    writeWatched(log, 9n, folder);
    expect(readWatched(log, folder)).toBe(9n);
    expect(readdirSync(folder).filter((name) => name.endsWith(".tmp"))).toEqual(["watch.0xabc.json.tmp"]);
  });
});

describe("openStore", () => {
  const ADDRESS = "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4";
  const saved = (board: string, done: string[]) => JSON.stringify({ board: board.toLowerCase(), tasks: {}, done, hired: { block: 1_234, tasks: done } });
  const held = (file: string, pid: number) => `Another run (pid ${pid}) is already working for this worker. Stop it before starting another; ${file} holds its lock.`;

  it("moves state kept per address to the network whose board it holds, says so once, and drops its stale lock", () => {
    const folder = dir();
    const old = join(folder, ADDRESS);
    writeFileSync(`${old}.json`, saved(TESTNET.contracts.taskBoard, ["5"]));
    writeFileSync(`${old}.lock`, String(spawnSync("true").pid));
    const log = vi.fn();
    expect(openStore(ADDRESS, TESTNET, log, folder).state).toMatchObject({ done: ["5"], hired: { block: 1_234 } });
    expect(log.mock.calls).toEqual([[`moved ${old}.json to ${old}.testnet.json`]]);
    expect(readdirSync(folder).sort()).toEqual([`${ADDRESS}.testnet.json`, `${ADDRESS}.testnet.lock`]);
    expect(lockPid(`${old}.testnet.lock`)).toBe(process.pid);
    openStore(ADDRESS, TESTNET, log, folder);
    expect(log).toHaveBeenCalledOnce();
  });

  it("leaves state kept for the other board until a run on that network moves it", () => {
    const folder = dir();
    const old = join(folder, ADDRESS);
    const text = saved(MAINNET.contracts.taskBoard, ["5"]);
    writeFileSync(`${old}.json`, text);
    const log = vi.fn();
    expect(openStore(ADDRESS, TESTNET, log, folder).state.done).toEqual([]);
    expect(log).not.toHaveBeenCalled();
    expect(readFileSync(`${old}.json`, "utf8")).toBe(text);
    expect(existsSync(`${old}.testnet.json`)).toBe(false);
    expect(openStore(ADDRESS, MAINNET, log, folder).state.done).toEqual(["5"]);
    expect(log.mock.calls).toEqual([[`moved ${old}.json to ${old}.mainnet.json`]]);
    expect(existsSync(`${old}.json`)).toBe(false);
  });

  it("leaves old state alone once the network has its own", () => {
    const folder = dir();
    const old = join(folder, ADDRESS);
    writeFileSync(`${old}.json`, saved(TESTNET.contracts.taskBoard, ["5"]));
    writeFileSync(`${old}.testnet.json`, saved(TESTNET.contracts.taskBoard, ["9"]));
    const log = vi.fn();
    expect(openStore(ADDRESS, TESTNET, log, folder).state.done).toEqual(["9"]);
    expect(log).not.toHaveBeenCalled();
    expect(existsSync(`${old}.json`)).toBe(true);
  });

  it("refuses while a run from before the move works on this network, and not on the other", () => {
    const folder = dir();
    const old = join(folder, ADDRESS);
    writeFileSync(`${old}.json`, saved(MAINNET.contracts.taskBoard, ["5"]));
    writeFileSync(`${old}.lock`, String(process.ppid));
    expect(() => openStore(ADDRESS, MAINNET, undefined, folder)).toThrow(held(`${old}.lock`, process.ppid));
    expect(existsSync(`${old}.json`)).toBe(true);
    expect(openStore(ADDRESS, TESTNET, undefined, folder).state.done).toEqual([]);
  });

  it("moves state past a lock from before the move whose pid a process took up since", () => {
    const later = spawn("sleep", ["30"], { stdio: "ignore" });
    try {
      const folder = dir();
      const old = join(folder, ADDRESS);
      writeFileSync(`${old}.json`, saved(MAINNET.contracts.taskBoard, ["5"]));
      writeFileSync(`${old}.lock`, String(later.pid));
      utimesSync(`${old}.lock`, minuteAgo(), minuteAgo());
      expect(openStore(ADDRESS, MAINNET, vi.fn(), folder).state.done).toEqual(["5"]);
      expect(existsSync(`${old}.lock`)).toBe(false);
    } finally {
      later.kill("SIGKILL");
    }
  });

  it("runs one key on testnet and mainnet at once, each with its own lock and state", () => {
    const folder = dir();
    const testnet = openStore(ADDRESS, TESTNET, undefined, folder);
    testnet.state.hired = { block: 1_234, tasks: ["7"] };
    testnet.save();
    // Held by a live process from here on, as a testnet run in another terminal would hold it.
    writeFileSync(join(folder, `${ADDRESS}.testnet.lock`), String(process.ppid));

    const mainnet = openStore(ADDRESS, MAINNET, undefined, folder);
    expect(mainnet.state).toEqual({ board: MAINNET.contracts.taskBoard.toLowerCase(), tasks: {}, done: [] });
    mainnet.state.hired = { block: 99, tasks: [] };
    mainnet.save();
    expect(lockPid(join(folder, `${ADDRESS}.mainnet.lock`))).toBe(process.pid);
    expect(readFileSync(join(folder, `${ADDRESS}.testnet.lock`), "utf8")).toBe(String(process.ppid));
    expect(fileStore(join(folder, `${ADDRESS}.testnet.json`), TESTNET.contracts.taskBoard).state.hired).toEqual({ block: 1_234, tasks: ["7"] });
  });

  it("names the network's lock file when another run holds it", () => {
    const folder = dir();
    const file = join(folder, `${ADDRESS}.testnet.lock`);
    writeFileSync(file, String(process.ppid));
    expect(() => openStore(ADDRESS, TESTNET, undefined, folder)).toThrow(held(file, process.ppid));
  });
});
