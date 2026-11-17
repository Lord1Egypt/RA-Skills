import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { encodeAbiParameters, encodeEventTopics, parseAbi, parseEther, zeroAddress, type Address, type Hex, type Log } from "viem";
import { describe, expect, it, vi } from "vitest";

import type { Settlement } from "./chain.js";
import { collectionAbi, createSettlementWatch, mint, mintedToken, type ProofsChain } from "./mint.js";
import { MAINNET, TESTNET, type Network } from "./network.js";
import { fileStore, memoryStore, type Store } from "./state.js";

const ACCOUNT: Address = "0x00000000000000000000000000000000000000C1";
const TX: Hex = `0x${"fe".repeat(32)}`;
const PRICE = parseEther("0.001");
const NOW = 1_800_000_000;
const BOARD = MAINNET.contracts.taskBoard;
const PENDING = `https://brain.usebrainchain.com/proofs/274663/pending/${ACCOUNT}`;

/** A Proofs chain that records what it is asked to send, in order. */
function fakeChain(options: { weth?: bigint; eth?: bigint; opensAt?: bigint } = {}) {
  const sent: string[] = [];
  let weth = options.weth ?? parseEther("0.01");
  let opensAt = options.opensAt ?? 0n;
  let tokenId = 28n;
  const chain = {
    account: ACCOUNT,
    price: vi.fn(async () => PRICE),
    weth: vi.fn(async () => weth),
    ethBalance: vi.fn(async () => options.eth ?? parseEther("0.001")),
    faucetOpensAt: vi.fn(async () => opensAt),
    claimWeth: vi.fn(async () => {
      sent.push("faucet");
      weth += parseEther("1");
      opensAt = BigInt(NOW + 86_400);
    }),
    approve: vi.fn(async (amount: bigint) => void sent.push(`approve ${amount}`)),
    mint: vi.fn(async () => {
      sent.push("mint");
      weth -= PRICE;
      tokenId += 1n;
      return { tokenId, tx: TX };
    }),
  } satisfies ProofsChain;
  return { chain, sent };
}

const listing = (body: unknown, status = 200) => vi.fn<typeof fetch>(async () => Response.json(body, { status }));

async function mintRun(chain: ProofsChain, fetcher: typeof fetch, options: { dry?: boolean; count?: number; network?: Network } = {}) {
  const lines: string[] = [];
  await mint(options.network ?? MAINNET, chain, { count: options.count, dry: options.dry ?? false, log: (line) => lines.push(line), fetcher, now: () => NOW });
  return lines;
}

const LAG = "`mint --dry` lists these tasks until the service has seen these mints, which can take minutes. A mint before then, here or by `run --mint`, pays for another piece.";

describe("mint", () => {
  it("approves the price and mints one piece for each task the service lists, and prints the task, token id and hash", async () => {
    const { chain, sent } = fakeChain();
    const fetcher = listing({ tasks: ["12", "15", "12"] });
    const lines = await mintRun(chain, fetcher);
    expect(fetcher.mock.calls[0]![0]).toBe(PENDING);
    // The list spans the sets and ids restart on each board, so the second 12 is another task.
    expect(sent).toEqual([`approve ${PRICE}`, "mint", `approve ${PRICE}`, "mint", `approve ${PRICE}`, "mint"]);
    expect(lines).toEqual([
      "Minting 3 Proofs on Robinhood Chain at 0.001 WETH each plus gas...",
      `Minted Proof 29 for task 12 (${TX}).`,
      `Minted Proof 30 for task 15 (${TX}).`,
      `Minted Proof 31 for task 12 (${TX}).`,
      LAG,
    ]);
  });

  it("sends nothing on a dry run", async () => {
    const { chain, sent } = fakeChain();
    const lines = await mintRun(chain, listing({ tasks: ["12", "15", "18"] }), { dry: true });
    expect(sent).toEqual([]);
    expect(lines).toEqual(["Dry run, nothing sent: mint would mint 3 Proofs on Robinhood Chain for tasks 12, 15 and 18, at 0.001 WETH each plus gas."]);
  });

  it("says exactly how much WETH is missing, and sends nothing", async () => {
    const { chain, sent } = fakeChain({ weth: parseEther("0.0005") });
    await expect(mintRun(chain, listing({ tasks: ["12", "15"] }))).rejects.toThrow(
      `${ACCOUNT} holds 0.0005 WETH on Robinhood Chain, and 2 Proofs cost 0.002 WETH plus gas. ` +
        "Send it 0.0015 WETH (0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73) on Robinhood Chain. Then run mint again.",
    );
    expect(sent).toEqual([]);
    expect(await mintRun(chain, listing({ tasks: ["12"] }), { dry: true })).toEqual([
      "Dry run, nothing sent: mint would mint 1 Proof on Robinhood Chain for task 12, at 0.001 WETH each plus gas.",
      `${ACCOUNT} holds 0.0005 WETH on Robinhood Chain, and 1 Proof costs 0.001 WETH plus gas. Send it 0.0005 WETH (0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73) on Robinhood Chain.`,
    ]);
  });

  it("says the wallet needs ETH on Robinhood Chain for gas", async () => {
    const { chain, sent } = fakeChain({ eth: 0n });
    await expect(mintRun(chain, listing({ tasks: ["12"] }))).rejects.toThrow(
      `${ACCOUNT} holds 0.01 WETH and no ETH on Robinhood Chain, and 1 Proof costs 0.001 WETH plus gas. Send it a little ETH there for gas. Then run mint again.`,
    );
    expect(sent).toEqual([]);
  });

  it("claims test WETH from the faucet on testnet when the wallet is short and the faucet is open", async () => {
    const { chain, sent } = fakeChain({ weth: 0n });
    const fetcher = listing({ tasks: ["4"] });
    const lines = await mintRun(chain, fetcher, { network: TESTNET });
    expect(fetcher.mock.calls[0]![0]).toBe(`https://brain.testnet.usebrainchain.com/proofs/274630/pending/${ACCOUNT}`);
    expect(sent).toEqual(["faucet", `approve ${PRICE}`, "mint"]);
    expect(lines).toEqual(["Claiming test WETH from the faucet...", "Minting 1 Proof on Robinhood Chain testnet at 0.001 WETH each plus gas...", `Minted Proof 29 for task 4 (${TX}).`, LAG]);

    const dry = fakeChain({ weth: 0n });
    expect((await mintRun(dry.chain, listing({ tasks: ["4"] }), { network: TESTNET, dry: true })).at(-1)).toBe(
      "The wallet is short of WETH, so mint would claim test WETH from the faucet first.",
    );
    expect(dry.sent).toEqual([]);
  });

  it("says when the test WETH faucet opens again for the wallet", async () => {
    const { chain, sent } = fakeChain({ weth: 0n, opensAt: BigInt(NOW + 3_600) });
    await expect(mintRun(chain, listing({ tasks: ["4"] }), { network: TESTNET })).rejects.toThrow(
      `${ACCOUNT} holds 0 WETH on Robinhood Chain testnet, and 1 Proof costs 0.001 WETH plus gas. ` +
        "The test WETH faucet allows one claim a day, and this wallet can claim again at 2027-01-15T09:00:00Z. Then run mint again.",
    );
    expect(sent).toEqual([]);
  });

  it("mints at most 10 a run, or --count, and says how many tasks are left", async () => {
    const tasks = Array.from({ length: 12 }, (_, i) => String(i + 1));
    const all = fakeChain({ weth: parseEther("1") });
    expect((await mintRun(all.chain, listing({ tasks }))).slice(-2)).toEqual(["2 more paid tasks wait for a Proof, for a later mint.", LAG]);
    expect(all.chain.mint).toHaveBeenCalledTimes(10);

    const one = fakeChain();
    const lines = await mintRun(one.chain, listing({ tasks: ["12", "15"] }), { count: 1 });
    expect(one.chain.mint).toHaveBeenCalledOnce();
    expect(lines.slice(-2)).toEqual(["1 more paid task waits for a Proof, for a later mint.", LAG]);
  });

  it("says so when no paid task waits for a Proof", async () => {
    const { chain } = fakeChain();
    expect(await mintRun(chain, listing({ tasks: [] }))).toEqual([
      `The BrainChain service lists no paid task of ${ACCOUNT} waiting for a Proof, so there is nothing to mint.`,
    ]);
    expect(chain.price).not.toHaveBeenCalled();
  });

  it("names a service that does not list the tasks yet, or answers in a form it cannot read", async () => {
    const { chain } = fakeChain();
    await expect(mintRun(chain, listing({ error: "Not Found" }, 404))).rejects.toThrow(
      "The BrainChain service at brain.usebrainchain.com does not list the tasks waiting for a Proof yet",
    );
    await expect(mintRun(chain, listing({}, 502))).rejects.toThrow("The BrainChain service at brain.usebrainchain.com answered 502");
    for (const body of [{}, { tasks: "1" }, { tasks: [1] }, { tasks: ["0x1"] }, null]) {
      await expect(mintRun(chain, listing(body))).rejects.toThrow("in a form the worker cannot read");
    }
    expect(chain.mint).not.toHaveBeenCalled();
  });
});

describe("mintedToken", () => {
  const COLLECTION: Address = "0x324B52EE2182641ec29652076ab541bc9F9907d2";
  const WETH: Address = "0x1F852eF3Afa13156b807204d838BbB46B4b452eb";
  const erc20Transfer = parseAbi(["event Transfer(address indexed from, address indexed to, uint256 value)"]);
  const log = (address: Address, topics: Hex[], data: Hex = "0x"): Log => ({
    address,
    topics: topics as [Hex, ...Hex[]],
    data,
    blockHash: `0x${"11".repeat(32)}`,
    blockNumber: 1n,
    logIndex: 0,
    transactionHash: TX,
    transactionIndex: 0,
    removed: false,
  });
  const piece = (address: Address, from: Address, to: Address, tokenId: bigint) =>
    log(address, encodeEventTopics({ abi: collectionAbi, eventName: "Transfer", args: { from, to, tokenId } }) as Hex[]);

  it("reads the token id from the collection's Transfer from the zero address to the worker", () => {
    const logs = [
      log(WETH, encodeEventTopics({ abi: erc20Transfer, eventName: "Transfer", args: { from: ACCOUNT, to: COLLECTION } }) as Hex[], encodeAbiParameters([{ type: "uint256" }], [PRICE])),
      piece("0x00000000000000000000000000000000000000d1", zeroAddress, ACCOUNT, 7n),
      piece(COLLECTION, zeroAddress, "0x00000000000000000000000000000000000000e1", 8n),
      piece(COLLECTION, zeroAddress, ACCOUNT, 29n),
    ];
    expect(mintedToken(logs, COLLECTION, ACCOUNT)).toBe(29n);
    expect(mintedToken(logs.slice(0, 3), COLLECTION, ACCOUNT)).toBeUndefined();
  });
});

describe("run's settlement watch", () => {
  const PAID: Settlement = { paid: true, amount: 975_000n, at: BigInt(NOW + 200) };

  function setup(options: { store?: Store; mints?: boolean; network?: Network; fetcher?: ReturnType<typeof listing>; chain?: ReturnType<typeof fakeChain> } = {}) {
    let now = NOW;
    let outcome: Settlement | undefined;
    const { chain, sent } = options.chain ?? fakeChain();
    const settlement = vi.fn(async (_task: bigint) => outcome);
    const log = vi.fn<(message: string) => void>();
    const fetcher = options.fetcher ?? listing({ tasks: ["7"] });
    const store = options.store ?? memoryStore(BOARD);
    const watch = createSettlementWatch({ network: options.network ?? MAINNET, chain, settlement, store, log, mints: options.mints ?? true, fetcher, now: () => now });
    return {
      watch,
      chain,
      sent,
      settlement,
      log,
      fetcher,
      store,
      at: (seconds: number) => void (now = NOW + seconds),
      settle: (value: Settlement | undefined) => void (outcome = value),
    };
  }
  const logged = (log: ReturnType<typeof vi.fn>) => log.mock.calls.map((call) => String(call[0]));
  const stateFile = () => join(mkdtempSync(join(tmpdir(), "brainchain-worker-")), "worker.json");

  it("logs the payment, mints once for the paid task, and a restart does not mint it again", async () => {
    const file = stateFile();
    const first = setup({ store: fileStore(file, BOARD) });
    first.watch.track(7n);
    await first.watch.round();
    expect(first.settlement).not.toHaveBeenCalled();

    first.at(300);
    await first.watch.round();
    expect(first.settlement).toHaveBeenCalledWith(7n);
    expect(first.fetcher).not.toHaveBeenCalled();

    first.settle(PAID);
    first.at(600);
    await first.watch.round();
    expect(first.fetcher.mock.calls[0]![0]).toBe(PENDING);
    expect(first.sent).toEqual([`approve ${PRICE}`, "mint"]);
    expect(logged(first.log)).toEqual(["task 7: paid 0.975 USDG", `minted proof 29 for task 7 (${TX})`]);
    expect(first.store.state.proofs).toEqual({});

    const second = setup({ store: fileStore(file, BOARD) });
    second.settle(PAID);
    second.at(4_000);
    await second.watch.round();
    expect(second.settlement).not.toHaveBeenCalled();
    expect(second.chain.mint).not.toHaveBeenCalled();
  });

  it("tries a task at most once an hour, across a restart", async () => {
    const file = stateFile();
    const first = setup({ store: fileStore(file, BOARD) });
    first.watch.track(7n);
    first.settle(PAID);
    first.at(300);
    first.chain.mint.mockRejectedValueOnce(new Error("The worker was killed here"));
    await first.watch.round();
    expect(logged(first.log)).toEqual(["task 7: paid 0.975 USDG", "task 7: minting its proof failed (The worker was killed here); trying again in an hour"]);

    const second = setup({ store: fileStore(file, BOARD) });
    second.at(300 + 1_800);
    await second.watch.round();
    expect(second.chain.mint).not.toHaveBeenCalled();
    expect(second.fetcher).not.toHaveBeenCalled();

    second.at(300 + 3_600);
    await second.watch.round();
    expect(second.chain.mint).toHaveBeenCalledOnce();
    expect(logged(second.log)).toEqual([`minted proof 29 for task 7 (${TX})`]);
  });

  it("waits for a late listing as long as the worker can still mint, and says so once", async () => {
    // The report's service listed a payment 10.5 minutes after it landed; the worker once gave up after 15.
    const t = setup({ fetcher: listing({ tasks: [] }) });
    t.watch.track(7n);
    t.settle(PAID);
    t.at(300);
    await t.watch.round();
    t.at(200 + 900);
    await t.watch.round();
    t.at(200 + 900 + 300);
    await t.watch.round();
    expect(t.store.state.proofs?.["7"]).toBeDefined();
    expect(logged(t.log)).toEqual([
      "task 7: paid 0.975 USDG",
      "task 7: the BrainChain service does not list it as waiting for a proof yet; checking every 5 minutes until 2027-01-16T07:03:20Z",
    ]);

    t.fetcher.mockImplementation(async () => Response.json({ tasks: ["7"] }));
    t.at(200 + 2 * 3_600);
    await t.watch.round();
    expect(t.chain.mint).toHaveBeenCalledOnce();
    expect(logged(t.log).at(-1)).toBe(`minted proof 29 for task 7 (${TX})`);
  });

  it("leaves a task once the service stops listing it, which it does when the task has its piece", async () => {
    const t = setup({ chain: fakeChain({ weth: 0n }) });
    t.watch.track(7n);
    t.settle(PAID);
    t.at(300);
    await t.watch.round();
    expect(t.chain.mint).not.toHaveBeenCalled();
    t.fetcher.mockImplementation(async () => Response.json({ tasks: [] }));
    t.at(300 + 3_600);
    await t.watch.round();
    expect(t.store.state.proofs).toEqual({});
    expect(logged(t.log).at(-1)).toBe("task 7: the BrainChain service no longer lists it as waiting for a proof, so it has one");
  });

  it("stops trying 23 hours after payment, and says whether the service ever listed the task", async () => {
    const never = setup({ fetcher: listing({ tasks: [] }) });
    never.watch.track(7n);
    never.settle(PAID);
    never.at(300);
    await never.watch.round();
    never.at(200 + 23 * 3_600);
    await never.watch.round();
    expect(never.store.state.proofs).toEqual({});
    expect(logged(never.log).at(-1)).toBe("task 7: the BrainChain service never listed it as waiting for a proof, so the worker minted none");

    const broke = setup({ chain: fakeChain({ weth: 0n }) });
    broke.watch.track(7n);
    broke.settle(PAID);
    broke.at(300);
    await broke.watch.round();
    broke.at(200 + 23 * 3_600);
    await broke.watch.round();
    expect(logged(broke.log).at(-1)).toBe("task 7: no proof minted within a day of payment, so the task joins the public pool");
  });

  it("says why it mints nothing on mainnet each hour: no WETH, no ETH or a service that does not list the tasks yet", async () => {
    const cases = [
      {
        chain: fakeChain({ weth: 0n }),
        fetcher: listing({ tasks: ["7"] }),
        line: `task 7: no proof minted yet. ${ACCOUNT} holds 0 WETH on Robinhood Chain, and 1 Proof costs 0.001 WETH plus gas. Send it 0.001 WETH (0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73) on Robinhood Chain. Trying again in an hour.`,
      },
      {
        chain: fakeChain({ eth: 0n }),
        fetcher: listing({ tasks: ["7"] }),
        line: `task 7: no proof minted yet. ${ACCOUNT} holds 0.01 WETH and no ETH on Robinhood Chain, and 1 Proof costs 0.001 WETH plus gas. Send it a little ETH there for gas. Trying again in an hour.`,
      },
      {
        chain: fakeChain(),
        fetcher: listing({ error: "Not Found" }, 404),
        line: "task 7: no proof minted yet (The BrainChain service at brain.usebrainchain.com does not list the tasks waiting for a Proof yet); trying again in an hour",
      },
    ];
    for (const { chain, fetcher, line } of cases) {
      const t = setup({ chain, fetcher });
      t.watch.track(7n);
      t.settle(PAID);
      t.at(300);
      await t.watch.round();
      expect(logged(t.log)).toEqual(["task 7: paid 0.975 USDG", line]);
      expect(t.sent).toEqual([]);
      t.at(300 + 3_599);
      await t.watch.round();
      expect(t.log).toHaveBeenCalledTimes(2);
      t.at(300 + 3_600);
      await t.watch.round();
      expect(logged(t.log).at(-1)).toBe(line);
    }
  });

  it("says once on testnet that minting needs Robinhood Chain testnet ETH no agent route provides, and when the Proof goes to the pool", async () => {
    const t = setup({ network: TESTNET, chain: fakeChain({ weth: 0n, eth: 0n }), fetcher: listing({ tasks: ["7"] }) });
    t.watch.track(7n);
    t.settle(PAID);
    t.at(300);
    await t.watch.round();
    expect(logged(t.log)).toEqual([
      "task 7: paid 0.975 tUSDG",
      `task 7: no proof minted. ${ACCOUNT} holds 0 WETH and no ETH on Robinhood Chain testnet, and 1 Proof costs 0.001 WETH plus gas. ` +
        "A person can get Robinhood Chain testnet ETH for gas at https://faucet.testnet.chain.robinhood.com, which asks for a browser check and a Google account, " +
        "and send it to this address; BrainChain's gas drip sends ETH on BrainChain testnet only. The worker claims test WETH from the faucet once it has ETH. " +
        "It tries again every hour, without another line, until 2027-01-16T07:03:20Z; an hour later the Proof goes to the public pool. " +
        "Proofs earn no income, and `run` without `--mint` mints none.",
    ]);
    for (const hours of [1, 2, 3]) {
      t.at(300 + hours * 3_600);
      await t.watch.round();
    }
    expect(t.chain.ethBalance).toHaveBeenCalledTimes(4);
    expect(t.log).toHaveBeenCalledTimes(2);
    expect(t.sent).toEqual([]);
  });

  it("claims test WETH from the faucet on testnet", async () => {
    const t = setup({ network: TESTNET, chain: fakeChain({ weth: 0n }), fetcher: listing({ tasks: ["7"] }) });
    t.watch.track(7n);
    t.settle(PAID);
    t.at(300);
    await t.watch.round();
    expect(t.sent).toEqual(["faucet", `approve ${PRICE}`, "mint"]);
    expect(logged(t.log)).toEqual(["task 7: paid 0.975 tUSDG", "claiming test WETH from the faucet", `minted proof 29 for task 7 (${TX})`]);
  });

  it("logs why a task was refunded and any stake slashed, and stops watching one unsettled three days after delivery", async () => {
    const refunded = setup({ network: TESTNET });
    refunded.watch.track(7n);
    refunded.settle({ paid: false, reason: 3, slashed: 0n });
    refunded.at(300);
    await refunded.watch.round();
    expect(logged(refunded.log)).toEqual(["task 7: refunded to its poster: Jev did not accept the work"]);
    expect(refunded.store.state.proofs).toEqual({});

    const slashed = setup({ network: TESTNET });
    slashed.watch.track(46n);
    slashed.settle({ paid: false, reason: 4, slashed: 100n * 10n ** 18n });
    slashed.at(300);
    await slashed.watch.round();
    expect(logged(slashed.log)).toEqual(["task 46: refunded to its poster: Jev ruled for the poster; 100 tBRAIN of the worker's stake was slashed"]);

    const stuck = setup();
    stuck.watch.track(7n);
    stuck.at(86_400);
    await stuck.watch.round();
    expect(stuck.log).not.toHaveBeenCalled();
    stuck.at(3 * 86_400);
    await stuck.watch.round();
    expect(logged(stuck.log)).toEqual(["task 7: not settled three days after delivery, so the worker stops watching it"]);
    expect(stuck.fetcher).not.toHaveBeenCalled();
  });

  it("still logs each outcome under --no-mint, and mints nothing", async () => {
    const t = setup({ mints: false });
    t.watch.track(7n);
    t.watch.track(8n);
    t.at(300);
    t.settlement.mockImplementation(async (task) => (task === 7n ? PAID : { paid: false, reason: 1, slashed: 0n }));
    await t.watch.round();
    expect(logged(t.log)).toEqual(["task 7: paid 0.975 USDG", "task 8: refunded to its poster: the result was not delivered in time"]);
    expect(t.store.state.proofs).toEqual({});
    expect(t.fetcher).not.toHaveBeenCalled();
    expect(t.sent).toEqual([]);
  });

  it("says when it cannot read whether a task settled, and reads again later", async () => {
    const t = setup();
    t.watch.track(7n);
    t.at(300);
    t.settlement.mockRejectedValueOnce(new Error("Could not reach rpc.example.com"));
    await t.watch.round();
    expect(logged(t.log)).toEqual(["task 7: could not read whether it settled (Could not reach rpc.example.com)"]);
    t.at(600);
    t.settle(PAID);
    await t.watch.round();
    expect(logged(t.log).at(-2)).toBe("task 7: paid 0.975 USDG");
  });
});
