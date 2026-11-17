import { encodeFunctionData, parseAbi, verifyMessage, type Address, type Hex } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { describe, expect, it, vi } from "vitest";

import { TESTNET } from "./network.js";
import { argumentsOf, FLOORS, createReporter, createWatch, fetchProof, judge, MAX_CHECKED, MAX_FINDINGS, outcome, REPORT_PREFIX, UNREADABLE_MS, ReportRefused, requireWatcher, type QueuedChange, type Report, type WatchChain } from "./watch.js";

const TX: Hex = `0x${"ab".repeat(32)}`;
const BOARD: Address = TESTNET.contracts.taskBoard;
const abi = parseAbi([
  "function setParameters(uint16 changeThresholdBps, uint64 timelock, uint32 houseTasksPerDay, uint128 maxHouseBounty, uint128 houseSpendPerDay)",
  "function setFee(uint16 feeBps, address feeRouter)",
  "function setWorkerAllowed(address account, bool allowed)",
  "function setOwner(address owner)",
  "function setPaused(bool paused)",
  "function transfer(address to, uint256 amount)",
]);

const change = (changeId: bigint, data: Hex, target: Address = BOARD): QueuedChange => ({ changeId, decisionId: changeId, target, data, eta: 1_800_000_000n, block: 10n });

function fakeChain(options: { queued?: QueuedChange[]; open?: boolean; decisions?: bigint[]; gate?: boolean } = {}) {
  const vetoes: string[] = [];
  const counts = options.decisions ?? [3n];
  let round = 0;
  const chain: WatchChain = {
    account: "0x00000000000000000000000000000000000000C1",
    head: vi.fn(async () => 3_000n),
    queued: vi.fn(async () => options.queued ?? []),
    open: vi.fn(async () => options.open ?? true),
    decisions: vi.fn(async () => counts[Math.min(round++, counts.length - 1)]!),
    ...(options.gate === false
      ? {}
      : {
          veto: vi.fn(async (changeId: bigint, why: string) => {
            vetoes.push(`${changeId}: ${why}`);
            return TX;
          }),
        }),
  };
  return { chain, vetoes };
}

describe("judging changes", () => {
  it("reads a call's static words and applies the constitution's floors", () => {
    const fine = encodeFunctionData({ abi, functionName: "setParameters", args: [6_000, 86_400n, 5, 2_000_000n, 10_000_000n] });
    expect(argumentsOf(fine)).toEqual([6_000n, 86_400n, 5n, 2_000_000n, 10_000_000n]);
    expect(judge(fine)).toEqual({ name: "setParameters", broken: [] });
    const low = encodeFunctionData({ abi, functionName: "setParameters", args: [5_000, 3_600n, 25, 2_000_000n, 10_000_000n] });
    expect(judge(low).broken).toEqual(["the change bar falls below 60%", "the timelock falls below 24 hours", "more than 20 house tasks a day"]);
    expect(judge(encodeFunctionData({ abi, functionName: "setFee", args: [600, BOARD] })).broken).toEqual(["a protocol fee above 5%"]);
    expect(judge(encodeFunctionData({ abi, functionName: "setWorkerAllowed", args: [BOARD, true] })).broken).toEqual([]);
    expect(judge(encodeFunctionData({ abi, functionName: "setOwner", args: [BOARD] })).broken).toEqual(["a call the monitor does not know, which counts as breaking a floor"]);
  });

  it("knows exactly the calls the constitution's page names, and any other breaks a floor", () => {
    expect(Object.values(FLOORS).map((floor) => floor.name).sort()).toEqual(["setConfig", "setFee", "setModel", "setParameters", "setPaused", "setWorkerAllowed", "transfer"]);
    expect(judge("0x8f5a168f" as Hex).broken).toEqual(["a call the monitor does not know, which counts as breaking a floor"]);
  });

  it("says what a known call with no floor does, in place of calling it within the constitution", () => {
    const transfer = encodeFunctionData({ abi, functionName: "transfer", args: [BOARD, 1_000_000_000_000n] });
    expect(judge(transfer)).toEqual({ name: "transfer", broken: [], does: "moves house treasury funds" });
    expect(judge(encodeFunctionData({ abi, functionName: "setPaused", args: [true] })).does).toBe("pauses or resumes new posts");
    expect(judge(encodeFunctionData({ abi, functionName: "setWorkerAllowed", args: [BOARD, true] })).does).toBe("allows or removes a worker");
  });
});

describe("requireWatcher", () => {
  const withWatcher = (watcher: WatchChain["watcher"]) => ({ ...fakeChain().chain, watcher });
  const OTHER: Address = "0x00000000000000000000000000000000000000D2";

  it("refuses a key that is not the gate's watcher, naming both addresses and the way out", async () => {
    const chain = withWatcher(async () => OTHER);
    await expect(requireWatcher(chain, () => undefined)).rejects.toThrow(
      `This key cannot veto: the gate's watcher is ${OTHER}, not ${chain.account}. Set BRAINCHAIN_WORKER_KEY to the watcher's key, or run watch without --veto.`,
    );
  });

  it("takes the watcher's key, whatever the address's case", async () => {
    const log = vi.fn();
    await requireWatcher(withWatcher(async () => "0x00000000000000000000000000000000000000c1"), log);
    expect(log).not.toHaveBeenCalled();
  });

  it("says so and keeps watching when the watcher cannot be read", async () => {
    const log = vi.fn();
    await requireWatcher(
      withWatcher(async () => {
        throw new Error("Could not reach rpc.example");
      }),
      log,
    );
    expect(log).toHaveBeenCalledWith("could not read the gate's watcher (Could not reach rpc.example); it is read again before any veto");
  });
});

describe("watch", () => {
  const lines: string[] = [];
  const log = (line: string) => lines.push(line);

  it("says a change is within the constitution when it has floors and crosses none, to the second", async () => {
    lines.length = 0;
    const fine = encodeFunctionData({ abi, functionName: "setFee", args: [300, BOARD] });
    const { chain } = fakeChain({ queued: [{ ...change(1n, fine), eta: 1_800_000_040n }] });
    expect(await createWatch({ network: TESTNET, chain, veto: false, log }).round()).toEqual({ findings: 0, incomplete: false });
    expect(lines[0]).toBe(`change 1: setFee on ${BOARD}, within the constitution, runs after 2027-01-15 08:00:40 UTC`);
  });

  it("lists a treasury transfer as moving funds no floor covers, and not as a finding", async () => {
    lines.length = 0;
    const transfer = encodeFunctionData({ abi, functionName: "transfer", args: [BOARD, 1_000_000_000_000n] });
    const { chain, vetoes } = fakeChain({ queued: [change(4n, transfer)] });
    expect(await createWatch({ network: TESTNET, chain, veto: true, log }).round()).toEqual({ findings: 0, incomplete: false });
    expect(lines[0]).toBe(`change 4: transfer on ${BOARD} moves house treasury funds, which no floor covers, runs after 2027-01-15 08:00:00 UTC`);
    expect(vetoes).toEqual([]);
  });

  it("reports a change within the constitution and leaves it alone", async () => {
    lines.length = 0;
    const { chain, vetoes } = fakeChain({ queued: [change(1n, encodeFunctionData({ abi, functionName: "setWorkerAllowed", args: [BOARD, true] }))] });
    const watch = createWatch({ network: TESTNET, chain, veto: true, log });
    expect(await watch.round()).toEqual({ findings: 0, incomplete: false });
    expect(lines[0]).toMatch(/^change 1: setWorkerAllowed on 0x7A7cC.* allows or removes a worker, which no floor covers, runs after 2027-01-15 08:00:00 UTC$/);
    expect(vetoes).toEqual([]);
    // A later round does not judge the same change again.
    await watch.round();
    expect(lines.filter((l) => l.startsWith("change 1")).length).toBe(1);
  });

  it("vetoes a change that crosses a floor through the gate, with the reason", async () => {
    lines.length = 0;
    const bad = encodeFunctionData({ abi, functionName: "setFee", args: [600, BOARD] });
    const { chain, vetoes } = fakeChain({ queued: [change(2n, bad)] });
    const watch = createWatch({ network: TESTNET, chain, veto: true, log });
    expect(await watch.round()).toEqual({ findings: 1, incomplete: false });
    expect(vetoes).toEqual(["2: Breaks the constitution: a protocol fee above 5%"]);
    expect(lines).toEqual([
      "change 2: setFee on 0x7A7cC5D35A642CCc268C7B263fF800bc7eBD52A4 breaks the constitution (a protocol fee above 5%), runs after 2027-01-15 08:00:00 UTC",
      `vetoed change 2 through the guardian gate: ${TX}`,
    ]);
  });

  it("only reports without --veto, and says when there is no gate to veto through", async () => {
    lines.length = 0;
    const bad = encodeFunctionData({ abi, functionName: "setFee", args: [600, BOARD] });
    const reporting = fakeChain({ queued: [change(2n, bad)] });
    expect(await createWatch({ network: TESTNET, chain: reporting.chain, veto: false, log }).round()).toEqual({ findings: 1, incomplete: false });
    expect(reporting.vetoes).toEqual([]);
    const gateless = fakeChain({ queued: [change(2n, bad)], gate: false });
    await createWatch({ network: TESTNET, chain: gateless.chain, veto: true, log }).round();
    expect(lines.at(-1)).toBe("cannot veto: BrainChain testnet has no guardian gate this worker can reach");
  });

  it("does not count a change that has closed, with or without --veto, and says so in the past tense", async () => {
    lines.length = 0;
    const bad = encodeFunctionData({ abi, functionName: "setFee", args: [600, BOARD] });
    const fine = encodeFunctionData({ abi, functionName: "setWorkerAllowed", args: [BOARD, true] });
    for (const veto of [false, true]) {
      const closed = fakeChain({ queued: [change(2n, bad), change(3n, fine)], open: false });
      expect(await createWatch({ network: TESTNET, chain: closed.chain, veto, log }).round()).toEqual({ findings: 0, incomplete: false });
      expect(closed.vetoes).toEqual([]);
    }
    expect(lines.slice(0, 2)).toEqual([
      `change 2: setFee on ${BOARD} broke the constitution (a protocol fee above 5%); closed, it has run or was vetoed`,
      `change 3: setWorkerAllowed on ${BOARD}; closed, it has run or was vetoed`,
    ]);
  });

  it("tries a veto again every round until it lands, after a failed read or a failed send", async () => {
    lines.length = 0;
    const bad = encodeFunctionData({ abi, functionName: "setFee", args: [600, BOARD] });
    const failing = fakeChain({ queued: [change(2n, bad)] });
    vi.mocked(failing.chain.open).mockRejectedValueOnce(new Error("RPC hiccup"));
    const afterRead = createWatch({ network: TESTNET, chain: failing.chain, veto: true, log });
    await expect(afterRead.round()).rejects.toThrow("RPC hiccup");
    await afterRead.round();
    expect(failing.vetoes).toEqual(["2: Breaks the constitution: a protocol fee above 5%"]);

    const refused = fakeChain({ queued: [change(2n, bad)] });
    vi.mocked(refused.chain.veto!).mockRejectedValueOnce(new Error("nonce too low"));
    const afterSend = createWatch({ network: TESTNET, chain: refused.chain, veto: true, log });
    expect((await afterSend.round()).findings).toBe(1);
    expect(lines.at(-1)).toBe("veto of change 2 failed, tried again next round: nonce too low");
    expect((await afterSend.round()).findings).toBe(1);
    expect(lines.at(-1)).toBe(`vetoed change 2 through the guardian gate: ${TX}`);
    await afterSend.round();
    expect(refused.vetoes).toHaveLength(1);
  });

  it("stops trying a veto once the change has closed", async () => {
    lines.length = 0;
    const bad = encodeFunctionData({ abi, functionName: "setFee", args: [600, BOARD] });
    const { chain, vetoes } = fakeChain({ queued: [change(2n, bad)] });
    vi.mocked(chain.veto!).mockRejectedValueOnce(new Error("nonce too low"));
    const watch = createWatch({ network: TESTNET, chain, veto: true, log });
    await watch.round();
    vi.mocked(chain.open).mockResolvedValue(false);
    await watch.round();
    expect(lines.at(-1)).toBe("change 2 is closed already, nothing to veto");
    await watch.round();
    expect(chain.veto).toHaveBeenCalledOnce();
    expect(vetoes).toEqual([]);
  });

  it("notes where the decision log stands, then re-verifies every new decision", async () => {
    lines.length = 0;
    const { chain } = fakeChain({ decisions: [3n, 5n] });
    const verify = vi.fn(async (id: bigint) => ({ findings: id === 5n ? ["record hash: does not match payloadHash"] : [] }));
    const watch = createWatch({ network: TESTNET, chain, verify, veto: false, log });
    await watch.round();
    expect(lines).toEqual(["3 decisions recorded so far; new ones are checked from here"]);
    expect(await watch.round()).toEqual({ findings: 1, incomplete: false });
    expect(verify.mock.calls.map((c) => c[0])).toEqual([4n, 5n]);
    expect(lines.slice(1)).toEqual(["decision 4 verified", "decision 5 does not verify: record hash: does not match payloadHash"]);
  });
});

describe("a one-shot run", () => {
  it("checks the latest decisions on a first run, then what was added since", async () => {
    const { chain } = fakeChain({ decisions: [12n] });
    const verify = vi.fn(async () => ({ findings: [] }));
    const seen: bigint[] = [];
    const first = createWatch({ network: TESTNET, chain, verify, veto: false, log: () => {}, recent: 3n, saw: (n) => seen.push(n) });
    await first.round();
    expect(verify.mock.calls.map((c) => (c as unknown as [bigint])[0])).toEqual([10n, 11n, 12n]);
    expect(seen).toEqual([12n]);

    verify.mockClear();
    const next = fakeChain({ decisions: [14n] }).chain;
    await createWatch({ network: TESTNET, chain: next, verify, veto: false, log: () => {}, seenDecision: 12n, recent: 3n }).round();
    expect(verify.mock.calls.map((c) => (c as unknown as [bigint])[0])).toEqual([13n, 14n]);
  });

  it("starts over when the log has fewer decisions than the count it kept", async () => {
    const { chain } = fakeChain({ decisions: [2n] });
    const verify = vi.fn(async () => ({ findings: [] }));
    await createWatch({ network: TESTNET, chain, verify, veto: false, log: () => {}, seenDecision: 34n, recent: 10n }).round();
    expect(verify.mock.calls.map((c) => (c as unknown as [bigint])[0])).toEqual([1n, 2n]);
  });
});

describe("what a decision's checks come to", () => {
  const check = (name: string, status: "ok" | "fail" | "skip" | "error", message = name) => ({ name, status, message });

  it("treats fail as a finding and error as could not be checked, a real failure winning over what could not be read", async () => {
    await expect(outcome({ checks: [check("read", "ok"), check("threshold", "skip")] })).resolves.toEqual({ findings: [] });
    await expect(outcome({ checks: [check("record-hash", "fail", "differs")] })).resolves.toEqual({ findings: ["record-hash: differs"] });
    await expect(outcome({ checks: [check("fetch", "error", "could not fetch")] })).rejects.toThrow("fetch: could not fetch");
    await expect(outcome({ checks: [check("answer", "fail", "differs"), check("fetch", "error", "could not fetch")] })).resolves.toEqual({ findings: ["answer: differs"] });
  });

  it("names the hash checks a withheld record leaves unrun, is no finding, and fetches nothing more", async () => {
    const refetch = vi.fn(async () => new Uint8Array());
    await expect(outcome({ withheld: true, payloadURI: "https://records.example/1.json", checks: [check("fetch", "ok"), check("record-hash", "skip"), check("input-hash", "skip"), check("levels", "skip")] }, { refetch })).resolves.toEqual({ findings: [], withheld: ["record-hash", "input-hash"] });
    expect(refetch).not.toHaveBeenCalled();
    await expect(outcome({ withheld: true, checks: [check("answer", "fail", "differs"), check("record-hash", "skip")] })).resolves.toEqual({ findings: ["answer: differs"] });
  });
});

describe("a withheld decision", () => {
  it("is listed as withheld with the checks that did not run, neither verified nor a finding, and is not reported as re-verified", async () => {
    const { chain } = fakeChain({ decisions: [3n] });
    const lines: string[] = [];
    const reports: Parameters<Report>[] = [];
    const seen: bigint[] = [];
    const watch = createWatch({
      network: TESTNET,
      chain,
      veto: false,
      log: (l) => lines.push(l),
      seenDecision: 1n,
      recent: 10n,
      saw: (n) => seen.push(n),
      verify: async (id) => (id === 2n ? { findings: [], withheld: ["record-hash", "input-hash"] } : { findings: [], record: new Uint8Array([1]) }),
      report: async (...args) => (reports.push(args), "reported"),
    });
    expect(await watch.round()).toEqual({ findings: 0, incomplete: false });
    expect(lines).toEqual(["decision 2 withheld: its record is served without the work, so record-hash and input-hash did not run; the checks that ran agree with the chain", "decision 3 verified", "reported"]);
    expect(reports[0]![0].map((c) => c.id)).toEqual([3n]);
    expect(seen).toEqual([3n]);
  });
});

describe("a round that cannot finish", () => {
  const verified = { findings: [] };
  const record = new TextEncoder().encode('{"kind":"hire"}');

  it("stops at a decision it could not check, keeps its place there and says the round is incomplete", async () => {
    const { chain } = fakeChain({ decisions: [5n] });
    const lines: string[] = [];
    const seen: bigint[] = [];
    const verify = vi.fn(async (id: bigint) => {
      if (id === 4n) throw new Error("Missing or invalid\n  parameters");
      return verified;
    });
    const first = createWatch({ network: TESTNET, chain, verify, veto: false, log: (l) => lines.push(l), seenDecision: 2n, recent: 10n, saw: (n) => seen.push(n) });
    expect(await first.round()).toEqual({ findings: 0, incomplete: true });
    expect(verify.mock.calls.map((c) => c[0])).toEqual([3n, 4n]);
    expect(seen).toEqual([3n]);
    expect(lines.at(-1)).toBe("decision 4 could not be checked, so it is tried again next round: Missing or invalid parameters");

    verify.mockClear();
    const next = createWatch({ network: TESTNET, chain, verify: async (id) => (verify(id), verified), veto: false, log: () => {}, seenDecision: seen.at(-1), recent: 10n, saw: (n) => seen.push(n) });
    expect(await next.round()).toEqual({ findings: 0, incomplete: false });
    expect(seen.at(-1)).toBe(5n);
  });

  it("goes on to the next decision in a later round of a long watch", async () => {
    const { chain } = fakeChain({ decisions: [2n, 4n, 4n] });
    const verify = vi.fn(async (_id: bigint) => verified);
    verify.mockImplementationOnce(async () => {
      throw new Error("RPC down");
    });
    const watch = createWatch({ network: TESTNET, chain, verify, veto: false, log: () => {} });
    await watch.round();
    expect((await watch.round()).incomplete).toBe(true);
    expect((await watch.round()).incomplete).toBe(false);
    expect(verify.mock.calls.map((c) => c[0])).toEqual([3n, 3n, 4n]);
  });

  it("sends the report before saving its place, and only warns when the save fails", async () => {
    const { chain } = fakeChain({ decisions: [2n] });
    const lines: string[] = [];
    const report = vi.fn(async () => "reported");
    const watch = createWatch({
      network: TESTNET,
      chain,
      verify: async () => ({ findings: [], record: new Uint8Array([1]) }),
      report,
      veto: false,
      log: (l) => lines.push(l),
      seenDecision: 0n,
      recent: 10n,
      saw: () => {
        throw new Error("EACCES: permission denied");
      },
    });
    expect(await watch.round()).toEqual({ findings: 0, incomplete: false });
    expect(report).toHaveBeenCalledOnce();
    expect(lines.slice(-2)).toEqual(["reported", "warning: could not save how far this got, so the next run checks these decisions again: EACCES: permission denied"]);
  });

  it("keeps its place when the report did not reach the service, and flags a refusal too, moving on since sending again would not change it", async () => {
    const run = async (failure: Error) => {
      const { chain } = fakeChain({ decisions: [2n] });
      const seen: bigint[] = [];
      const watch = createWatch({
        network: TESTNET,
        chain,
        verify: async () => ({ findings: [], record: new Uint8Array([1]) }),
        report: async () => {
          throw failure;
        },
        veto: false,
        log: () => {},
        seenDecision: 0n,
        recent: 10n,
        saw: (n) => seen.push(n),
      });
      return { ...(await watch.round()), seen };
    };
    expect(await run(new Error("503 from the service"))).toEqual({ findings: 0, incomplete: true, seen: [0n] });
    expect(await run(new ReportRefused("The report was signed too long ago."))).toEqual({ findings: 0, incomplete: true, seen: [2n] });
  });

  describe("a record that cannot be read", () => {
    const RECORDED = "2026-11-06 12:00:00 UTC";
    const at = Date.parse(RECORDED);
    const young = at + UNREADABLE_MS - 1;
    const old = at + UNREADABLE_MS;
    // What the verifier answers when the record's host does not: a check with status error, not a throw.
    const dead = { recordedAt: RECORDED, checks: [{ name: "read", status: "ok" as const, message: "read" }, { name: "fetch", status: "error" as const, message: "could not fetch the record: 503" }] };
    const OLD_FINDING = "the record could not be read a day or more after it was recorded: fetch: could not fetch the record: 503";

    function rig(verify: (id: bigint) => ReturnType<NonNullable<Parameters<typeof createWatch>[0]["verify"]>>, seenDecision = 224n) {
      const { chain } = fakeChain({ decisions: [226n] });
      const lines: string[] = [];
      const seen: bigint[] = [];
      const reports: Parameters<Report>[] = [];
      const watch = createWatch({
        network: TESTNET,
        chain,
        verify,
        veto: false,
        log: (l) => lines.push(l),
        seenDecision,
        recent: 10n,
        saw: (n) => seen.push(n),
        report: async (...args) => (reports.push(args), "reported"),
      });
      return { watch, lines, seen, reports };
    }

    it("holds the place while the decision is under a day old, and a later run checks it again", async () => {
      const first = rig(async (id) => (id === 225n ? outcome(dead, { now: young }) : { findings: [] }));
      expect(await first.watch.round()).toEqual({ findings: 0, incomplete: true });
      expect(first.seen).toEqual([224n]);
      expect(first.reports).toEqual([]);
      expect(first.lines.at(-1)).toBe("decision 225 could not be checked, so it is tried again next round: fetch: could not fetch the record: 503");
      const next = rig(async () => ({ findings: [] }), first.seen.at(-1));
      expect(await next.watch.round()).toEqual({ findings: 0, incomplete: false });
      expect(next.lines).toEqual(["decision 225 verified", "decision 226 verified"]);
      expect(next.seen).toEqual([226n]);
    });

    it("becomes a finding a day after the decision's block time, goes to the service once, and the place moves on", async () => {
      const verify = vi.fn(async (id: bigint) => (id === 225n ? outcome(dead, { now: old }) : { findings: [], record }));
      const first = rig(verify);
      expect(await first.watch.round()).toEqual({ findings: 1, incomplete: false });
      expect(verify.mock.calls.map((c) => c[0])).toEqual([225n, 226n]);
      expect(first.seen).toEqual([226n]);
      expect(first.lines[0]).toBe(`decision 225 does not verify: ${OLD_FINDING}`);
      expect(first.reports).toEqual([[[{ id: 226n, proof: fetchProof(record, "0x00000000000000000000000000000000000000C1") }], [{ id: 225n, checks: [OLD_FINDING] }]]]);
      // A later run starts past it, so it is reported once.
      const next = rig(verify, first.seen.at(-1));
      expect(await next.watch.round()).toEqual({ findings: 0, incomplete: false });
      expect(verify).toHaveBeenCalledTimes(2);
      expect(next.reports).toEqual([]);
    });

    it("holds the place when the decision's time is unknown, since nothing says the limit has passed", async () => {
      await expect(outcome({ checks: dead.checks } as never, { now: old })).rejects.toThrow("fetch: could not fetch the record: 503");
      await expect(outcome({ ...dead, recordedAt: "not a time" } as never, { now: old })).rejects.toThrow("fetch: could not fetch the record: 503");
    });

    it("applies the same rule to a verified record's failed refetch", async () => {
      const verified = { recordedAt: RECORDED, payloadURI: "https://records.example/1.json", checks: [{ name: "read", status: "ok", message: "read" }] } as never;
      const refetch = vi.fn(async () => record);
      await expect(outcome(verified, { refetch, now: young })).resolves.toEqual({ findings: [], record });
      expect(refetch).toHaveBeenCalledWith("https://records.example/1.json");
      const failing = async () => Promise.reject(new Error("503 from https://records.example/1.json"));
      await expect(outcome(verified, { refetch: failing, now: young })).rejects.toThrow("503 from https://records.example/1.json");
      await expect(outcome(verified, { refetch: failing, now: old })).resolves.toEqual({ findings: ["the record could not be read a day or more after it was recorded: 503 from https://records.example/1.json"] });
      // No key, nothing to report, so no second fetch.
      await expect(outcome(verified, { now: old })).resolves.toEqual({ findings: [] });
    });
  });
});

describe("reporting rounds", () => {
  const worker = privateKeyToAccount(`0x${"7".repeat(64)}`);
  const record = new TextEncoder().encode('{"kind":"hire"}');

  it("sends a signed report of the decisions re-verified and the findings, and logs the service's answer", async () => {
    const calls: { url: string; body: { report: string; signature: Hex } }[] = [];
    const fetcher = (async (url: string | URL | Request, init?: RequestInit) => {
      calls.push({ url: String(url), body: JSON.parse(String(init?.body)) as { report: string; signature: Hex } });
      return new Response(JSON.stringify({ checked: 3, mark: null, markAfter: 10 }), { status: 200 });
    }) as typeof fetch;
    const report = createReporter(TESTNET, worker, fetcher);
    const line = await report([{ id: 4n, proof: fetchProof(record, worker.address) }], [{ id: 5n, checks: ["record-hash: differs"] }]);
    expect(line).toBe("reported to BrainChain testnet: 3 of the 10 re-verified decisions that earn the watchtower mark");
    expect(calls[0]!.url).toBe(`${TESTNET.service}/watchtowers/reports`);
    const sent = JSON.parse(calls[0]!.body.report) as { worker: string; chainId: number; log: string; checked: unknown[]; findings: unknown[] };
    expect(sent).toMatchObject({ worker: worker.address, chainId: TESTNET.chainId, log: TESTNET.contracts.log, findings: [{ id: 5, checks: ["record-hash: differs"] }] });
    expect(sent.checked).toEqual([{ id: 4, proof: fetchProof(record, worker.address) }]);
    expect(await verifyMessage({ address: worker.address, message: `${REPORT_PREFIX}${calls[0]!.body.report}`, signature: calls[0]!.body.signature })).toBe(true);
  });

  it("names the mark once the service grants it, and the refusal when it does not take the report", async () => {
    const granted = createReporter(TESTNET, worker, (async () => new Response(JSON.stringify({ checked: 12, mark: { since: "2026-11-02", checked: 12 } }), { status: 200 })) as typeof fetch);
    expect(await granted([{ id: 1n, proof: fetchProof(record, worker.address) }], [])).toBe("reported to BrainChain testnet: 12 decisions re-verified in all, watchtower mark since 2026-11-02");
    const refused = createReporter(TESTNET, worker, (async () => new Response(JSON.stringify({ error: "The proof for decision 1 does not match its record." }), { status: 400 })) as typeof fetch);
    await expect(refused([{ id: 1n, proof: fetchProof(record, worker.address) }], [])).rejects.toThrow("The proof for decision 1 does not match its record.");
  });

  it("sends a long round in several reports, each signed later than the last, so no decision is passed unreported", async () => {
    const reports: { checked: { id: number }[]; findings: unknown[]; at: number }[] = [];
    const fetcher = (async (_url: string | URL | Request, init?: RequestInit) => {
      reports.push(JSON.parse((JSON.parse(String(init?.body)) as { report: string }).report));
      return new Response(JSON.stringify({ checked: 1, mark: null, markAfter: 10 }), { status: 200 });
    }) as typeof fetch;
    const proof = fetchProof(record, worker.address);
    const checked = Array.from({ length: MAX_CHECKED * 2 + 1 }, (_, i) => ({ id: BigInt(i + 1), proof }));
    const findings = Array.from({ length: MAX_FINDINGS + 1 }, (_, i) => ({ id: BigInt(1_000 + i), checks: ["differs"] }));
    await createReporter(TESTNET, worker, fetcher)(checked, findings);
    expect(reports.map((r) => [r.checked.length, r.findings.length])).toEqual([[MAX_CHECKED, MAX_FINDINGS], [MAX_CHECKED, 1], [1, 0]]);
    expect(reports.flatMap((r) => r.checked.map((c) => c.id))).toEqual(checked.map((c) => Number(c.id)));
    expect(reports[1]!.at).toBeGreaterThan(reports[0]!.at);
    expect(reports[2]!.at).toBeGreaterThan(reports[1]!.at);
  });

  it("reports after a round that re-verified decisions, with the proof bound to the worker, and goes on when the service refuses", async () => {
    const { chain } = fakeChain({ decisions: [2n, 4n, 5n] });
    const lines: string[] = [];
    const reports: Parameters<Report>[] = [];
    let refuse = false;
    const watch = createWatch({
      network: TESTNET,
      chain,
      veto: false,
      log: (line) => lines.push(line),
      verify: async (id) => (id === 4n ? { findings: ["record-hash: differs"] } : { findings: [], record }),
      report: async (checked, findings) => {
        reports.push([checked, findings]);
        if (refuse) throw new ReportRefused("The report was signed too long ago.");
        return "reported";
      },
    });
    await watch.round();
    expect(reports).toEqual([]);
    await watch.round();
    expect(reports).toEqual([[[{ id: 3n, proof: fetchProof(record, chain.account) }], [{ id: 4n, checks: ["record-hash: differs"] }]]]);
    expect(lines.at(-1)).toBe("reported");
    refuse = true;
    await watch.round();
    expect(reports).toHaveLength(2);
    expect(lines.at(-1)).toBe("report not taken: The report was signed too long ago.");
  });

  it("sends nothing without a reporter or when a round re-verified nothing", async () => {
    const { chain } = fakeChain({ decisions: [2n, 2n, 3n] });
    const reports: unknown[] = [];
    const watch = createWatch({ network: TESTNET, chain, veto: false, log: () => {}, verify: async () => ({ findings: [] }), report: async (...args) => (reports.push(args), "reported") });
    await watch.round();
    await watch.round();
    expect(reports).toEqual([]);
    // Verified without a record (the refetch failed): nothing to prove, so nothing is sent.
    await watch.round();
    expect(reports).toEqual([]);
  });
});
