// A delivery bond on Shipped: the worker locks USDG on Robinhood Chain behind
// a task, and the task's Proof is what releases it. Shipped's check reads
// BrainChain's ProofIndex, proofOf(task) >= 1, so a task that is paid and gets
// its Proof by the bond's deadline returns the bond less Shipped's 1% fee, and
// one that does not pays the bond to the agent that paid for the task.
import {
  createPublicClient,
  createWalletClient,
  decodeAbiParameters,
  decodeFunctionData,
  encodeAbiParameters,
  encodeFunctionData,
  formatEther,
  http,
  isAddress,
  parseAbi,
  parseEventLogs,
  type Address,
  type Hex,
  type PrivateKeyAccount,
} from "viem";

import { taskBoardAbi } from "./abi.js";
import { erc20Abi, RECEIPT_MS, Status } from "./chain.js";
import { chainOf, proofsChainOf, proofsTransport, type Network } from "./network.js";
import { usdg, when } from "./standing.js";

export const proofIndexAbi = parseAbi(["function proofOf(address board, uint256 taskId) view returns (uint256)"]);

const TERMS =
  "(string title, string milestone, address project, uint8 projectKind, address asset, uint64 deadline, address verifier, address backupVerifier, address appealPanel, address check, bytes checkData, address refundTo, uint16 defaultRemainderBps, uint16 refundCapBps, bool allowPartial, uint32 verifierGrace, uint32 backupGrace, uint32 appealWindow, uint32 panelWindow, uint128 appealBond, uint128 verifierFee, address[] refundExcluded)";

export const shippedAbi = parseAbi([
  `function create(${TERMS} t, uint256 deposit) returns (uint256 deedId)`,
  "function withdraw(address asset) returns (uint256)",
  "function owed(address account, address asset) view returns (uint256)",
  "function deedCount() view returns (uint256)",
  "function core(uint256 deedId) view returns (address creator, uint8 status, address asset, uint64 deadline)",
  `function getDeed(uint256 deedId) view returns ((address creator, uint8 status, uint8 ruling, uint16 remainderBps, uint16 feeBps, bool overturned, uint64 createdAt, uint64 ruledAt, uint64 appealedAt, uint64 settledAt, uint64 checkMetAt, uint64 windowEnd, address ruledBy, address appellant, uint256 balance, ${TERMS} terms))`,
  `event DeedCreated(uint256 indexed deedId, address indexed creator, address indexed project, ${TERMS} terms, uint256 deposit, uint16 feeBps)`,
  "error AssetNotAllowed()",
  "error CreationIsPaused()",
  "error InvalidDeadline()",
  "error InvalidRefund()",
  "error NothingOwed()",
]);

/** ShippedDeeds.Status and Ruling. */
export const DeedStatus = { None: 0, Open: 1, Ruled: 2, Appealed: 3, Settled: 4 } as const;
export const Ruling = { None: 0, Accepted: 1, Rejected: 2, Partial: 3, Invalid: 4, Conceded: 5, Default: 6, CheckMet: 7 } as const;
/** Who a missed bond pays, in the words every line about one uses. */
export const MISSED_TO = "the agent that paid BrainChain's desk for the task, or to the poster for a task posted on the board directly";
const BPS = 10_000n;
const ZERO: Address = "0x0000000000000000000000000000000000000000";
/** The bond's deadline is the task's plus this: 48 hours for a grade, a dispute and an appealed ruling on set 3.5.0, then the worker's day to mint. */
export const BOND_LEAD_SEC = 72n * 3_600n;
/** A marked check is confirmed an hour later; a bond with no Proof can be settled a day after that. */
export const CHECK_HOLD_SEC = 3_600n;
export const CHECK_CONFIRM_SEC = 86_400n;
/** Shipped's fee on a released bond, in basis points, as the registry charges it today. */
export const FEE_BPS = 100n;
/** Below this the fee and the gas are too large a share of the bond. */
export const MIN_BOND = 2_000_000n;
/** Gas each transaction takes, measured on a fork of Robinhood Chain (approve 57,976; create 978,948 on a 496-byte milestone; withdraw 61,603), with room. */
export const GAS = { approve: 60_000n, create: 1_100_000n, withdraw: 85_000n };
/** Deeds read per batch, and the most read when the worker's bonds are looked for. */
const DEED_BATCH = 200;
const DEED_SCAN = 5_000;

export interface BondConfig {
  registry: Address;
  check: Address;
  /** Unset until BrainChain's ProofIndex is deployed: no bond can be checked without it. */
  proofIndex?: Address;
  /** The bond asset on Robinhood Chain: the same USDG the task's bounty is in. */
  usdg: Address;
}

export interface BondTerms {
  title: string;
  milestone: string;
  project: Address;
  projectKind: number;
  asset: Address;
  deadline: bigint;
  verifier: Address;
  backupVerifier: Address;
  appealPanel: Address;
  check: Address;
  checkData: Hex;
  refundTo: Address;
  defaultRemainderBps: number;
  refundCapBps: number;
  allowPartial: boolean;
  verifierGrace: number;
  backupGrace: number;
  appealWindow: number;
  panelWindow: number;
  appealBond: bigint;
  verifierFee: bigint;
  refundExcluded: Address[];
}

const checkDataTypes = [{ type: "address" }, { type: "bytes" }, { type: "uint8" }, { type: "uint256" }] as const;

/** StaticCallCheck data: proofOf(board, task) on the index, at least 1. Task ids restart with each board, so the board is part of the key. */
export function encodeCheckData(proofIndex: Address, board: Address, task: bigint): Hex {
  return encodeAbiParameters(checkDataTypes, [proofIndex, encodeFunctionData({ abi: proofIndexAbi, functionName: "proofOf", args: [board, task] }), 0, 1n]);
}

/** The task a bond's check reads on `proofIndex` for `board`, or undefined for any other check. */
export function taskOfCheck(data: Hex, proofIndex: Address, board: Address): bigint | undefined {
  try {
    const [target, call, op, threshold] = decodeAbiParameters(checkDataTypes, data);
    if (target.toLowerCase() !== proofIndex.toLowerCase() || op !== 0 || threshold !== 1n) return undefined;
    const { functionName, args } = decodeFunctionData({ abi: proofIndexAbi, data: call });
    return functionName === "proofOf" && args[0].toLowerCase() === board.toLowerCase() ? args[1] : undefined;
  } catch {
    return undefined;
  }
}

/**
 * The terms of a delivery bond on one task. Shipped's own check decides it, so
 * there is no verifier and no appeal; the refund side is the agent that paid
 * for the task: the poster on the board, or the payer the desk recorded.
 */
export function bondTerms(config: BondConfig & { proofIndex: Address }, task: { id: bigint; refundTo: Address; paidThroughDesk: boolean; deadline: bigint }, board: { address: Address; chainId: number }): BondTerms {
  return {
    title: `BrainChain task #${task.id}`,
    milestone:
      `The Proof NFT for BrainChain task #${task.id} (task board ${board.address} on BrainChain, chain ${board.chainId}) is recorded in BrainChain's ProofIndex at ${config.proofIndex} on Robinhood Chain, ` +
      `read as proofOf(${board.address}, ${task.id}) >= 1. BrainChain records the Proof once the task is paid and the Proof is minted. ` +
      `If no Proof is recorded by the deadline, the bond is paid to ${task.refundTo}, ${task.paidThroughDesk ? "the agent that paid BrainChain's desk for the task" : "the task's poster"}.`,
    project: ZERO,
    projectKind: 0,
    asset: config.usdg,
    deadline: task.deadline + BOND_LEAD_SEC,
    verifier: ZERO,
    backupVerifier: ZERO,
    appealPanel: ZERO,
    check: config.check,
    checkData: encodeCheckData(config.proofIndex, board.address, task.id),
    refundTo: task.refundTo,
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
  };
}

export interface TaskFacts {
  poster: Address;
  bounty: bigint;
  deadline: bigint;
  status: number;
  model: Hex;
}

/** One of the worker's bonds, as the registry holds it. */
export interface BondView {
  deed: bigint;
  task: bigint;
  /** The task board the bond's task is on. */
  board: Address;
  amount: bigint;
  deadline: bigint;
  status: number;
  ruling: number;
  remainderBps: number;
  checkMetAt: bigint;
  settledAt: bigint;
  refundTo: Address;
}

/** What bonding needs from BrainChain and from Robinhood Chain. */
export interface BondChain {
  account: Address;
  /** The task on the board, or undefined when there is none. */
  task(id: bigint, board?: Address): Promise<TaskFacts | undefined>;
  now(): Promise<bigint>;
  usdgBalance(): Promise<bigint>;
  ethBalance(): Promise<bigint>;
  gasPrice(): Promise<bigint>;
  allowance(): Promise<bigint>;
  approve(amount: bigint): Promise<Hex>;
  create(terms: BondTerms, amount: bigint): Promise<{ deed: bigint; tx: Hex }>;
  /** The worker's bonds on one task, newest first. */
  bondsOn(task: bigint): Promise<BondView[]>;
  proofOf(task: bigint, board?: Address): Promise<bigint>;
  owed(): Promise<bigint>;
  withdraw(): Promise<{ amount: bigint; tx: Hex }>;
  /** The agent that paid BrainChain's desk for the task, as the service records it; undefined for a plain on-chain post. */
  payerOf(task: bigint): Promise<Address | undefined>;
}

export function createBondChain(network: Network, config: BondConfig, account: PrivateKeyAccount, fetcher: typeof fetch = fetch): BondChain {
  const brainchain = createPublicClient({ chain: chainOf(network), transport: http(network.rpc, { timeout: 20_000, retryCount: 2 }) });
  const chain = proofsChainOf(network.proofs);
  const transport = proofsTransport(network.proofs);
  const client = createPublicClient({ chain, transport, pollingInterval: 1_000 });
  const wallet = createWalletClient({ account, chain, transport });
  const registry = { address: config.registry, abi: shippedAbi } as const;
  const token = { address: config.usdg, abi: erc20Abi } as const;

  async function send(request: Parameters<typeof wallet.writeContract>[0]) {
    const hash = await wallet.writeContract(request);
    const receipt = await client.waitForTransactionReceipt({ hash, timeout: RECEIPT_MS });
    if (receipt.status !== "success") throw new Error(`Transaction ${hash} reverted`);
    return { hash, receipt };
  }

  return {
    account: account.address,
    async task(id, board = network.contracts.taskBoard) {
      const t = await brainchain.readContract({ address: board, abi: taskBoardAbi, functionName: "get", args: [id] });
      return t.status === 0 ? undefined : { poster: t.poster, bounty: t.bounty, deadline: t.deadline, status: t.status, model: t.model };
    },
    now: async () => (await client.getBlock()).timestamp,
    usdgBalance: () => client.readContract({ ...token, functionName: "balanceOf", args: [account.address] }),
    ethBalance: () => client.getBalance({ address: account.address }),
    gasPrice: () => client.getGasPrice(),
    allowance: () => client.readContract({ ...token, functionName: "allowance", args: [account.address, config.registry] }),
    async approve(amount) {
      return (await send({ ...token, functionName: "approve", args: [config.registry, amount] })).hash;
    },
    async create(terms, amount) {
      const { hash, receipt } = await send({ ...registry, functionName: "create", args: [terms, amount] });
      const created = parseEventLogs({ abi: shippedAbi, eventName: "DeedCreated", args: { creator: account.address }, logs: receipt.logs }).find((log) => log.address.toLowerCase() === config.registry.toLowerCase());
      if (!created) throw new Error(`The bond ${hash} created no deed for ${account.address}`);
      return { deed: created.args.deedId, tx: hash };
    },
    async bondsOn(task) {
      if (!config.proofIndex) return [];
      const count = Number(await client.readContract({ ...registry, functionName: "deedCount" }));
      const mine: bigint[] = [];
      for (let to = count; to > Math.max(0, count - DEED_SCAN); to -= DEED_BATCH) {
        const ids = Array.from({ length: Math.min(DEED_BATCH, to - Math.max(0, count - DEED_SCAN)) }, (_, i) => BigInt(to - i));
        const cores = await client.multicall({ contracts: ids.map((id) => ({ ...registry, functionName: "core", args: [id] }) as const), allowFailure: false });
        ids.forEach((id, i) => {
          if (cores[i]![0].toLowerCase() === account.address.toLowerCase()) mine.push(id);
        });
      }
      if (mine.length === 0) return [];
      const deeds = await client.multicall({ contracts: mine.map((id) => ({ ...registry, functionName: "getDeed", args: [id] }) as const), allowFailure: false });
      return mine.flatMap((deed, i) => {
        const d = deeds[i]!;
        if (d.terms.check.toLowerCase() !== config.check.toLowerCase()) return [];
        const board = [network.contracts.taskBoard, ...(network.retired ?? []).map((r) => r.taskBoard)].find((b) => taskOfCheck(d.terms.checkData, config.proofIndex!, b) === task);
        if (!board) return [];
        return [{ deed, task, board, amount: d.balance, deadline: d.terms.deadline, status: d.status, ruling: d.ruling, remainderBps: d.remainderBps, checkMetAt: d.checkMetAt, settledAt: d.settledAt, refundTo: d.terms.refundTo }];
      });
    },
    proofOf: (task, board = network.contracts.taskBoard) => client.readContract({ address: config.proofIndex!, abi: proofIndexAbi, functionName: "proofOf", args: [board, task] }),
    async payerOf(task) {
      const host = new URL(network.service).host;
      const response = await fetcher(`${network.service}/bonds/refund-to/${task}`, { signal: AbortSignal.timeout(15_000) }).catch(() => {
        throw new Error(`Could not reach the BrainChain service at ${host} to ask who paid for task ${task}`);
      });
      if (!response.ok) {
        await response.body?.cancel();
        throw new Error(`The BrainChain service at ${host} answered ${response.status} when asked who paid for task ${task}`);
      }
      const { board, refundTo } = ((await response.json().catch(() => undefined)) as { board?: unknown; refundTo?: unknown } | undefined) ?? {};
      // Task ids restart with each board, so an answer for another board names who paid for a different task.
      if (typeof board !== "string" || board.toLowerCase() !== network.contracts.taskBoard.toLowerCase()) {
        throw new Error(`The BrainChain service at ${host} answered for ${typeof board === "string" ? `the task board ${board}` : "an unnamed task board"}, and this worker reads task ${task} from ${network.contracts.taskBoard}, so who paid for the task cannot be told. Nothing was sent.`);
      }
      if (refundTo === null || refundTo === undefined) return undefined;
      if (typeof refundTo !== "string" || !isAddress(refundTo)) throw new Error(`The BrainChain service at ${host} named the payer of task ${task} in a form bond cannot read`);
      return refundTo;
    },
    owed: () => client.readContract({ ...registry, functionName: "owed", args: [account.address, config.usdg] }),
    async withdraw() {
      const amount = await client.readContract({ ...registry, functionName: "owed", args: [account.address, config.usdg] });
      const { hash } = await send({ ...registry, functionName: "withdraw", args: [config.usdg] });
      return { amount, tx: hash };
    },
  };
}

/** The ETH the bond's transactions need at this gas price, approval included when one is needed. */
export const bondGas = (gasPrice: bigint, approves: boolean) => (GAS.create + (approves ? GAS.approve : 0n)) * gasPrice;

const fee = (amount: bigint) => (amount * FEE_BPS) / BPS;

/** A bond by Shipped's number when Shipped knows it, and by the registry's id, a different number, when it does not. */
const bondName = (b: BondView, page: DeedPage | undefined) => (page ? `Bond No. ${page.number}` : `The bond with registry id ${b.deed}`);

/** Where a bond stands, in one line. */
export function bondLine(network: Network, b: BondView, facts: { indexed: boolean; now: bigint; page?: DeedPage | undefined; owed?: bigint; taskStatus?: number | undefined }): string {
  const { indexed, now, page, owed = 0n, taskStatus } = facts;
  const head = `${page ? `Bond No. ${page.number} on task ${b.task}` : `Bond on task ${b.task} (registry id ${b.deed})`}: ${usdg(network, b.amount)}`;
  if (b.status === DeedStatus.Settled) {
    if (b.remainderBps !== Number(BPS)) return `${head}, missed at ${when(b.settledAt)}: ${indexed ? "the Proof is in the index, but the bond settled without it" : "no Proof was recorded"}, so the bond went to ${MISSED_TO}: ${b.refundTo}`;
    const delivered = `${head}, delivered at ${when(b.settledAt)}: the bond less Shipped's 1% fee, ${usdg(network, b.amount - fee(b.amount))},`;
    // The registry keeps one sum per wallet, so only an empty one says which bonds were collected.
    return owed === 0n ? `${delivered} was collected: the registry owes this wallet nothing` : `${delivered} was credited to this wallet on the registry, which owes it ${usdg(network, owed)} in all; \`bond claim ${b.task}\` collects that`;
  }
  if (b.checkMetAt > 0n) {
    const confirmAt = b.checkMetAt + CHECK_HOLD_SEC;
    return `${head}, the Proof is in the index and the check was marked at ${when(b.checkMetAt)}; BrainChain confirms it ${now < confirmAt ? `after ${when(confirmAt)}` : "shortly"}`;
  }
  const settles = `it settles after ${when(b.deadline + CHECK_HOLD_SEC + CHECK_CONFIRM_SEC)} to ${MISSED_TO}: ${b.refundTo}`;
  // Shipped sets no first mark after the deadline, so a Proof that is in the index by now does not release the bond.
  if (now > b.deadline) return `${head}, deadline ${when(b.deadline)} passed ${indexed ? "with the Proof in the index and the check unmarked, and Shipped sets no mark after the deadline" : "with no Proof recorded"}; ${settles}`;
  const open = `${head}, open until ${when(b.deadline)}:`;
  if (indexed) return `${open} the Proof is in the index and BrainChain marks the check shortly`;
  // A refunded task is final and gets no Proof, so its bond can only be missed.
  if (taskStatus === Status.Refunded) return `${open} the task was refunded, so no Proof will be recorded; ${settles}`;
  return `${open} ${taskStatus === Status.Paid ? "the task is paid; waiting for its Proof to be minted and recorded" : "waiting for the task to be paid and its Proof recorded"}`;
}

function closed(network: Network, config: BondConfig | undefined): string | undefined {
  if (!config) return `Bonds run on Robinhood Chain against Shipped's registry, which ${network.name} has no counterpart of. Set BRAINCHAIN_NETWORK=mainnet.`;
  if (!config.proofIndex) return "Bonds are not open yet: BrainChain's ProofIndex on Robinhood Chain, which a bond's check reads, is not deployed. A later release of brainchain-worker names it.";
  return undefined;
}

/** Shipped's own number and page for a deed, which the API may not give for a test bond or when it cannot be reached. */
export const SHIPPED_API = "https://api.shipped.bond";

export interface DeedPage {
  number: string;
  url: string;
}

export async function deedPage(deed: bigint, fetchImpl: typeof fetch = fetch): Promise<DeedPage | undefined> {
  try {
    const response = await fetchImpl(`${SHIPPED_API}/v1/deeds/${deed}`, { signal: AbortSignal.timeout(5_000) });
    if (!response.ok) return undefined;
    const body = (await response.json()) as { deed?: { number?: unknown; url?: unknown } };
    const { number, url } = body.deed ?? {};
    return typeof number === "string" && typeof url === "string" ? { number, url } : undefined;
  } catch {
    return undefined;
  }
}

export interface BondOptions {
  amount: bigint;
  yes: boolean;
  /** Reads Shipped's deed page for the bond's number and link; the global fetch by default. */
  fetch?: typeof fetch;
  /** Asks the person at the terminal; undefined when there is no terminal. */
  ask?: (question: string) => Promise<string>;
  log: (line: string) => void;
}

/** Reads the task, says what the bond costs and what it does, and sends the approval and the bond. */
export async function bond(network: Network, config: BondConfig | undefined, chain: BondChain, task: bigint, options: BondOptions): Promise<void> {
  const { log } = options;
  const shut = closed(network, config);
  if (shut) throw new Error(shut);
  const open = config as BondConfig & { proofIndex: Address };
  const t = await chain.task(task);
  if (!t) throw new Error(`There is no task ${task} on ${network.name}.`);
  if (t.poster.toLowerCase() === chain.account.toLowerCase()) throw new Error(`Task ${task} was posted by this wallet. A bond guarantees delivery to someone else: it earns no standing on a task the worker posted itself.`);
  const hiredHere = t.status === Status.Hired && t.model.toLowerCase().endsWith(chain.account.slice(2).toLowerCase());
  if (!hiredHere) throw new Error(`Task ${task} is not hired to this worker. Bond a task after Jev hires you for it.`);
  const now = await chain.now();
  if (t.deadline <= now) throw new Error(`Task ${task}'s deadline, ${when(t.deadline)}, has passed.`);
  if (options.amount < t.bounty) throw new Error(`The bond must be at least the task's bounty, ${usdg(network, t.bounty)}; ${usdg(network, options.amount)} is under it.`);
  if (options.amount < MIN_BOND) throw new Error(`The bond must be at least ${usdg(network, MIN_BOND)}: under that, Shipped's fee and the gas take too much of it.`);
  // Task ids restart with each board, so a bond on a retired board's task of this number is another task's.
  const existing = (await chain.bondsOn(task)).find((b) => b.status !== DeedStatus.Settled && b.board.toLowerCase() === network.contracts.taskBoard.toLowerCase());
  if (existing) {
    const page = await deedPage(existing.deed, options.fetch);
    throw new Error(`This worker already has ${page ? `bond No. ${page.number}` : "a bond"} open on task ${task} (registry id ${existing.deed}${page ? `, ${page.url}` : ""}). \`bond status ${task}\` shows where it stands.`);
  }
  // A task paid through the desk has the desk as its poster on the board; the bond pays the agent that paid.
  const payer = await chain.payerOf(task);
  if (payer?.toLowerCase() === chain.account.toLowerCase()) throw new Error(`Task ${task} was paid for by this wallet. A bond guarantees delivery to someone else: it earns no standing on a task the worker paid for itself.`);
  const refundTo = payer ?? t.poster;

  const [balance, allowance, gasPrice, eth] = await Promise.all([chain.usdgBalance(), chain.allowance(), chain.gasPrice(), chain.ethBalance()]);
  const approves = allowance < options.amount;
  const gas = bondGas(gasPrice, approves);
  const terms = bondTerms(open, { id: task, refundTo, paidThroughDesk: payer !== undefined, deadline: t.deadline }, { address: network.contracts.taskBoard, chainId: network.chainId });
  const back = options.amount - fee(options.amount);
  log(
    [
      `Bond ${usdg(network, options.amount)} on task ${task} (bounty ${usdg(network, t.bounty)}, deadline ${when(t.deadline)}).`,
      `  Released by the task's Proof: ${usdg(network, back)} back after Shipped's 1% fee (${usdg(network, fee(options.amount))}), collected with \`bond claim ${task}\`.`,
      `  Missed: if no Proof is recorded by ${when(terms.deadline)}, the ${usdg(network, options.amount)} goes to ${refundTo}, ${payer ? "the agent that paid for the task" : "the poster"}.`,
      `  Gas now: about ${formatEther(gas)} ETH on ${network.proofs.name} for ${approves ? "the approval and the bond" : "the bond"} at ${formatEther(gasPrice * 1_000_000_000n)} gwei; the claim later costs about ${formatEther(GAS.withdraw * gasPrice)} ETH.`,
    ].join("\n"),
  );
  if (balance < options.amount) throw new Error(`${chain.account} holds ${usdg(network, balance)} on ${network.proofs.name}, under the ${usdg(network, options.amount)} to bond. Nothing was sent.`);
  if (eth < gas) throw new Error(`${chain.account} holds ${formatEther(eth)} ETH on ${network.proofs.name}, under the ${formatEther(gas)} ETH the transactions need. Nothing was sent.`);
  if (!options.yes) {
    if (!options.ask) throw new Error("There is no terminal to confirm on. Run again with --yes to send without asking.");
    const answer = (await options.ask("Send it? [y/N] ")).trim().toLowerCase();
    if (answer !== "y" && answer !== "yes") return log("Nothing sent.");
  }
  if (approves) {
    log(`Approving ${usdg(network, options.amount)} for Shipped's registry...`);
    await chain.approve(options.amount);
  }
  log(`Bonding ${usdg(network, options.amount)} on task ${task}...`);
  const { deed, tx } = await chain.create(terms, options.amount);
  const page = await deedPage(deed, options.fetch);
  const opened = page ? `Bond No. ${page.number} is open on Shipped: ${page.url} (${tx}).` : `A bond with registry id ${deed} is open on Shipped (${tx}).`;
  log(`${opened} \`bond status ${task}\` follows it. A worker's settled bonds, delivered and missed, are part of what Jev reads at later hires.`);
}

/** Prints where the worker's bonds on a task stand. */
export async function bondStatus(
  network: Network,
  config: BondConfig | undefined,
  chain: BondChain,
  task: bigint,
  log: (line: string) => void,
  fetchImpl: typeof fetch = fetch,
): Promise<void> {
  const shut = closed(network, config);
  if (shut) throw new Error(shut);
  const bonds = await chain.bondsOn(task);
  if (bonds.length === 0) return log(`${chain.account} has no bond on task ${task}.`);
  const delivered = bonds.some((b) => b.status === DeedStatus.Settled && b.remainderBps === Number(BPS));
  const [now, indexed, tasks, owed, pages] = await Promise.all([
    chain.now(),
    Promise.all(bonds.map((b) => chain.proofOf(task, b.board))),
    // Only a bond still waiting for its Proof is worded by where the task stands.
    Promise.all(bonds.map((b) => (b.status !== DeedStatus.Settled && b.checkMetAt === 0n ? chain.task(task, b.board) : undefined))),
    delivered ? chain.owed() : 0n,
    Promise.all(bonds.map((b) => deedPage(b.deed, fetchImpl))),
  ]);
  bonds.forEach((b, i) => {
    const page = pages[i];
    const old = network.retired?.find((r) => r.taskBoard.toLowerCase() === b.board.toLowerCase());
    log(`${bondLine(network, b, { indexed: indexed[i]! > 0n, now, page, owed, taskStatus: tasks[i]?.status })}${old ? ` (task of set ${old.release})` : ""}${page ? ` ${page.url}` : ""}`);
  });
}

/** Collects what a settled bond left the worker: withdraw(USDG) on the registry. */
export async function bondClaim(network: Network, config: BondConfig | undefined, chain: BondChain, task: bigint, log: (line: string) => void, fetchImpl: typeof fetch = fetch): Promise<void> {
  const shut = closed(network, config);
  if (shut) throw new Error(shut);
  const [latest] = await chain.bondsOn(task);
  if (!latest) throw new Error(`${chain.account} has no bond on task ${task}.`);
  const page = await deedPage(latest.deed, fetchImpl);
  if (latest.status !== DeedStatus.Settled) {
    const [now, indexed, t] = await Promise.all([chain.now(), chain.proofOf(task, latest.board), chain.task(task, latest.board)]);
    throw new Error(`${bondLine(network, latest, { indexed: indexed > 0n, now, page, taskStatus: t?.status })}. Nothing can be claimed before it settles.`);
  }
  const owed = await chain.owed();
  if (owed === 0n) {
    const name = bondName(latest, page);
    return log(latest.remainderBps === Number(BPS) ? `${name} was delivered and its ${usdg(network, latest.amount - fee(latest.amount))} was collected: the registry owes this wallet nothing.` : `${name} was missed: its ${usdg(network, latest.amount)} went to ${MISSED_TO}: ${latest.refundTo}. There is nothing to claim.`);
  }
  if ((await chain.ethBalance()) === 0n) throw new Error(`${chain.account} has no ETH on ${network.proofs.name} to pay gas for the claim.`);
  log(`Claiming ${usdg(network, owed)} from Shipped's registry on ${network.proofs.name}...`);
  const { amount, tx } = await chain.withdraw();
  log(`Paid ${usdg(network, amount)} to ${chain.account} (${tx}).`);
}
