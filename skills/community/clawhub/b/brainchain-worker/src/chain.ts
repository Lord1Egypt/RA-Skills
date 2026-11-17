import { isIP } from "node:net";

import {
  BaseError,
  ContractFunctionRevertedError,
  createPublicClient,
  createWalletClient,
  encodeAbiParameters,
  encodeFunctionData,
  http,
  HttpRequestError,
  InsufficientFundsError,
  keccak256,
  parseAbi,
  parseEventLogs,
  RpcRequestError,
  slice,
  TimeoutError,
  toBytes,
  WaitForTransactionReceiptTimeoutError,
  type Address,
  type Hex,
  type PrivateKeyAccount,
  type PublicClient,
} from "viem";

import { erc20Errors, taskBoardAbi, transferErrors, workerStakingAbi } from "./abi.js";
import { chainOf, parentChainOf, type Network } from "./network.js";
import { memoryStore, type Store } from "./state.js";

export const erc20Abi = parseAbi([
  "function balanceOf(address) view returns (uint256)",
  "function allowance(address owner, address spender) view returns (uint256)",
  "function approve(address spender, uint256 amount) returns (bool)",
  "function faucet()",
  "function FAUCET_AMOUNT() view returns (uint256)",
  "function FAUCET_INTERVAL() view returns (uint256)",
  "function lastClaim(address) view returns (uint256)",
  "error TooSoon(uint256 nextClaimAt)",
]);

export const bondsAbi = [
  ...parseAbi([
    "event Proposed(uint256 indexed id, address indexed proposer, address indexed target, bytes data, uint128 bond, string uri)",
    "event Settled(uint256 indexed id, uint256 indexed decisionId, bool adopted)",
    "function propose(address target, bytes data, string uri) returns (uint256)",
    "function get(uint256 id) view returns ((address proposer, uint128 bond, uint64 createdAt, uint8 state, bytes32 subject, uint64 deadline, uint16 thresholdBps))",
    "function bond() view returns (uint128)",
    "function openProposal(bytes32 subject) view returns (uint256)",
    "error AlreadyProposed(uint256 id)",
  ]),
  ...erc20Errors,
  ...transferErrors,
] as const;

export const executorAbi = parseAbi([
  "event Queued(uint256 indexed changeId, uint256 indexed decisionId, address indexed target, bytes data, uint64 eta)",
  "function getChange(uint256 changeId) view returns ((address target, bytes data, uint64 eta, bool executed, bool vetoed))",
  "function timelock() view returns (uint64)",
  "function changeSubject(address target, bytes data) view returns (bytes32)",
  "function vetoed(address target, bytes4 selector) view returns (bool)",
  "function vetoedCall(bytes32) view returns (bool)",
]);

/** The appeal terms of a task on set 3.5.0 and later; earlier boards have no appeals and no Ruled or Appealed status. */
export const appealAbi = parseAbi([
  "function appealOf(uint256 id) view returns ((uint64 window, uint16 bondBps, uint64 ruledAt, bool pays, bool confident, address appellant, uint128 bond, uint64 appealedAt))",
]);

/** Mirrors TaskBoard.Status. */
export const Status = { Open: 1, Hired: 2, Submitted: 3, Graded: 4, Disputed: 5, Paid: 6, Refunded: 7, Ruled: 8, Appealed: 9 } as const;
/** Mirrors ProposalBonds.State. */
export const ApplicationState = { Open: 1, Returned: 2, Burned: 3 } as const;
/** Why a task was refunded, by TaskBoard.RefundReason. */
export const REFUND_REASONS = ["no worker was hired", "the result was not delivered in time", "Jev did not grade it in time", "Jev did not accept the work", "Jev ruled for the poster"];

/** How a delivered task settled: paid, with what reached the wallet and when, or refunded, with why and any stake slashed. */
export type Settlement = { paid: true; amount: bigint; at: bigint } | { paid: false; reason: number; slashed: bigint };

/** A task of this worker's that has not settled, with the times that decide what happens next. */
export interface Flight {
  id: bigint;
  status: number;
  accepted: boolean;
  disputedByModel: boolean;
  deadline: bigint;
  gradedAt: bigint;
  disputedAt: bigint;
  disputeWindow: bigint;
  ruleWindow: bigint;
  /** Read for a ruled or appealed task only. */
  appeal?: { window: bigint; ruledAt: bigint; pays: boolean; appealedAt: bigint };
}

const LOG_RANGE = 50_000n;
const MAX_BRIEF_BYTES = 256 * 1024;
/** What the service answers, with its own JSON error, when it will never take this result. */
const REFUSED = [400, 403, 409, 413];
/** How long a transaction's receipt is waited for. */
export const RECEIPT_MS = 90_000;

export interface HiredTask {
  id: bigint;
  deadline: bigint;
  briefURI: string;
  briefHash: Hex;
}

/** A failure that trying again cannot fix. */
export class PermanentError extends Error {}

/** What the work loop needs from the chain and the service. */
export interface WorkerChain {
  now(): Promise<bigint>;
  /** Tasks hired to this worker that wait for its result. */
  hired(): Promise<HiredTask[]>;
  ethBalance(): Promise<bigint>;
  /** Uploads a result to the service, which publishes it once Jev accepts the work, or grades it for a house task. */
  publish(id: bigint, text: string): Promise<{ uri: string; hash: Hex }>;
  /** Sends the submit, hands its hash to `sent` before waiting for the receipt, and returns the hash once it succeeds. */
  submit(id: bigint, resultHash: Hex, resultURI: string, sent: (tx: Hex) => void): Promise<Hex>;
  /** Whether a transaction already sent succeeded, waiting up to `waitMs` for it; undefined when it did not land in that time. */
  landed(tx: Hex, waitMs: number): Promise<boolean | undefined>;
}

/** What the worker signs to upload a result: the chain, the board, the task and the hash of exactly the bytes it uploads. */
export function resultMessage(chainId: number, board: Address, task: bigint, hash: Hex): string {
  return ["BrainChain result v2", `chain ${chainId}`, `board ${board.toLowerCase()}`, `task ${task}`, `hash ${hash}`].join("\n");
}

/** WorkerStaking.idOf: a worker's id is its account, left-padded to 32 bytes. */
export function workerId(account: Address): Hex {
  return `0x${account.slice(2).toLowerCase().padStart(64, "0")}`;
}

export function applicationData(account: Address): Hex {
  return encodeFunctionData({ abi: taskBoardAbi, functionName: "setWorkerAllowed", args: [account, true] });
}

type Reader = Pick<PublicClient, "readContract">;

/** Whether the guardian's veto shuts a call. A set 3.4.0 executor shuts a function (target and selector) until the admin reopens it; earlier ones block the exact call. */
export async function callVetoed(client: Reader, executor: Address, target: Address, data: Hex): Promise<boolean> {
  try {
    return await client.readContract({ address: executor, abi: executorAbi, functionName: "vetoed", args: [target, slice(data, 0, 4)] });
  } catch {
    return client.readContract({
      address: executor,
      abi: executorAbi,
      functionName: "vetoedCall",
      args: [keccak256(encodeAbiParameters([{ type: "address" }, { type: "bytes" }], [target, data]))],
    });
  }
}

/** The open proposal for this exact call, from any wallet, or 0n: the bond contract takes one at a time. */
export async function openProposalOf(client: Reader, network: Network, target: Address, data: Hex): Promise<bigint> {
  const subject = await client.readContract({ address: network.contracts.executor, abi: executorAbi, functionName: "changeSubject", args: [target, data] });
  return client.readContract({ address: network.contracts.bonds, abi: bondsAbi, functionName: "openProposal", args: [subject] });
}

/** The contract error a call reverted with, when the ABI knows it. */
function revertOf(error: unknown) {
  const revert = error instanceof BaseError ? error.walk((e) => e instanceof ContractFunctionRevertedError) : null;
  return revert instanceof ContractFunctionRevertedError ? revert.data : undefined;
}

export function submitFailure(error: unknown): unknown {
  const name = revertOf(error)?.errorName;
  if (name === "TooLate") return new PermanentError("The deadline passed before the result could be submitted");
  if (name === "BadStatus") return new PermanentError("The task no longer waits for a result");
  return error;
}

/** When the faucet opens again for this wallet, if it refused a claim as too soon. */
export function faucetReopens(error: unknown): bigint | undefined {
  const revert = revertOf(error);
  return revert?.errorName === "TooSoon" ? (revert.args?.[0] as bigint) : undefined;
}

const hostOf = (url: string) => (URL.canParse(url) ? new URL(url).host : "the RPC");

/** viem passes on an answer that is not JSON as a quoted JSON string. */
function unquote(text: string): string {
  if (!text.startsWith('"')) return text;
  try {
    const value: unknown = JSON.parse(text);
    return typeof value === "string" ? value : text;
  } catch {
    return text;
  }
}

/** The Basic credentials viem sends for a URL's user and password, which a server that echoes requests answers with. */
function basicAuth(username: string, password: string): string[] {
  if (!username) return [];
  try {
    return [btoa(`${decodeURIComponent(username)}:${decodeURIComponent(password)}`)];
  } catch {
    return [];
  }
}

/** The parts of a URL long enough to be an API key: its credentials, the path, the query and each of their segments. */
function secretParts(url: string): string[] {
  if (!URL.canParse(url)) return [];
  const { pathname, search, username, password } = new URL(url);
  const path = pathname + search;
  return [...basicAuth(username, password), username, password, path, pathname, search, ...path.split(/[/?&=]/)].filter((part) => part.length >= 8);
}

/**
 * One short line of an answer, without the RPC URL's credentials, path or
 * query: an answer can echo them, and they can hold an API key. A web page is
 * far longer than one line.
 */
function excerpt(details: string, url: string): string {
  let line = unquote(details);
  for (const part of secretParts(url)) line = line.replaceAll(part, "…");
  line = line
    .replace(/\b(Basic|Bearer)\s+[\w+/=.~-]+/gi, "$1 …")
    .replace(/\s+/g, " ")
    .replace(/[\x00-\x1f\x7f-\x9f]/g, "")
    .trim();
  return line.length > 160 ? `${line.slice(0, 159)}…` : line;
}

/** A 2xx answer in JSON that is no JSON-RPC reply, such as a REST API's. */
class NotRpcError extends Error {
  /** One short line of the answer, without the URL's secrets. */
  constructor(readonly excerpt: string) {
    super("The answer is not a JSON-RPC reply");
  }
}

const isReply = (value: unknown) =>
  typeof value === "object" && value !== null && ("result" in value || ("error" in value && typeof value.error === "object" && value.error !== null));

/** viem reads an answer without a result as an empty one, and fails later on whatever needed it, such as "Block could not be found." */
async function checkReply(response: Response, url: string): Promise<void> {
  if (!response.ok) return;
  const text = await response.clone().text();
  let value: unknown;
  try {
    value = JSON.parse(text);
  } catch {
    // viem names an answer that is not JSON itself.
    return;
  }
  // The excerpt is cut here, where the URL still holds the credentials viem leaves out of its errors.
  if (!(Array.isArray(value) ? value.every(isReply) : isReply(value))) throw new NotRpcError(excerpt(text, url));
}

/**
 * Whether BRAINCHAIN_RPC_URL holds anything but a host. viem leaves a URL's user
 * and password out of what it reports, so they cannot be masked once an answer
 * echoes them, and an echo can take any form: with such a URL, no answer's text
 * is printed.
 */
function rpcHoldsSecret(): boolean {
  const value = process.env.BRAINCHAIN_RPC_URL?.trim();
  if (!value || !URL.canParse(value)) return false;
  const { username, password, pathname, search } = new URL(value);
  return Boolean(username || password || search || pathname.length > 1);
}

/** A request that failed, named by the RPC's host and the status it answered with. */
function requestFailure(request: HttpRequestError | RpcRequestError | TimeoutError): string {
  const host = hostOf(request.url);
  // viem passes on a 2xx answer that does not parse as JSON as the parser's error.
  if (request.cause instanceof SyntaxError) return `${host} answered, but not as an RPC`;
  if (request.cause instanceof NotRpcError) return `${host} answered, but not as an RPC (${request.cause.excerpt})`;
  const details = request.details ? excerpt(request.details, request.url) : "";
  const status = request instanceof TimeoutError ? undefined : request.status;
  if (status === undefined) return `Could not reach ${host}${details ? ` (${details})` : ""}`;
  // A proxy or CDN in front of the RPC answers an outage or a rate limit with its own page.
  if (details.startsWith("<")) return `${host} answered ${status} with a web page${status === 404 || status === 405 ? ", not as an RPC" : ""}`;
  return `${host} answered ${status}${details && !rpcHoldsSecret() ? ` (${details})` : ""}`;
}

/** A JSON-RPC error, in the RPC's own words: viem's line for an error code is generic and can send the reader after the wrong thing. */
function rpcRefusal(answer: RpcRequestError): string {
  const host = hostOf(answer.url);
  if (rpcHoldsSecret()) return `${host} refused the request (JSON-RPC error ${answer.code})`;
  return `${host} refused the request: ${excerpt(answer.details, answer.url)}`;
}

const SHORT_OF_GAS = "The wallet holds too little ETH to pay for this transaction's gas, so it was not sent. `brainchain-worker status` shows what it holds";


/** Whether a send failed because the wallet cannot cover its gas: the RPC's gas estimate says so as a revert, and the send itself as insufficient funds. */
function outOfGas(error: BaseError): boolean {
  return /gas required exceeds allowance/i.test(error.message) || error.walk((e) => e instanceof InsufficientFundsError) instanceof InsufficientFundsError;
}

/**
 * A send that reverted, checked again as a call without the RPC's cap on gas.
 * The RPC estimates a send with no more gas than the wallet pays for, and a
 * token transfer inside it can run out and revert with FailedInnerCall; a call
 * that passes uncapped failed only for want of gas.
 */
export async function explainRevert(error: unknown, uncapped: () => Promise<unknown>): Promise<unknown> {
  if (!(error instanceof BaseError && error.walk((e) => e instanceof ContractFunctionRevertedError))) return error;
  return (await uncapped().then(() => true, () => false)) ? new Error(SHORT_OF_GAS) : error;
}

/** The contract errors a worker's own sends can meet, in words. */
const PLAIN: Record<string, string> = {
  BadStatus: "the task is not at the step this needs",
  TooLate: "its window has closed",
  TooEarly: "its window has not closed yet",
  NotWorker: "this wallet is not the worker hired for the task",
  NotDisputant: "only the poster or the account that delivered can dispute the grade",
  NotAppellant: "only the side the ruling went against can appeal it",
  IsPaused: "the task board is paused",
  TransferMismatch: "the token moved a different amount than the call asked for",
  FailedInnerCall: "a token transfer inside the call failed without a reason",
  SafeERC20FailedOperation: "a token transfer inside the call failed",
  ERC20InsufficientAllowance: "the wallet has not approved enough of the token for the contract to take",
  ERC20InsufficientBalance: "the wallet holds too little of the token",
  Locked: "the stake is still locked",
  AlreadyProposed: "that exact call already has an open proposal, and the contract takes one at a time",
};

/** One readable line for an error. It names the RPC by host only: its URL can hold an API key. */
export function reason(error: unknown): string {
  if (!(error instanceof BaseError)) return error instanceof Error ? error.message : String(error);
  if (outOfGas(error)) return SHORT_OF_GAS;
  // An RPC error with an HTTP status is a provider refusing the request, such as a bad key or a rate limit.
  const request = error.walk(
    (e) => e instanceof HttpRequestError || e instanceof TimeoutError || (e instanceof RpcRequestError && e.status !== undefined),
  );
  if (request instanceof HttpRequestError || request instanceof RpcRequestError || request instanceof TimeoutError) return requestFailure(request);
  const name = revertOf(error)?.errorName;
  if (name === undefined) {
    const answer = error.walk((e) => e instanceof RpcRequestError);
    const reverted = error.walk((e) => e instanceof ContractFunctionRevertedError) instanceof ContractFunctionRevertedError;
    return answer instanceof RpcRequestError && !reverted ? rpcRefusal(answer) : error.shortMessage;
  }
  const plain = Object.hasOwn(PLAIN, name) ? PLAIN[name] : undefined;
  return plain ? `${error.shortMessage.replace(/\.$/, "")}: ${plain} (${name})` : `${error.shortMessage} (${name})`;
}

/** Why the BrainChain service failed its health check, or undefined when it passed. */
export async function unhealthy(service: string, fetcher: typeof fetch = fetch): Promise<string | undefined> {
  const host = new URL(service).host;
  const response = await fetcher(`${service}/health`, { signal: AbortSignal.timeout(10_000) }).catch(() => undefined);
  if (response === undefined) return `could not reach the BrainChain service at ${host}; results are uploaded there, so none can be delivered until it answers`;
  await response.body?.cancel();
  if (response.ok) return undefined;
  // The service answers 503 while its review rounds are late, which does not stop it taking results.
  if (response.status === 503) return `the BrainChain service at ${host} reports it is behind (503); results still upload, and grading may be late`;
  return `the BrainChain service at ${host} answered its health check with ${response.status}; results are uploaded there, so delivery can fail until it recovers`;
}

/**
 * Refuses a BRAINCHAIN_RPC_URL that serves another chain, which otherwise shows
 * as a read that returns no data or a scan through someone else's blocks. An RPC
 * that does not answer is left to the commands, which say so or outlast it.
 */
export async function requireChainId(network: Network, read: () => Promise<number>): Promise<void> {
  const id = await read().catch(() => undefined);
  if (id !== undefined && id !== network.chainId) throw new Error(`BRAINCHAIN_RPC_URL serves chain ${id}; ${network.name} is chain ${network.chainId}.`);
}

/** BrainChain's RPC, with answers that are not JSON-RPC refused before viem reads them. */
export const brainchainTransport = (network: Network) =>
  http(network.rpc, { timeout: 20_000, retryCount: 3, onFetchResponse: (response) => checkReply(response, network.rpc) });

const identityAbi = parseAbi([
  "function ownerOf(uint256 tokenId) view returns (address)",
  "function getAgentWallet(uint256 agentId) view returns (address)",
]);

export function createChain(network: Network, account: PrivateKeyAccount, store: Store = memoryStore()) {
  const chain = chainOf(network);
  const transport = brainchainTransport(network);
  // BrainChain mines a block per transaction, so receipts are polled every second.
  const client = createPublicClient({ chain, transport, pollingInterval: 1_000 });
  const wallet = createWalletClient({ account, chain, transport });
  const { taskBoard, staking, bonds, executor, stakeToken, bountyToken } = network.contracts;
  const id = workerId(account.address);
  const board = { address: taskBoard, abi: taskBoardAbi } as const;
  const origin = new URL(network.service).origin;

  async function send(request: Parameters<typeof wallet.writeContract>[0], sent?: (hash: Hex) => void): Promise<Hex> {
    const hash = await wallet.writeContract(request).catch(async (error: unknown) => {
      throw await explainRevert(error, () => client.call({ account: account.address, to: request.address, data: encodeFunctionData(request as Parameters<typeof encodeFunctionData>[0]) }));
    });
    sent?.(hash);
    const receipt = await client.waitForTransactionReceipt({ hash, timeout: RECEIPT_MS });
    if (receipt.status !== "success") throw new Error(`Transaction ${hash} reverted`);
    return hash;
  }

  /** Every log of one event from `from` to `to`, in windows the RPC accepts. */
  async function scan<T>(fetch: (fromBlock: bigint, toBlock: bigint) => Promise<T[]>, from: bigint, to: bigint): Promise<T[]> {
    const all: T[] = [];
    for (let start = from; start <= to; start += LOG_RANGE) {
      const end = start + LOG_RANGE - 1n < to ? start + LOG_RANGE - 1n : to;
      all.push(...(await fetch(start, end)));
    }
    return all;
  }

  const hiredLogs = (from: bigint, to: bigint) =>
    scan((fromBlock, toBlock) => client.getContractEvents({ ...board, eventName: "WorkerHired", args: { model: id }, fromBlock, toBlock }), from, to);

  const briefs = new Map<bigint, string>();
  async function briefURI(task: bigint, latest: bigint): Promise<string> {
    const known = briefs.get(task);
    if (known !== undefined) return known;
    const [posted] = await scan(
      (fromBlock, toBlock) => client.getContractEvents({ ...board, eventName: "Posted", args: { id: task }, fromBlock, toBlock }),
      network.fromBlock,
      latest,
    );
    if (posted === undefined) throw new Error(`Task ${task} has no Posted event`);
    briefs.set(task, posted.args.briefURI!);
    return posted.args.briefURI!;
  }

  const work: WorkerChain = {
    async now() {
      const block = await client.getBlock();
      const wall = BigInt(Math.floor(Date.now() / 1000));
      // An idle chain makes no blocks, so the latest block's time can lag the clock.
      return block.timestamp > wall ? block.timestamp : wall;
    },
    async hired() {
      const latest = await client.getBlockNumber();
      const known = store.state.hired;
      const ids = new Set(known?.tasks);
      for (const log of await hiredLogs(known ? BigInt(known.block) + 1n : network.fromBlock, latest)) ids.add(log.args.id!.toString());
      const tasks = await Promise.all(
        [...ids].map(async (key) => {
          const task = BigInt(key);
          const t = await client.readContract({ ...board, functionName: "get", args: [task] });
          if (t.status === Status.Hired && t.model.toLowerCase() === id) {
            return { id: task, deadline: t.deadline, briefURI: await briefURI(task, latest), briefHash: t.briefHash };
          }
          // A task never returns to Hired, the only state that waits on the worker.
          briefs.delete(task);
          return undefined;
        }),
      );
      const hired = tasks.filter((t) => t !== undefined);
      store.state.hired = { block: Number(latest), tasks: hired.map((t) => t.id.toString()) };
      store.save();
      return hired;
    },
    ethBalance: () => client.getBalance({ address: account.address }),
    async publish(task, text) {
      const hash = keccak256(toBytes(text));
      const signature = await account.signMessage({ message: resultMessage(network.chainId, taskBoard, task, hash) });
      const response = await fetch(`${network.service}/results`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ task: task.toString(), text, signature }),
        signal: AbortSignal.timeout(30_000),
      }).catch(() => {
        throw new Error(`Could not reach the BrainChain service at ${new URL(origin).host}`);
      });
      const body = (await response.json().catch(() => undefined)) as { uri?: string; hash?: Hex; error?: unknown } | null | undefined;
      // Only the service's own JSON error is a refusal: a CDN or firewall page with the same status is retried.
      const said = typeof body?.error === "string" ? body.error : undefined;
      const why = `(${response.status}): ${said ?? "no reason given"}`;
      if (REFUSED.includes(response.status) && said !== undefined) throw new PermanentError(`The service refused the result ${why}`);
      if (!response.ok || !body?.uri) throw new Error(`Uploading the result failed ${why}`);
      if (body.hash?.toLowerCase() !== hash) throw new Error("The service stored different bytes than were sent");
      // Not permanent: the address comes from how the service or BRAINCHAIN_SERVICE_URL is set, and the same result uploads again once that is fixed.
      if (!body.uri.startsWith(`${origin}/`)) throw new Error(`The service returned a result address outside ${origin}`);
      return { uri: body.uri, hash };
    },
    submit: (task, resultHash, resultURI, sent) =>
      send({ ...board, functionName: "submit", args: [task, resultHash, resultURI] }, sent).catch((error: unknown) => {
        throw submitFailure(error);
      }),
    async landed(tx, waitMs) {
      // Without replacement checks a receipt is only ever this transaction's, never another sent with its nonce.
      const receipt = await client.waitForTransactionReceipt({ hash: tx, timeout: waitMs, checkReplacement: false }).catch((error: unknown) => {
        if (error instanceof WaitForTransactionReceiptTimeoutError) return undefined;
        throw error;
      });
      return receipt && receipt.status === "success";
    },
  };

  return {
    ...work,
    account: account.address,
    gasPrice: () => client.getGasPrice(),
    /** How many transactions the wallet has sent. */
    sent: () => client.getTransactionCount({ address: account.address }),
    stakeBalance: () => client.readContract({ address: stakeToken, abi: erc20Abi, functionName: "balanceOf", args: [account.address] }),
    bountyBalance: () => client.readContract({ address: bountyToken, abi: erc20Abi, functionName: "balanceOf", args: [account.address] }),
    stake: () => client.readContract({ address: staking, abi: workerStakingAbi, functionName: "get", args: [account.address] }),
    minStake: () => client.readContract({ address: staking, abi: workerStakingAbi, functionName: "minStake" }),
    held: () => client.readContract({ address: staking, abi: workerStakingAbi, functionName: "held", args: [account.address] }),
    allowed: () => client.readContract({ ...board, functionName: "workerAllowed", args: [account.address] }),
    bond: () => client.readContract({ address: bonds, abi: bondsAbi, functionName: "bond" }),
    /** Seconds between Jev allowing a worker and the worker being hireable. */
    timelock: () => client.readContract({ address: executor, abi: executorAbi, functionName: "timelock" }),
    async approve(token: Address, spender: Address, amount: bigint) {
      const current = await client.readContract({ address: token, abi: erc20Abi, functionName: "allowance", args: [account.address, spender] });
      if (current >= amount) return;
      await send({ address: token, abi: erc20Abi, functionName: "approve", args: [spender, amount] });
    },
    claimStakeToken: () => send({ address: stakeToken, abi: erc20Abi, functionName: "faucet" }),
    /** What the stake token's faucet gives, and from when this wallet can claim it. */
    async faucet() {
      const token = { address: stakeToken, abi: erc20Abi } as const;
      const [amount, interval, last] = await Promise.all([
        client.readContract({ ...token, functionName: "FAUCET_AMOUNT" }),
        client.readContract({ ...token, functionName: "FAUCET_INTERVAL" }),
        client.readContract({ ...token, functionName: "lastClaim", args: [account.address] }),
      ]);
      return { amount, opensAt: last === 0n ? 0n : last + interval };
    },
    stakeTokens: (amount: bigint, price: bigint) => send({ address: staking, abi: workerStakingAbi, functionName: "stake", args: [amount, price] }),
    setPrice: (price: bigint) => send({ address: staking, abi: workerStakingAbi, functionName: "setPrice", args: [price] }),
    requestUnstake: (amount: bigint, at: Address = staking) => send({ address: at, abi: workerStakingAbi, functionName: "requestUnstake", args: [amount] }),
    withdraw: (at: Address = staking) => send({ address: at, abi: workerStakingAbi, functionName: "withdraw" }),
    /** Stake left on earlier sets' contracts, which this set's reads do not see. */
    async retiredStakes() {
      const sets = network.retired ?? [];
      const stakes = await Promise.all(sets.map((s) => client.readContract({ address: s.staking, abi: workerStakingAbi, functionName: "get", args: [account.address] })));
      return sets.flatMap((s, i) => (stakes[i]!.staked > 0n || stakes[i]!.unstaking > 0n ? [{ ...s, w: stakes[i]! }] : []));
    },
    /**
     * Whether this wallet owns the ERC-8004 agent `agentId` on the parent chain or is
     * its registered wallet; undefined when the registry could not be read.
     */
    async holdsAgent(agentId: bigint): Promise<boolean | undefined> {
      if (!network.identity || !network.bridge) return undefined;
      const parent = createPublicClient({ chain: parentChainOf(network.bridge), transport: http(network.bridge.rpc, { timeout: 20_000 }) });
      const mine = (holder: Address) => holder.toLowerCase() === account.address.toLowerCase();
      const read = (functionName: "ownerOf" | "getAgentWallet") =>
        parent.readContract({ address: network.identity!, abi: identityAbi, functionName, args: [agentId] });
      try {
        return mine(await read("ownerOf")) || mine(await read("getAgentWallet"));
      } catch (error) {
        return error instanceof BaseError && error.walk((e) => e instanceof ContractFunctionRevertedError) ? false : undefined;
      }
    },
    apply: (profileURI: string) =>
      send({ address: bonds, abi: bondsAbi, functionName: "propose", args: [taskBoard, applicationData(account.address), profileURI] }),
    /** Whether the guardian's veto shuts allowing a worker, which is what an application asks for. */
    applicationVetoed: () => callVetoed(client, executor, taskBoard, applicationData(account.address)),
    /** An open proposal to allow this worker, from any wallet, or 0n. */
    openApplication: () => openProposalOf(client, network, taskBoard, applicationData(account.address)),
    /**
     * This worker's applications, newest last, with their state and the
     * decision that settled each, and the last change any of them queued.
     * Everything is read at one block, so a bond settled just after its change
     * was queued is never seen without the change.
     */
    async applications() {
      const data = applicationData(account.address).toLowerCase();
      const blockNumber = await client.getBlockNumber();
      const proposed = (
        await scan(
          (fromBlock, toBlock) =>
            client.getContractEvents({ address: bonds, abi: bondsAbi, eventName: "Proposed", args: { proposer: account.address, target: taskBoard }, fromBlock, toBlock }),
          network.fromBlock,
          blockNumber,
        )
      ).filter((log) => log.args.data!.toLowerCase() === data);
      // Queued does not index the call, so its scan narrows to the board as target and to blocks from this worker's first application on.
      const since = proposed[0]?.blockNumber ?? blockNumber + 1n;
      const [settled, queued] = await Promise.all([
        scan(
          (fromBlock, toBlock) =>
            client.getContractEvents({ address: bonds, abi: bondsAbi, eventName: "Settled", args: { id: proposed.map((log) => log.args.id!) }, fromBlock, toBlock }),
          since,
          blockNumber,
        ),
        scan(
          (fromBlock, toBlock) => client.getContractEvents({ address: executor, abi: executorAbi, eventName: "Queued", args: { target: taskBoard }, fromBlock, toBlock }),
          since,
          blockNumber,
        ),
      ]);
      const mine = queued.filter((log) => log.args.data!.toLowerCase() === data).at(-1);
      const change = mine && {
        ...(await client.readContract({ address: executor, abi: executorAbi, functionName: "getChange", args: [mine.args.changeId!], blockNumber })),
        decisionId: mine.args.decisionId!,
      };
      const decided = new Map(settled.map((log) => [log.args.id!, log.args.decisionId!]));
      const applications = await Promise.all(
        proposed.map(async (log) => ({
          id: log.args.id!,
          state: (await client.readContract({ address: bonds, abi: bondsAbi, functionName: "get", args: [log.args.id!], blockNumber })).state,
          decisionId: decided.get(log.args.id!),
        })),
      );
      return { applications, change };
    },
    /** How a task settled, read from the events of its settlement, or undefined while it has not. */
    async settlement(task: bigint): Promise<Settlement | undefined> {
      const { status } = await client.readContract({ ...board, functionName: "get", args: [task] });
      if (status !== Status.Paid && status !== Status.Refunded) return undefined;
      const latest = await client.getBlockNumber();
      if (status === Status.Paid) {
        const [log] = await scan(
          (fromBlock, toBlock) => client.getContractEvents({ ...board, eventName: "BountyPaid", args: { id: task }, fromBlock, toBlock }),
          network.fromBlock,
          latest,
        );
        if (log === undefined) throw new Error(`Task ${task} is paid, but no BountyPaid event for it was found`);
        const { timestamp } = await client.getBlock({ blockNumber: log.blockNumber });
        return { paid: true, amount: log.args.bounty! - log.args.fee!, at: timestamp };
      }
      const [log] = await scan(
        (fromBlock, toBlock) => client.getContractEvents({ ...board, eventName: "BountyRefunded", args: { id: task }, fromBlock, toBlock }),
        network.fromBlock,
        latest,
      );
      if (log === undefined) throw new Error(`Task ${task} is refunded, but no BountyRefunded event for it was found`);
      // A worker that loses a dispute it opened is slashed in the transaction that settles the task.
      const { logs } = await client.getTransactionReceipt({ hash: log.transactionHash });
      const slashed = parseEventLogs({ abi: workerStakingAbi, eventName: "Slashed", args: { account: account.address }, logs })
        .filter((slash) => slash.address.toLowerCase() === staking.toLowerCase())
        .reduce((sum, slash) => sum + slash.args.amount, 0n);
      return { paid: false, reason: log.args.reason!, slashed };
    },
    /** Tasks this worker was hired for, by outcome, what it was paid after fees, and each task still in flight. */
    async record() {
      const latest = await client.getBlockNumber();
      const ids = [...new Set((await hiredLogs(network.fromBlock, latest)).map((log) => log.args.id!))];
      const tasks = await Promise.all(ids.map(async (task) => ({ id: task, ...(await client.readContract({ ...board, functionName: "get", args: [task] })) })));
      const paid = await scan(
        (fromBlock, toBlock) => client.getContractEvents({ ...board, eventName: "BountyPaid", args: { account: account.address }, fromBlock, toBlock }),
        network.fromBlock,
        latest,
      );
      const open: number[] = [Status.Hired, Status.Submitted, Status.Graded, Status.Disputed, Status.Ruled, Status.Appealed];
      const inFlight: Flight[] = await Promise.all(
        tasks
          .filter((t) => open.includes(t.status))
          .map(async ({ id: task, status, accepted, disputedByModel, deadline, gradedAt, disputedAt, disputeWindow, ruleWindow }) => {
            const flight: Flight = { id: task, status, accepted, disputedByModel, deadline, gradedAt, disputedAt, disputeWindow, ruleWindow };
            if (status !== Status.Ruled && status !== Status.Appealed) return flight;
            return { ...flight, appeal: await client.readContract({ address: taskBoard, abi: appealAbi, functionName: "appealOf", args: [task] }) };
          }),
      );
      return {
        paid: tasks.filter((t) => t.status === Status.Paid).length,
        refunded: tasks.filter((t) => t.status === Status.Refunded && t.model.toLowerCase() === id).length,
        inFlight: inFlight.sort((a, b) => (a.id < b.id ? -1 : 1)),
        earned: paid.reduce((sum, log) => sum + log.args.bounty! - log.args.fee!, 0n),
      };
    },
  };
}

export type Chain = ReturnType<typeof createChain>;

/** Briefs come from strangers, so the worker fetches only public names, never an address or a local network's name. */
function publicHost(hostname: string): boolean {
  const host = hostname.toLowerCase().replace(/\.$/, "");
  if (host.startsWith("[") || isIP(host) !== 0) return false;
  return host.includes(".") && !/(^|\.)localhost$|\.local$|\.internal$/.test(host);
}

async function download(uri: string, fetcher: typeof fetch): Promise<Uint8Array> {
  if (!URL.canParse(uri)) throw new PermanentError("The brief's URL is not valid");
  const url = new URL(uri);
  if (!publicHost(url.hostname)) throw new PermanentError(`The brief is on ${url.hostname}, which is not a public host`);
  const stop = new AbortController();
  const response = await fetcher(url, { redirect: "error", signal: AbortSignal.any([stop.signal, AbortSignal.timeout(15_000)]) });
  if (!response.ok) throw new Error(`The brief answered ${response.status}`);
  const chunks: Uint8Array[] = [];
  let size = 0;
  for await (const chunk of response.body ?? []) {
    size += chunk.byteLength;
    if (size > MAX_BRIEF_BYTES) {
      stop.abort();
      throw new PermanentError(`The brief is larger than ${MAX_BRIEF_BYTES / 1024} KB`);
    }
    chunks.push(chunk);
  }
  return Uint8Array.from(Buffer.concat(chunks));
}

/** Reads a brief and checks it against the hash on chain. Briefs are base64 data URIs or https URLs. */
export async function fetchBrief(uri: string, expected: Hex, fetcher: typeof fetch = fetch): Promise<string> {
  let bytes: Uint8Array;
  if (uri.startsWith("data:")) {
    const comma = uri.indexOf(",");
    if (comma < 0 || !uri.slice(0, comma).endsWith(";base64")) throw new PermanentError("The brief's data URI is not base64");
    bytes = Uint8Array.from(Buffer.from(uri.slice(comma + 1), "base64"));
  } else if (uri.startsWith("https://")) {
    bytes = await download(uri, fetcher);
  } else {
    throw new PermanentError("The brief is neither a data URI nor an https URL");
  }
  if (bytes.byteLength > MAX_BRIEF_BYTES) throw new PermanentError(`The brief is larger than ${MAX_BRIEF_BYTES / 1024} KB`);
  if (keccak256(bytes).toLowerCase() !== expected.toLowerCase()) throw new PermanentError("The brief does not match its hash on chain");
  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch {
    throw new PermanentError("The brief is not UTF-8 text");
  }
}
