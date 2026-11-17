import { existsSync, mkdtempSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { afterAll, beforeAll, describe, expect, it, vi } from "vitest";

import { clearKeyFromEnvironment, keyConfigured, keyText, writeKeyFile } from "./key.js";

const KEY = `0x${"4f".repeat(32)}`;
const dir = () => mkdtempSync(join(tmpdir(), "brainchain-worker-"));
// A handoff file goes in the state folder where the system has no /dev/shm.
beforeAll(() => void vi.stubEnv("HOME", dir()));
afterAll(() => void vi.unstubAllEnvs());

function keyFile(text: string, mode = 0o600): string {
  const file = join(dir(), "worker.key");
  writeFileSync(file, text, { mode });
  return file;
}

describe("keyText", () => {
  it("reads the key from the environment, trimmed; blank counts as unset", () => {
    expect(keyText({ BRAINCHAIN_WORKER_KEY: ` ${KEY}\n` })).toBe(KEY);
    expect(keyText({ BRAINCHAIN_WORKER_KEY: " " })).toBeUndefined();
    expect(keyText({})).toBeUndefined();
  });

  it("reads a key file that holds the key alone, with or without 0x, around whitespace", () => {
    for (const text of [`${KEY}\n`, KEY, KEY.slice(2), `  ${KEY}  \n`, `${KEY}\r\n`, `0X${KEY.slice(2).toUpperCase()}`]) {
      expect(keyText({ BRAINCHAIN_WORKER_KEY_FILE: keyFile(text) })).toBe(text.trim());
    }
  });

  it("says what is wrong with any other key file, without repeating it", () => {
    const cases: [string, string][] = [
      ["", "is empty"],
      [" \n", "is empty"],
      [`export BRAINCHAIN_WORKER_KEY=${KEY}\n`, "holds a line in the form NAME=value"],
      [`BRAINCHAIN_WORKER_KEY="${KEY}"\n`, "holds a line in the form NAME=value"],
      [`BRAINCHAIN_WORKER_KEY=${KEY}\naddress 0x0\n`, "holds more than one line"],
      [`"${KEY}"\n`, "holds the key in quotes"],
      [`'${KEY}'`, "holds the key in quotes"],
      [`${KEY.slice(0, -1)}\n`, "holds 63 hex characters where a key has 64"],
      [`${KEY} # worker\n`, "holds characters that are not hex digits"],
    ];
    for (const [text, problem] of cases) {
      const file = keyFile(text);
      const error = (() => {
        try {
          keyText({ BRAINCHAIN_WORKER_KEY_FILE: file });
        } catch (thrown) {
          return (thrown as Error).message;
        }
      })();
      expect(error, JSON.stringify(text)).toBe(`BRAINCHAIN_WORKER_KEY_FILE names ${file}, which ${problem}. It must hold the key alone: 64 hex characters, with or without 0x`);
      expect(error).not.toContain("4f4f");
    }
  });

  it("warns about a file others can read, and refuses two sources or a file it cannot read, naming no secret", () => {
    const warn = vi.fn();
    const open = keyFile(KEY, 0o644);
    expect(keyText({ BRAINCHAIN_WORKER_KEY_FILE: open }, warn)).toBe(KEY);
    expect(warn).toHaveBeenCalledWith(`warning: other users can read ${open}; run chmod 600 on it`);
    expect(() => keyText({ BRAINCHAIN_WORKER_KEY: KEY, BRAINCHAIN_WORKER_KEY_FILE: open })).toThrow("not both");
    const missing = join(dir(), "absent");
    expect(() => keyText({ BRAINCHAIN_WORKER_KEY_FILE: missing })).toThrow(`names ${missing}, which could not be read (ENOENT)`);
  });

  it("says whether a key is named, without reading the file", () => {
    expect(keyConfigured({ BRAINCHAIN_WORKER_KEY_FILE: "/nowhere" })).toBe(true);
    expect(keyConfigured({ BRAINCHAIN_WORKER_KEY: KEY })).toBe(true);
    expect(keyConfigured({ BRAINCHAIN_WORKER_KEY: " " })).toBe(false);
  });
});

describe("writeKeyFile", () => {
  it("creates the file only its owner can read, with its folder", () => {
    const file = join(dir(), "new", "worker.key");
    writeKeyFile(file, KEY);
    expect(readFileSync(file, "utf8")).toBe(`${KEY}\n`);
    expect(statSync(file).mode & 0o777).toBe(0o600);
    expect(keyText({ BRAINCHAIN_WORKER_KEY_FILE: file })).toBe(KEY);
  });

  it("never replaces an existing key", () => {
    const file = keyFile("the only copy");
    expect(() => writeKeyFile(file, KEY)).toThrow("already exists");
    expect(readFileSync(file, "utf8")).toBe("the only copy");
  });
});

describe("clearKeyFromEnvironment", () => {
  type Execve = NonNullable<typeof process.execve>;

  it("restarts in place without the key, which the new image takes from a file it removes", () => {
    const execve = vi.fn<Execve>();
    const warn = vi.fn();
    const env: NodeJS.ProcessEnv = { BRAINCHAIN_WORKER_KEY: KEY, OTHER: "kept" };
    clearKeyFromEnvironment(KEY, warn, env, execve as Execve);
    expect(warn).not.toHaveBeenCalled();
    const [file, args, passed] = execve.mock.calls[0]!;
    expect(file).toBe(process.execPath);
    expect(args).toEqual([process.execPath, ...process.execArgv, process.argv[1], ...process.argv.slice(2)]);
    expect(args!.join(" ")).not.toContain(KEY);
    expect(passed).not.toHaveProperty("BRAINCHAIN_WORKER_KEY");
    expect(JSON.stringify(passed)).not.toContain(KEY);
    expect(passed).toMatchObject({ OTHER: "kept" });
    const next = { ...(passed as NodeJS.ProcessEnv) };
    const handoff = next.BRAINCHAIN_WORKER_KEY_HANDOFF!;
    expect(statSync(handoff).mode & 0o777).toBe(0o600);
    expect(keyConfigured(next)).toBe(true);
    expect(keyText(next)).toBe(KEY);
    expect(existsSync(handoff)).toBe(false);
    expect(next.BRAINCHAIN_WORKER_KEY_HANDOFF).toBeUndefined();
  });

  it("clears every key variable in the restart, the Solana key's and both file paths included", () => {
    const execve = vi.fn<Execve>();
    const secret = "SOLANASECRETKEYMARKER";
    clearKeyFromEnvironment(KEY, vi.fn(), { BRAINCHAIN_WORKER_KEY: KEY, BRAINCHAIN_SOLANA_KEY: secret, BRAINCHAIN_SOLANA_KEY_FILE: "/keys/sol.json", BRAINCHAIN_WORKER_KEY_FILE: "/keys/w.key", BRAINCHAIN_NETWORK: "mainnet" }, execve as Execve);
    const passed = execve.mock.calls[0]![2] as NodeJS.ProcessEnv;
    expect(Object.keys(passed).sort()).toEqual(["BRAINCHAIN_NETWORK", "BRAINCHAIN_WORKER_KEY_HANDOFF"]);
    expect(JSON.stringify(passed)).not.toContain(secret);
    keyText({ ...passed });
  });

  it("clears a key variable whatever the case of its name, as Windows reads it", () => {
    const execve = vi.fn<Execve>();
    const secret = "SOLANASECRETKEYMARKER";
    clearKeyFromEnvironment(KEY, vi.fn(), { brainchain_worker_key: KEY, Brainchain_Solana_Key: secret, BRAINCHAIN_NETWORK: "mainnet" }, execve as Execve);
    const passed = execve.mock.calls[0]![2] as NodeJS.ProcessEnv;
    expect(Object.keys(passed).sort()).toEqual(["BRAINCHAIN_NETWORK", "BRAINCHAIN_WORKER_KEY_HANDOFF"]);
    expect(JSON.stringify(passed)).not.toContain(secret);
    keyText({ ...passed });
  });

  it("restarts for a Solana key or a key file alone, passing the worker's key on", () => {
    for (const env of [{ BRAINCHAIN_SOLANA_KEY: "s" }, { BRAINCHAIN_SOLANA_KEY_FILE: "/keys/sol.json" }, { BRAINCHAIN_WORKER_KEY_FILE: keyFile(KEY) }]) {
      const execve = vi.fn<Execve>();
      clearKeyFromEnvironment(KEY, vi.fn(), env, execve as Execve);
      const passed = { ...(execve.mock.calls[0]![2] as NodeJS.ProcessEnv) };
      expect(Object.keys(passed)).toEqual(["BRAINCHAIN_WORKER_KEY_HANDOFF"]);
      expect(keyText(passed)).toBe(KEY);
    }
  });

  it("has nothing to do when the key was piped in or the restart already happened", () => {
    const execve = vi.fn<Execve>();
    // What a pipe's path looks like to stat: not a regular file. A restart would put a key piped in to stay out of files in one.
    clearKeyFromEnvironment(KEY, vi.fn(), { BRAINCHAIN_WORKER_KEY_FILE: "/dev/null" }, execve as Execve);
    clearKeyFromEnvironment(KEY, vi.fn(), {}, execve as Execve);
    clearKeyFromEnvironment(KEY, vi.fn(), { BRAINCHAIN_NETWORK: "mainnet" }, execve as Execve);
    expect(execve).not.toHaveBeenCalled();
  });

  it("restarts when something else is set beside a piped key", () => {
    const execve = vi.fn<Execve>();
    clearKeyFromEnvironment(KEY, vi.fn(), { BRAINCHAIN_WORKER_KEY_FILE: "/dev/null", BRAINCHAIN_SOLANA_KEY: "s" }, execve as Execve);
    expect(Object.keys(execve.mock.calls[0]![2] as object)).toEqual(["BRAINCHAIN_WORKER_KEY_HANDOFF"]);
  });

  it("goes on with a warning where it cannot restart, and leaves no file behind", () => {
    const warn = vi.fn();
    // Not undefined, which would pick up the real process.execve and replace the test runner.
    clearKeyFromEnvironment(KEY, warn, { BRAINCHAIN_WORKER_KEY: KEY }, null as unknown as Execve);
    expect(warn.mock.calls[0]![0]).toContain("Node.js 22.15 or later can");

    const failing = vi.fn<Execve>(() => {
      throw new Error("exec format error");
    });
    const env = { BRAINCHAIN_WORKER_KEY: KEY };
    clearKeyFromEnvironment(KEY, warn, env, failing as Execve);
    const handoff = (failing.mock.calls[0]![2] as NodeJS.ProcessEnv).BRAINCHAIN_WORKER_KEY_HANDOFF!;
    expect(existsSync(handoff)).toBe(false);
    expect(warn.mock.calls.at(-1)![0]).toContain("exec format error");
  });

  it("refuses a handoff path that is not its own, and removes nothing", () => {
    const victim = keyFile("someone's file");
    expect(() => keyText({ BRAINCHAIN_WORKER_KEY_HANDOFF: victim })).toThrow("for the worker's own use");
    expect(existsSync(victim)).toBe(true);
  });
});

describe("clearKeyFromEnvironment on Windows", () => {
  it("does not try to restart, writes no handoff file, and says how to keep the key out of the environment", () => {
    const warnings: string[] = [];
    const execve = vi.fn();
    clearKeyFromEnvironment(`0x${"11".repeat(32)}`, (m) => warnings.push(m), { BRAINCHAIN_WORKER_KEY: `0x${"11".repeat(32)}` }, execve as never, "win32");
    expect(execve).not.toHaveBeenCalled();
    expect(warnings).toEqual([expect.stringContaining("BRAINCHAIN_WORKER_KEY_FILE")]);
  });
});
