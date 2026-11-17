import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";

import { describe, expect, it, vi } from "vitest";

import { processGroup } from "./proc.js";

vi.mock("node:child_process", () => ({ spawnSync: vi.fn() }));
vi.mock("node:fs", () => ({ readFileSync: vi.fn() }));

const noPs = () => vi.mocked(spawnSync).mockReturnValue({ status: null, stdout: "" } as never);

describe("processGroup", () => {
  it("takes the group from ps where there is one", () => {
    vi.mocked(spawnSync).mockReturnValue({ status: 0, stdout: "  555\n" } as never);
    expect(processGroup(4242)).toBe("555");
    expect(spawnSync).toHaveBeenCalledWith("ps", ["-o", "pgid=", "-p", "4242"], { encoding: "utf8" });
  });

  it("reads field 5 of /proc/<pid>/stat without ps, past a name with spaces and parentheses", () => {
    noPs();
    vi.mocked(readFileSync).mockReturnValue("4242 (odd) name (x) S 1 777 888 0 -1 4194560");
    expect(processGroup(4242)).toBe("777");
    expect(readFileSync).toHaveBeenCalledWith("/proc/4242/stat", "utf8");
  });

  it("is undefined when neither ps nor /proc can tell", () => {
    noPs();
    vi.mocked(readFileSync).mockImplementation(() => {
      throw Object.assign(new Error("no such file"), { code: "ENOENT" });
    });
    expect(processGroup(4242)).toBeUndefined();
  });
});
