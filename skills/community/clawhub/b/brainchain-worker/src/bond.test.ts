import { decodeAbiParameters, decodeFunctionData, parseUnits, type Address, type Hex } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { describe, expect, it, vi } from "vitest";

import { bond, bondClaim, bondGas, bondLine, bondStatus, bondTerms, createBondChain, deedPage, BOND_LEAD_SEC, DeedStatus, encodeCheckData, GAS, MIN_BOND, MISSED_TO, proofIndexAbi, Ruling, taskOfCheck, type BondChain, type BondConfig, type BondView, type TaskFacts, type BondTerms } from "./bond.js";
import { Status } from "./chain.js";
import { MAINNET, TESTNET } from "./network.js";

const ACCOUNT: Address = "0x00000000000000000000000000000000000000C1";
const POSTER: Address = "0x00000000000000000000000000000000000000D1";
const INDEX: Address = "0x00000000000000000000000000000000000000f1";
const TX: Hex = `0x${"fe".repeat(32)}`;
const USDG = (n: string) => parseUnits(n, 6);
const NOW = 1_800_000_000n;
const config: BondConfig & { proofIndex: Address } = { ...MAINNET.proofs.bonds!, proofIndex: INDEX };
const offline = (async () => {
  throw new Error("offline");
}) as unknown as typeof fetch;
const page = { deed: { number: "3", url: "https://app.shipped.bond/bonds/3" } };
const shipped = (async () => ({ ok: true, json: async () => page })) as unknown as typeof fetch;
const task = (overrides: Partial<TaskFacts> = {}): TaskFacts => ({ poster: POSTER, bounty: USDG("1"), deadline: NOW + 86_400n, status: Status.Hired, model: `0x${"0".repeat(24)}${ACCOUNT.slice(2)}`, ...overrides });
const view = (overrides: Partial<BondView> = {}): BondView => ({ deed: 4n, task: 12n, board: MAINNET.contracts.taskBoard, amount: USDG("5"), deadline: NOW + 86_400n + BOND_LEAD_SEC, status: DeedStatus.Open, ruling: 0, remainderBps: 0, checkMetAt: 0n, settledAt: 0n, refundTo: POSTER, ...overrides });

function fakeChain(options: { task?: TaskFacts; bonds?: BondView[]; usdg?: bigint; eth?: bigint; allowance?: bigint; owed?: bigint; proof?: bigint; payer?: Address } = {}) {
  return {
    account: ACCOUNT,
    task: vi.fn(async () => options.task),
    now: vi.fn(async () => NOW),
    usdgBalance: vi.fn(async () => options.usdg ?? USDG("100")),
    ethBalance: vi.fn(async () => options.eth ?? parseUnits("0.01", 18)),
    gasPrice: vi.fn(async () => 20_000_000n),
    allowance: vi.fn(async () => options.allowance ?? 0n),
    approve: vi.fn(async () => TX),
    create: vi.fn(async (_terms: BondTerms, _amount: bigint) => ({ deed: 7n, tx: TX })),
    bondsOn: vi.fn(async () => options.bonds ?? []),
    proofOf: vi.fn(async () => options.proof ?? 0n),
    owed: vi.fn(async () => options.owed ?? 0n),
    withdraw: vi.fn(async () => ({ amount: options.owed ?? 0n, tx: TX })),
    payerOf: vi.fn(async () => options.payer),
  } satisfies BondChain;
}

async function run(chain: BondChain, amount: string, options: { yes?: boolean; answer?: string; config?: BondConfig | undefined; network?: typeof MAINNET; fetch?: typeof fetch } = {}) {
  const lines: string[] = [];
  const ask = options.answer === undefined ? undefined : vi.fn(async () => options.answer!);
  await bond(options.network ?? MAINNET, "config" in options ? options.config : config, chain, 12n, { amount: USDG(amount), yes: options.yes ?? false, fetch: options.fetch ?? (async () => { throw new Error("no network in tests"); }), ...(ask ? { ask } : {}), log: (line) => lines.push(line) });
  return { lines, ask };
}

describe("ShippedDeeds' enums", () => {
  it("pins Ruling as the contract declares it: Conceded is 5 and CheckMet 7, and a line reads the settled split, never the ruling number", () => {
    expect(Ruling).toEqual({ None: 0, Accepted: 1, Rejected: 2, Partial: 3, Invalid: 4, Conceded: 5, Default: 6, CheckMet: 7 });
    expect(DeedStatus).toEqual({ None: 0, Open: 1, Ruled: 2, Appealed: 3, Settled: 4 });
    const delivered = view({ status: DeedStatus.Settled, ruling: Ruling.CheckMet, remainderBps: 10_000, settledAt: NOW });
    expect(delivered.ruling).toBe(7);
    expect(bondLine(MAINNET, delivered, { indexed: true, now: NOW })).toContain("delivered at");
    expect(bondLine(MAINNET, view({ status: DeedStatus.Settled, ruling: Ruling.Conceded, remainderBps: 0, settledAt: NOW }), { indexed: false, now: NOW })).toContain(`missed at 2027-01-15T08:00:00Z: no Proof was recorded, so the bond went to ${MISSED_TO}: ${POSTER}`);
  });
});

describe("bondTerms", () => {
  it("builds the terms Shipped's create accepts for a check-only bond, keyed by board and task, with the refund side named", () => {
    const board = MAINNET.contracts.taskBoard;
    const terms = bondTerms(config, { id: 12n, refundTo: POSTER, paidThroughDesk: false, deadline: NOW }, { address: board, chainId: MAINNET.chainId });
    expect(terms.title).toBe("BrainChain task #12");
    expect(Buffer.byteLength(terms.title)).toBeLessThanOrEqual(96);
    expect(Buffer.byteLength(terms.milestone)).toBeLessThanOrEqual(2048);
    expect(terms.milestone).toContain(`proofOf(${board}, 12) >= 1`);
    expect(terms.milestone).toContain(INDEX);
    expect(terms.milestone).toContain(`paid to ${POSTER}, the task's poster`);
    expect(bondTerms(config, { id: 12n, refundTo: ACCOUNT, paidThroughDesk: true, deadline: NOW }, { address: board, chainId: MAINNET.chainId }).milestone).toContain(
      `paid to ${ACCOUNT}, the agent that paid BrainChain's desk for the task`,
    );
    expect(terms).toMatchObject({
      project: "0x0000000000000000000000000000000000000000",
      projectKind: 0,
      asset: "0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168",
      deadline: NOW + 72n * 3_600n,
      verifier: "0x0000000000000000000000000000000000000000",
      backupVerifier: "0x0000000000000000000000000000000000000000",
      appealPanel: "0x0000000000000000000000000000000000000000",
      check: "0x2e7C4F0F2e6079C3B5F7Cd2440308234CBDc537D",
      refundTo: POSTER,
      defaultRemainderBps: 0,
      refundCapBps: 0,
      allowPartial: false,
      verifierGrace: 0,
      backupGrace: 0,
      appealWindow: 0,
      panelWindow: 0,
      appealBond: 0n,
      verifierFee: 0n,
      refundExcluded: [],
    });
    const [target, call, op, threshold] = decodeAbiParameters([{ type: "address" }, { type: "bytes" }, { type: "uint8" }, { type: "uint256" }], terms.checkData);
    expect([target, op, threshold]).toEqual([INDEX, 0, 1n]);
    expect(decodeFunctionData({ abi: proofIndexAbi, data: call })).toEqual({ functionName: "proofOf", args: [board, 12n] });
    expect(taskOfCheck(terms.checkData, INDEX, board)).toBe(12n);
    expect(taskOfCheck(terms.checkData, POSTER, board)).toBeUndefined();
    expect(taskOfCheck(terms.checkData, INDEX, POSTER)).toBeUndefined();
    expect(taskOfCheck(encodeCheckData(INDEX, board, 3n), INDEX, board)).toBe(3n);
  });
});

describe("bond", () => {
  it("shows the all-in cost, asks, then approves and opens the bond", async () => {
    const chain = fakeChain({ task: task() });
    const { lines, ask } = await run(chain, "5", { answer: "y" });
    expect(ask).toHaveBeenCalledWith("Send it? [y/N] ");
    expect(lines[0]).toBe(
      [
        "Bond 5 USDG on task 12 (bounty 1 USDG, deadline 2027-01-16T08:00:00Z).",
        "  Released by the task's Proof: 4.95 USDG back after Shipped's 1% fee (0.05 USDG), collected with `bond claim 12`.",
        "  Missed: if no Proof is recorded by 2027-01-19T08:00:00Z, the 5 USDG goes to 0x00000000000000000000000000000000000000D1, the poster.",
        `  Gas now: about ${(Number(GAS.create + GAS.approve) * 0.02) / 1e9} ETH on Robinhood Chain for the approval and the bond at 0.02 gwei; the claim later costs about ${(Number(GAS.withdraw) * 0.02) / 1e9} ETH.`,
      ].join("\n"),
    );
    expect(chain.approve).toHaveBeenCalledWith(USDG("5"));
    expect(chain.create).toHaveBeenCalledOnce();
    const [terms, amount] = chain.create.mock.calls[0]!;
    expect(amount).toBe(USDG("5"));
    expect(terms.refundTo).toBe(POSTER);
    expect(terms.deadline).toBe(NOW + 86_400n + BOND_LEAD_SEC);
    expect(lines.at(-1)).toBe(`A bond with registry id 7 is open on Shipped (${TX}). \`bond status 12\` follows it. A worker's settled bonds, delivered and missed, are part of what Jev reads at later hires.`);
    expect(bondGas(20_000_000n, true)).toBe((GAS.create + GAS.approve) * 20_000_000n);
  });

  it("skips the approval when the allowance covers the bond, and sends nothing on no", async () => {
    const chain = fakeChain({ task: task(), allowance: USDG("10") });
    const { lines } = await run(chain, "5", { answer: "n" });
    expect(lines[0]).toContain("for the bond at 0.02 gwei");
    expect(lines.at(-1)).toBe("Nothing sent.");
    expect(chain.approve).not.toHaveBeenCalled();
    expect(chain.create).not.toHaveBeenCalled();
    await run(chain, "5", { yes: true });
    expect(chain.approve).not.toHaveBeenCalled();
    expect(chain.create).toHaveBeenCalledOnce();
  });

  it("pays the agent that paid the desk for the task, and refuses a task this wallet paid for", async () => {
    const payer: Address = "0x00000000000000000000000000000000000000E1";
    const chain = fakeChain({ task: task({ poster: "0x00000000000000000000000000000000000000De" }), payer });
    const { lines } = await run(chain, "5", { yes: true });
    expect(chain.payerOf).toHaveBeenCalledWith(12n);
    const [terms] = chain.create.mock.calls[0]!;
    expect(terms.refundTo).toBe(payer);
    expect(terms.milestone).toContain(`paid to ${payer}, the agent that paid BrainChain's desk for the task`);
    expect(lines[0]).toContain(`the 5 USDG goes to ${payer}, the agent that paid for the task.`);
    const own = fakeChain({ task: task({ poster: "0x00000000000000000000000000000000000000De" }), payer: ACCOUNT });
    await expect(run(own, "5", { yes: true })).rejects.toThrow("Task 12 was paid for by this wallet.");
    expect(own.create).not.toHaveBeenCalled();
  });

  it("needs --yes where there is no terminal", async () => {
    const chain = fakeChain({ task: task() });
    await expect(run(chain, "5")).rejects.toThrow("There is no terminal to confirm on. Run again with --yes to send without asking.");
    expect(chain.create).not.toHaveBeenCalled();
  });

  it("refuses a task the wallet posted, an amount under the bounty or under 2 USDG, and a task it cannot bond", async () => {
    for (const [chain, amount, error] of [
      [fakeChain({ task: task({ poster: ACCOUNT }) }), "5", "Task 12 was posted by this wallet."],
      [fakeChain({ task: task({ bounty: USDG("8") }) }), "5", "The bond must be at least the task's bounty, 8 USDG; 5 USDG is under it."],
      [fakeChain({ task: task() }), "1.5", `The bond must be at least ${Number(MIN_BOND) / 1e6} USDG`],
      [fakeChain({ task: undefined }), "5", "There is no task 12 on BrainChain."],
      [fakeChain({ task: task({ status: Status.Hired, model: `0x${"0".repeat(24)}${"a".repeat(40)}` }) }), "5", "Task 12 is not hired to this worker. Bond a task after Jev hires you for it."],
      [fakeChain({ task: task({ status: Status.Paid }) }), "5", "Task 12 is not hired to this worker. Bond a task after Jev hires you for it."],
      [fakeChain({ task: task({ deadline: NOW - 1n }) }), "5", "deadline, 2027-01-15T07:59:59Z, has passed"],
      [fakeChain({ task: task(), bonds: [view()] }), "5", "This worker already has a bond open on task 12 (registry id 4)."],
      [fakeChain({ task: task(), usdg: USDG("4") }), "5", `${ACCOUNT} holds 4 USDG on Robinhood Chain, under the 5 USDG to bond. Nothing was sent.`],
      [fakeChain({ task: task(), eth: 0n }), "5", "holds 0 ETH on Robinhood Chain, under the"],
    ] as const) {
      await expect(run(chain, amount, { yes: true })).rejects.toThrow(error);
      expect(chain.create).not.toHaveBeenCalled();
    }
    // A task hired to this worker can still be bonded; a settled bond on it does not stand in the way.
    const hired = fakeChain({ task: task({ status: Status.Hired, model: `0x${ACCOUNT.slice(2).padStart(64, "0")}` }), bonds: [view({ status: DeedStatus.Settled, remainderBps: 10_000 })] });
    await run(hired, "5", { yes: true });
    expect(hired.create).toHaveBeenCalledOnce();
  });

  it("says when bonds are closed: no registry on testnet, no index yet on mainnet", async () => {
    const chain = fakeChain({ task: task() });
    await expect(run(chain, "5", { yes: true, network: TESTNET, config: TESTNET.proofs.bonds })).rejects.toThrow("Bonds run on Robinhood Chain against Shipped's registry, which BrainChain testnet has no counterpart of.");
    await expect(run(chain, "5", { yes: true, config: { ...MAINNET.proofs.bonds!, proofIndex: undefined } })).rejects.toThrow("Bonds are not open yet: BrainChain's ProofIndex on Robinhood Chain, which a bond's check reads, is not deployed.");
    expect(chain.task).not.toHaveBeenCalled();
  });
});

describe("bond status", () => {
  const facts = (over: Partial<Parameters<typeof bondLine>[2]> = {}) => ({ indexed: false, now: NOW, ...over });
  const deadline = NOW + 86_400n;
  const head = "Bond on task 12 (registry id 4): 5 USDG";

  it("reads a bond on a retired board's task on that board, and names the set", async () => {
    const old = MAINNET.retired![0]!;
    const chain = fakeChain({ bonds: [view({ board: old.taskBoard, deadline: NOW + 3_600n })] });
    const lines: string[] = [];
    await bondStatus(MAINNET, config, chain, 12n, (l) => lines.push(l), (async () => { throw new Error("offline"); }) as typeof fetch);
    expect(chain.proofOf).toHaveBeenCalledWith(12n, old.taskBoard);
    expect(lines[0]).toContain(`(task of set ${old.release})`);
  });

  it("prints each bond's state in one line", async () => {
    const lines: string[] = [];
    await bondStatus(MAINNET, config, fakeChain({ task: task(), bonds: [view({ deadline })] }), 12n, (l) => lines.push(l), offline);
    expect(lines).toEqual([`${head}, open until 2027-01-16T08:00:00Z: waiting for the task to be paid and its Proof recorded`]);
    expect(bondLine(MAINNET, view({ deadline }), facts({ indexed: true }))).toBe(`${head}, open until 2027-01-16T08:00:00Z: the Proof is in the index and BrainChain marks the check shortly`);
    expect(bondLine(MAINNET, view({ deadline, checkMetAt: NOW - 600n }), facts({ indexed: true }))).toBe(`${head}, the Proof is in the index and the check was marked at 2027-01-15T07:50:00Z; BrainChain confirms it after 2027-01-15T08:50:00Z`);
    expect(bondLine(MAINNET, view({ deadline, checkMetAt: NOW - 4_000n }), facts({ indexed: true }))).toContain("BrainChain confirms it shortly");
    lines.length = 0;
    await bondStatus(MAINNET, config, fakeChain(), 12n, (l) => lines.push(l));
    expect(lines).toEqual([`${ACCOUNT} has no bond on task 12.`]);
  });

  it("says a bond on a refunded task will be missed, and reads the task to know", async () => {
    const lines: string[] = [];
    await bondStatus(MAINNET, config, fakeChain({ task: task({ status: Status.Refunded }), bonds: [view({ deadline })] }), 12n, (l) => lines.push(l), offline);
    expect(lines).toEqual([`${head}, open until 2027-01-16T08:00:00Z: the task was refunded, so no Proof will be recorded; it settles after 2027-01-17T09:00:00Z to ${MISSED_TO}: ${POSTER}`]);
    expect(bondLine(MAINNET, view({ deadline }), facts({ taskStatus: Status.Paid }))).toBe(`${head}, open until 2027-01-16T08:00:00Z: the task is paid; waiting for its Proof to be minted and recorded`);
    expect(bondLine(MAINNET, view({ deadline }), facts({ taskStatus: Status.Hired }))).toContain("waiting for the task to be paid and its Proof recorded");
  });

  it("names who a lapsed or missed bond pays, and a Proof that came too late", () => {
    expect(bondLine(MAINNET, view({ deadline: NOW - 1n }), facts())).toBe(`${head}, deadline 2027-01-15T07:59:59Z passed with no Proof recorded; it settles after 2027-01-16T08:59:59Z to ${MISSED_TO}: ${POSTER}`);
    expect(bondLine(MAINNET, view({ deadline: NOW - 1n }), facts({ indexed: true }))).toContain("passed with the Proof in the index and the check unmarked, and Shipped sets no mark after the deadline; it settles after");
    expect(bondLine(MAINNET, view({ status: DeedStatus.Settled, settledAt: NOW }), facts({ indexed: true }))).toBe(`${head}, missed at 2027-01-15T08:00:00Z: the Proof is in the index, but the bond settled without it, so the bond went to ${MISSED_TO}: ${POSTER}`);
  });

  it("reads what the registry owes for a delivered bond: nothing once collected, and bond claim only when something is left", async () => {
    const delivered = view({ status: DeedStatus.Settled, remainderBps: 10_000, settledAt: NOW });
    const say = async (owed: bigint) => {
      const lines: string[] = [];
      const chain = fakeChain({ bonds: [delivered], owed });
      await bondStatus(MAINNET, config, chain, 12n, (l) => lines.push(l), offline);
      expect(chain.owed).toHaveBeenCalledOnce();
      return lines[0];
    };
    expect(await say(0n)).toBe(`${head}, delivered at 2027-01-15T08:00:00Z: the bond less Shipped's 1% fee, 4.95 USDG, was collected: the registry owes this wallet nothing`);
    expect(await say(USDG("6.93"))).toBe(`${head}, delivered at 2027-01-15T08:00:00Z: the bond less Shipped's 1% fee, 4.95 USDG, was credited to this wallet on the registry, which owes it 6.93 USDG in all; \`bond claim 12\` collects that`);
  });
});

describe("bond claim", () => {
  it("withdraws what a delivered bond left, and says when there is nothing to collect", async () => {
    const lines: string[] = [];
    const delivered = view({ status: DeedStatus.Settled, ruling: Ruling.CheckMet, remainderBps: 10_000, settledAt: NOW });
    const chain = fakeChain({ bonds: [delivered], owed: USDG("4.95") });
    await bondClaim(MAINNET, config, chain, 12n, (l) => lines.push(l), offline);
    expect(chain.withdraw).toHaveBeenCalledOnce();
    expect(lines).toEqual(["Claiming 4.95 USDG from Shipped's registry on Robinhood Chain...", `Paid 4.95 USDG to ${ACCOUNT} (${TX}).`]);

    lines.length = 0;
    await bondClaim(MAINNET, config, fakeChain({ bonds: [delivered] }), 12n, (l) => lines.push(l), offline);
    expect(lines).toEqual(["The bond with registry id 4 was delivered and its 4.95 USDG was collected: the registry owes this wallet nothing."]);
    lines.length = 0;
    await bondClaim(MAINNET, config, fakeChain({ bonds: [view({ status: DeedStatus.Settled, ruling: Ruling.Default, settledAt: NOW })] }), 12n, (l) => lines.push(l), offline);
    expect(lines).toEqual([`The bond with registry id 4 was missed: its 5 USDG went to ${MISSED_TO}: ${POSTER}. There is nothing to claim.`]);
  });

  it("gives a bond the number status gives it", async () => {
    const lines: string[] = [];
    const delivered = view({ status: DeedStatus.Settled, ruling: Ruling.CheckMet, remainderBps: 10_000, settledAt: NOW });
    await bondClaim(MAINNET, config, fakeChain({ bonds: [delivered] }), 12n, (l) => lines.push(l), shipped);
    expect(lines).toEqual(["Bond No. 3 was delivered and its 4.95 USDG was collected: the registry owes this wallet nothing."]);
    const open = fakeChain({ task: task({ status: Status.Refunded }), bonds: [view({ deadline: NOW + 86_400n })] });
    await expect(bondClaim(MAINNET, config, open, 12n, () => {}, shipped)).rejects.toThrow(/^Bond No\. 3 on task 12: 5 USDG, open until .*the task was refunded/);
  });

  it("refuses while the bond is open, without a bond, and without gas", async () => {
    const open = fakeChain({ bonds: [view()] });
    await expect(bondClaim(MAINNET, config, open, 12n, () => {}, offline)).rejects.toThrow(/open until .*\. Nothing can be claimed before it settles\./);
    expect(open.withdraw).not.toHaveBeenCalled();
    await expect(bondClaim(MAINNET, config, fakeChain(), 12n, () => {}, offline)).rejects.toThrow(`${ACCOUNT} has no bond on task 12.`);
    const dry = fakeChain({ bonds: [view({ status: DeedStatus.Settled, remainderBps: 10_000 })], owed: USDG("4.95"), eth: 0n });
    await expect(bondClaim(MAINNET, config, dry, 12n, () => {}, offline)).rejects.toThrow(`${ACCOUNT} has no ETH on Robinhood Chain to pay gas for the claim.`);
    expect(dry.withdraw).not.toHaveBeenCalled();
  });
});

describe("who paid for a task, from the service", () => {
  const account = privateKeyToAccount(`0x${"4f".repeat(32)}`);
  const BOARD = MAINNET.contracts.taskBoard;
  const payer: Address = "0x00000000000000000000000000000000000000e1";
  const asked = (body: unknown) => createBondChain(MAINNET, config, account, (async () => Response.json(body)) as unknown as typeof fetch).payerOf(12n);

  it("takes the payer only from an answer about the board this worker reads", async () => {
    await expect(asked({ board: BOARD, task: "12", refundTo: payer })).resolves.toBe(payer);
    await expect(asked({ board: BOARD.toLowerCase(), task: "12", refundTo: null })).resolves.toBeUndefined();
  });

  it("refuses an answer about another board or none, whatever it names: task ids restart with each board", async () => {
    const other: Address = "0x00000000000000000000000000000000000000B2";
    await expect(asked({ board: other, refundTo: payer })).rejects.toThrow(`answered for the task board ${other}, and this worker reads task 12 from ${BOARD}, so who paid for the task cannot be told. Nothing was sent.`);
    await expect(asked({ refundTo: payer })).rejects.toThrow("answered for an unnamed task board");
    await expect(asked({ board: other, refundTo: null })).rejects.toThrow("answered for the task board");
  });
});

describe("deed page", () => {
  const answering = (body: unknown, ok = true) => (async () => ({ ok, json: async () => body })) as unknown as typeof fetch;

  it("reads Shipped's number and link, and stands down on a test bond, an error or no network", async () => {
    expect(await deedPage(4n, answering(page))).toEqual({ number: "3", url: "https://app.shipped.bond/bonds/3" });
    expect(await deedPage(4n, answering({ deed: { number: null, url: null } }))).toBeUndefined();
    expect(await deedPage(4n, answering({}, false))).toBeUndefined();
    expect(await deedPage(4n, (async () => { throw new Error("offline"); }) as unknown as typeof fetch)).toBeUndefined();
  });

  it("names the bond by Shipped's number and page after creating it", async () => {
    const chain = fakeChain({ task: task() });
    const { lines } = await run(chain, "5", { yes: true, fetch: answering(page) });
    expect(lines.at(-1)).toBe(`Bond No. 3 is open on Shipped: https://app.shipped.bond/bonds/3 (${TX}). \`bond status 12\` follows it. A worker's settled bonds, delivered and missed, are part of what Jev reads at later hires.`);
  });

  it("names an open bond by Shipped's number in the refusal of a second", async () => {
    const chain = fakeChain({ task: task(), bonds: [view()] });
    await expect(run(chain, "5", { yes: true, fetch: answering(page) })).rejects.toThrow("This worker already has bond No. 3 open on task 12 (registry id 4, https://app.shipped.bond/bonds/3).");
  });

  it("shows the page on each status line when Shipped knows the bond", async () => {
    const lines: string[] = [];
    const deadline = NOW + 86_400n;
    await bondStatus(MAINNET, config, fakeChain({ task: task(), bonds: [view({ deadline })] }), 12n, (l) => lines.push(l), answering(page));
    expect(lines).toEqual(["Bond No. 3 on task 12: 5 USDG, open until 2027-01-16T08:00:00Z: waiting for the task to be paid and its Proof recorded https://app.shipped.bond/bonds/3"]);
  });
});
