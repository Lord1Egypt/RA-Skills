import {
  createPublicClient,
  createWalletClient,
  formatEther,
  http,
  parseAbi,
  parseEventLogs,
  zeroAddress,
  type Address,
  type Hex,
  type Log as ReceiptLog,
  type PrivateKeyAccount,
} from "viem";

import { reason, RECEIPT_MS, REFUND_REASONS, type Settlement } from "./chain.js";
import { proofsChainOf, proofsTransport, type Network } from "./network.js";
import type { ProofTask, Store } from "./state.js";
import { stake, usdg, when } from "./standing.js";

export const collectionAbi = parseAbi([
  "function PRICE_QUOTE() view returns (uint256)",
  "function mint(uint256 quantity, uint256 minRoutedTotal) payable",
  "event Transfer(address indexed from, address indexed to, uint256 indexed tokenId)",
  "error SupplyExceeded()",
  "error WalletCapExceeded()",
  "error Ended()",
  "error NotStarted()",
]);

export const wethAbi = parseAbi([
  "function balanceOf(address) view returns (uint256)",
  "function allowance(address owner, address spender) view returns (uint256)",
  "function approve(address spender, uint256 amount) returns (bool)",
  "function faucet() returns (uint256)",
  "function nextFaucetAt(address) view returns (uint256)",
  "error FaucetCoolingDown(uint256 nextAt)",
]);

/** The most pieces one mint run pays for. */
export const MAX_MINT = 10;

/** How often a delivered task's status is read until it settles. */
const STATUS_SEC = 300;
/** Grading, a dispute, its ruling, the appeal window and the ruling on appeal take up to 48 hours on set 3.5.0, so a task unsettled three days after delivery is left. */
const WATCH_SEC = 3 * 86_400;
/** A day after payment the task joins the public pool, so the worker's own attempts stop an hour short of it. */
const OWN_SEC = 23 * 3_600;
/** The least time between two mint attempts for one task. */
const RETRY_SEC = 3_600;
/** The service lists a payment a round or two after it lands, which has taken over ten minutes: this long, the listing is read every minute. */
const LISTING_SEC = 900;

/** What minting needs from the chain the Proofs live on. */
export interface ProofsChain {
  account: Address;
  /** WETH per piece. */
  price(): Promise<bigint>;
  weth(): Promise<bigint>;
  ethBalance(): Promise<bigint>;
  /** When this wallet can next claim from the WETH faucet; 0 for a wallet that never has. */
  faucetOpensAt(): Promise<bigint>;
  claimWeth(): Promise<void>;
  /** Lets the collection take `amount` of WETH, unless the allowance covers it already. */
  approve(amount: bigint): Promise<void>;
  /** Mints one piece to the worker and returns its token id and the transaction's hash. */
  mint(): Promise<{ tokenId: bigint; tx: Hex }>;
}

/** The piece a mint's receipt shows the collection minting to `to`. */
export function mintedToken(logs: ReceiptLog[], collection: Address, to: Address): bigint | undefined {
  // WETH's Transfer shares the event's signature but not its indexed token id, so only the collection's own logs decode.
  return parseEventLogs({ abi: collectionAbi, eventName: "Transfer", args: { from: zeroAddress, to }, logs }).find(
    (log) => log.address.toLowerCase() === collection.toLowerCase(),
  )?.args.tokenId;
}

export function createProofsChain(proofs: Network["proofs"], account: PrivateKeyAccount): ProofsChain {
  const chain = proofsChainOf(proofs);
  const transport = proofsTransport(proofs);
  const client = createPublicClient({ chain, transport, pollingInterval: 1_000 });
  const wallet = createWalletClient({ account, chain, transport });
  const weth = { address: proofs.weth, abi: wethAbi } as const;
  const collection = { address: proofs.collection, abi: collectionAbi } as const;

  async function send(request: Parameters<typeof wallet.writeContract>[0]) {
    const hash = await wallet.writeContract(request);
    const receipt = await client.waitForTransactionReceipt({ hash, timeout: RECEIPT_MS });
    if (receipt.status !== "success") throw new Error(`Transaction ${hash} reverted`);
    return { hash, receipt };
  }

  return {
    account: account.address,
    price: () => client.readContract({ ...collection, functionName: "PRICE_QUOTE" }),
    weth: () => client.readContract({ ...weth, functionName: "balanceOf", args: [account.address] }),
    ethBalance: () => client.getBalance({ address: account.address }),
    faucetOpensAt: () => client.readContract({ ...weth, functionName: "nextFaucetAt", args: [account.address] }),
    async claimWeth() {
      await send({ ...weth, functionName: "faucet" });
    },
    async approve(amount) {
      const current = await client.readContract({ ...weth, functionName: "allowance", args: [account.address, proofs.collection] });
      if (current >= amount) return;
      await send({ ...weth, functionName: "approve", args: [proofs.collection, amount] });
    },
    async mint() {
      const { hash, receipt } = await send({ ...collection, functionName: "mint", args: [1n, 0n] });
      const tokenId = mintedToken(receipt.logs, proofs.collection, account.address);
      if (tokenId === undefined) throw new Error(`The mint ${hash} minted no piece to ${account.address}`);
      return { tokenId, tx: hash };
    },
  };
}

/**
 * The worker's paid tasks the service has bound no piece to, in the order it
 * binds the worker's own mints to them: oldest payment first.
 */
export async function pendingTasks(network: Network, worker: Address, fetcher: typeof fetch = fetch): Promise<bigint[]> {
  const host = new URL(network.service).host;
  const response = await fetcher(`${network.service}/proofs/${network.chainId}/pending/${worker}`, { signal: AbortSignal.timeout(15_000) }).catch(() => {
    throw new Error(`Could not reach the BrainChain service at ${host}`);
  });
  if (!response.ok) {
    await response.body?.cancel();
    if (response.status === 404) throw new Error(`The BrainChain service at ${host} does not list the tasks waiting for a Proof yet`);
    throw new Error(`The BrainChain service at ${host} answered ${response.status} when asked for the tasks waiting for a Proof`);
  }
  const tasks = ((await response.json().catch(() => undefined)) as { tasks?: unknown } | null | undefined)?.tasks;
  if (!Array.isArray(tasks) || !tasks.every((id) => typeof id === "string" && /^\d{1,78}$/.test(id))) {
    throw new Error(`The BrainChain service at ${host} listed the tasks waiting for a Proof in a form the worker cannot read`);
  }
  // Task ids restart with each board and the list spans them, so a repeated id is another task.
  return (tasks as string[]).map((id) => BigInt(id));
}

const proofCount = (n: number) => `${n} Proof${n === 1 ? "" : "s"}`;

/** "task 12", "tasks 12 and 15", "tasks 12, 15 and 18". */
function taskList(tasks: bigint[]): string {
  const ids = tasks.map(String);
  if (ids.length === 1) return `task ${ids[0]}`;
  return `tasks ${ids.slice(0, -1).join(", ")} and ${ids.at(-1)}`;
}

const wall = () => Math.floor(Date.now() / 1000);

/**
 * What the wallet lacks to pay for `count` pieces, if anything. Short of test
 * WETH while the faucet is open, it claims from the faucet first, calling
 * `claiming` as it starts, unless `dry`, which only sets `claim`.
 */
async function afford(
  proofs: Network["proofs"],
  chain: ProofsChain,
  count: number,
  options: { dry: boolean; claiming: () => void; now: () => number },
): Promise<{ price: bigint; missing?: string; claim?: true; noEth?: true }> {
  const [price, eth] = await Promise.all([chain.price(), chain.ethBalance()]);
  const cost = price * BigInt(count);
  let weth = await chain.weth();
  let opensAt = 0n;
  if (weth < cost && proofs.faucet) {
    opensAt = await chain.faucetOpensAt();
    // The claim pays gas too.
    if (opensAt <= BigInt(options.now()) && eth > 0n) {
      if (options.dry) return { price, claim: true };
      options.claiming();
      await chain.claimWeth();
      [weth, opensAt] = await Promise.all([chain.weth(), chain.faucetOpensAt()]);
    }
  }
  const needWeth = weth < cost;
  const needEth = eth === 0n;
  if (!needWeth && !needEth) return { price };
  const fixes: string[] = [];
  if (needWeth && !proofs.faucet) fixes.push(`Send it ${formatEther(cost - weth)} WETH (${proofs.weth}) on ${proofs.name}.`);
  if (needEth) fixes.push(`${proofs.gas}.`);
  if (needWeth && proofs.faucet) {
    fixes.push(
      opensAt <= BigInt(options.now())
        ? "The worker claims test WETH from the faucet once it has ETH."
        : `The test WETH faucet allows one claim a day, and this wallet can claim again at ${when(opensAt)}.`,
    );
  }
  const holds = `${chain.account} holds ${formatEther(weth)} WETH${needEth ? " and no ETH" : ""} on ${proofs.name}`;
  return {
    price,
    missing: `${holds}, and ${proofCount(count)} cost${count === 1 ? "s" : ""} ${formatEther(cost)} WETH plus gas. ${fixes.join(" ")}`,
    ...(needEth ? { noEth: true as const } : {}),
  };
}

/**
 * Mints a piece for each of the worker's paid tasks the service lists without
 * one, up to `count` and at most MAX_MINT, from the worker's key. The service
 * binds each piece the worker mints to its oldest paid task waiting for one.
 */
export async function mint(
  network: Network,
  chain: ProofsChain,
  options: { count?: number; dry: boolean; log: (line: string) => void; fetcher?: typeof fetch; now?: () => number },
): Promise<void> {
  const { log } = options;
  const { proofs } = network;
  const listed = await pendingTasks(network, chain.account, options.fetcher);
  if (listed.length === 0) return log(`The BrainChain service lists no paid task of ${chain.account} waiting for a Proof, so there is nothing to mint.`);
  const batch = listed.slice(0, Math.min(options.count ?? MAX_MINT, MAX_MINT));
  const left = listed.length - batch.length;
  const rest = left > 0 ? ` ${left} more paid task${left === 1 ? " waits" : "s wait"} for a Proof, for a later mint.` : "";
  const funds = await afford(proofs, chain, batch.length, { dry: options.dry, claiming: () => log("Claiming test WETH from the faucet..."), now: options.now ?? wall });
  const each = `${formatEther(funds.price)} WETH each plus gas`;
  if (options.dry) {
    log(`Dry run, nothing sent: mint would mint ${proofCount(batch.length)} on ${proofs.name} for ${taskList(batch)}, at ${each}.${rest}`);
    if (funds.claim) log("The wallet is short of WETH, so mint would claim test WETH from the faucet first.");
    if (funds.missing) log(funds.missing);
    return;
  }
  if (funds.missing) throw new Error(`${funds.missing} Then run mint again.`);
  log(`Minting ${proofCount(batch.length)} on ${proofs.name} at ${each}...`);
  for (const task of batch) {
    await chain.approve(funds.price);
    const { tokenId, tx } = await chain.mint();
    log(`Minted Proof ${tokenId} for task ${task} (${tx}).`);
  }
  if (rest) log(rest.trim());
  // The service scans in rounds and caches the list, so it still shows these tasks for a while.
  log("`mint --dry` lists these tasks until the service has seen these mints, which can take minutes. A mint before then, here or by `run --mint`, pays for another piece.");
}

/**
 * What `run` does once a task is delivered: it watches the task until it
 * settles and logs how: paid and how much, or refunded, why and any stake
 * slashed. With `mints`, it then mints a piece for each paid task, at most once
 * an hour per task, while the service lists the task as waiting for one and
 * the worker can still mint it. The watched tasks live in the state, so a
 * restart neither forgets nor repeats a mint.
 */
export function createSettlementWatch(options: {
  network: Network;
  chain: ProofsChain;
  /** How a task settled on BrainChain, or undefined while it has not. */
  settlement: (task: bigint) => Promise<Settlement | undefined>;
  store: Store;
  log: (message: string) => void;
  /** False under --no-mint. */
  mints: boolean;
  fetcher?: typeof fetch;
  /** Wall-clock seconds. */
  now?: () => number;
}) {
  const { network, chain, store, log } = options;
  const clock = options.now ?? wall;
  const watched = () => (store.state.proofs ??= {});
  const drop = (key: string, why?: string) => {
    delete watched()[key];
    store.save();
    if (why) log(`task ${key}: ${why}`);
  };
  const later = (entry: ProofTask, seconds: number) => {
    entry.nextAt = clock() + seconds;
    store.save();
  };

  /** Reads whether a delivered task settled and logs how; true once it is paid and has a Proof to mint. */
  async function settle(key: string, entry: ProofTask): Promise<boolean> {
    let outcome: Settlement | undefined;
    try {
      outcome = await options.settlement(BigInt(key));
    } catch (error) {
      later(entry, STATUS_SEC);
      log(`task ${key}: could not read whether it settled (${reason(error)})`);
      return false;
    }
    if (outcome === undefined) {
      if (clock() - entry.deliveredAt >= WATCH_SEC) drop(key, "not settled three days after delivery, so the worker stops watching it");
      else later(entry, STATUS_SEC);
      return false;
    }
    if (!outcome.paid) {
      const slashed = outcome.slashed > 0n ? `; ${stake(network, outcome.slashed)} of the worker's stake was slashed` : "";
      drop(key, `refunded to its poster: ${REFUND_REASONS[outcome.reason] ?? `reason ${outcome.reason}`}${slashed}`);
      return false;
    }
    log(`task ${key}: paid ${usdg(network, outcome.amount)}`);
    if (!options.mints) {
      drop(key);
      return false;
    }
    entry.paidAt = Number(outcome.at);
    store.save();
    return true;
  }

  async function mintFor(key: string, entry: ProofTask, listed: bigint[] | Error): Promise<void> {
    const until = entry.paidAt! + OWN_SEC;
    if (clock() >= until) {
      if (Array.isArray(listed) && !listed.includes(BigInt(key)) && !entry.listed) {
        return drop(key, "the BrainChain service never listed it as waiting for a proof, so the worker minted none");
      }
      return drop(key, "no proof minted within a day of payment, so the task joins the public pool");
    }
    if (Array.isArray(listed) && !listed.includes(BigInt(key))) {
      // Once listed, a task leaves the list when it has its piece.
      if (entry.listed) return drop(key, "the BrainChain service no longer lists it as waiting for a proof, so it has one");
      if (clock() - entry.paidAt! < LISTING_SEC) return later(entry, 60);
      if (!entry.waited) {
        entry.waited = true;
        log(`task ${key}: the BrainChain service does not list it as waiting for a proof yet; checking every ${STATUS_SEC / 60} minutes until ${when(BigInt(until))}`);
      }
      return later(entry, STATUS_SEC);
    }
    if (Array.isArray(listed)) entry.listed = true;
    // Counted before anything is sent, so a restart during the mint waits out the hour too.
    later(entry, RETRY_SEC);
    if (listed instanceof Error) return log(`task ${key}: no proof minted yet (${reason(listed)}); trying again in an hour`);
    try {
      const funds = await afford(network.proofs, chain, 1, { dry: false, claiming: () => log("claiming test WETH from the faucet"), now: clock });
      if (funds.missing) {
        if (network.id !== "testnet" || !funds.noEth) return log(`task ${key}: no proof minted yet. ${funds.missing} Trying again in an hour.`);
        // No agent route leads to ETH on Robinhood Chain testnet, so the hourly retries say nothing new.
        if (entry.told) return;
        entry.told = true;
        store.save();
        return log(
          `task ${key}: no proof minted. ${funds.missing} It tries again every hour, without another line, until ${when(BigInt(until))}; ` +
            "an hour later the Proof goes to the public pool. Proofs earn no income, and `run` without `--mint` mints none.",
        );
      }
      await chain.approve(funds.price);
      const { tokenId, tx } = await chain.mint();
      drop(key);
      log(`minted proof ${tokenId} for task ${key} (${tx})`);
    } catch (error) {
      log(`task ${key}: minting its proof failed (${reason(error)}); trying again in an hour`);
    }
  }

  return {
    /** Watches a task the worker just delivered. */
    track(task: bigint): void {
      const now = clock();
      watched()[task.toString()] = { deliveredAt: now, nextAt: now + STATUS_SEC };
      store.save();
    },
    /** Reads every watched task that is due, logs each that settled, and mints for each paid one. */
    async round(): Promise<void> {
      if (store.state.proofs === undefined) return;
      const due = Object.entries(watched()).filter(([, entry]) => clock() >= entry.nextAt);
      const paid: [string, ProofTask][] = [];
      for (const [key, entry] of due) if (entry.paidAt !== undefined || (await settle(key, entry))) paid.push([key, entry]);
      if (paid.length === 0) return;
      // A run under --no-mint after one that minted leaves those tasks' Proofs to `mint`.
      if (!options.mints) {
        for (const [key] of paid) drop(key);
        return;
      }
      const listed = await pendingTasks(network, chain.account, options.fetcher).catch((error: unknown) => (error instanceof Error ? error : new Error(String(error))));
      for (const [key, entry] of paid) await mintFor(key, entry, listed);
    },
  };
}
