import { describe, it, expect, beforeEach, afterEach } from "vitest";
import fs from "fs";
import os from "os";
import path from "path";
import { SafeStorage } from "../src/storage.js";

describe("SafeStorage", () => {
  let tmpDir: string;
  let storage: SafeStorage;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "dchat-storage-test-"));
    storage = new SafeStorage(tmpDir);
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it("saves and loads identity", () => {
    const identity = { seed: "abcd1234".repeat(8), address: "abc123.def456" };
    storage.save(identity, "my-passphrase");
    expect(storage.exists()).toBe(true);

    const loaded = storage.load("my-passphrase");
    expect(loaded).toEqual(identity);
  });

  it("returns null when file does not exist", () => {
    expect(storage.exists()).toBe(false);
    expect(storage.load("anything")).toBeNull();
  });

  it("rejects wrong passphrase", () => {
    storage.save({ seed: "seed", address: "addr" }, "correct");
    expect(() => storage.load("wrong")).toThrow();
  });

  it("encrypts data at rest (not plaintext)", () => {
    const identity = { seed: "supersecret", address: "myaddr" };
    storage.save(identity, "pass");

    const raw = fs.readFileSync(storage.getFilePath());
    const rawStr = raw.toString("utf-8");
    expect(rawStr).not.toContain("supersecret");
    expect(rawStr).not.toContain("myaddr");
  });

  it("sets restrictive file permissions", () => {
    storage.save({ seed: "s", address: "a" }, "p");
    const stat = fs.statSync(storage.getFilePath());
    const mode = stat.mode & 0o777;
    expect(mode).toBe(0o600);
  });

  it("deletes identity file", () => {
    storage.save({ seed: "s", address: "a" }, "p");
    expect(storage.exists()).toBe(true);
    storage.delete();
    expect(storage.exists()).toBe(false);
  });

  it("handles re-save (overwrite)", () => {
    storage.save({ seed: "old", address: "old-addr" }, "pass1");
    storage.save({ seed: "new", address: "new-addr" }, "pass2");

    expect(() => storage.load("pass1")).toThrow(); // old passphrase no longer works
    const loaded = storage.load("pass2");
    expect(loaded).toEqual({ seed: "new", address: "new-addr" });
  });
});
