// `exit`: the worker's USDG on BrainChain paid back within a minute instead of the bridge's seven days. The desk pays
// it on Robinhood Chain, or, with `--to-solana`, as USDC on Solana through Relay: the transfer to the desk carries the
// Solana address after its arguments, so nothing else is signed and nothing is needed on Robinhood Chain. The token and
// the desk the service names are checked against this release before anything is signed.

import { PublicKey } from "@solana/web3.js";
import bs58 from "bs58";
import { createPublicClient, createWalletClient, encodeFunctionData, erc20Abi, formatUnits, http, isAddress, parseUnits, type Address, type Hex, type PrivateKeyAccount } from "viem";

import { RECEIPT_MS, reason } from "./chain.js";
import { chainOf, type Network } from "./network.js";

export interface ExitTerms {
  desk: Address;
  token: Address;
  payoutChainId: number;
  payoutToken: Address;
  feeBps: number;
  minFeeUnits: string;
  minUnits: string;
  maxUnits: string;
}

export interface ExitRecord {
  /** `held`: nothing more is sent for the exit until a person settles it. */
  state: "waiting" | "paying" | "paid" | "returning" | "returned" | "held";
  net: string;
  fee: string;
  payoutTx?: Hex;
  returnTx?: Hex;
  reason?: string;
  solana?: string;
  relayRequest?: string;
}

/**
 * Keys no one can spend USDC from. Program ids are often on the curve, so the
 * curve alone does not catch them: the all-zero address, which the desk also
 * reads as no destination, the token programs, USDC's mint and Relay's depository.
 */
const NOT_WALLETS = new Set([
  "11111111111111111111111111111111",
  "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
  "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb",
  "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
  "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "99vQwtBwYtrqqD9YSXbdum3KBdxPAVxYTaQ3cfnJSrN2",
]);

/** A Solana address a wallet can spend from: 32 bytes in base58, on the ed25519 curve. A program-derived address is off it, and USDC sent there is stranded. */
export function isSolanaAddress(value: string): boolean {
  if (!/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(value) || NOT_WALLETS.has(value)) return false;
  try {
    const bytes = bs58.decode(value);
    return bytes.length === 32 && PublicKey.isOnCurve(bytes);
  } catch {
    return false;
  }
}

/** A transfer to the desk with the Solana address after its arguments, which the desk reads to pay there. */
export function exitCalldata(desk: Address, amount: bigint, solana?: string): Hex {
  const transfer = encodeFunctionData({ abi: erc20Abi, functionName: "transfer", args: [desk, amount] });
  return solana ? `${transfer}${Buffer.from(bs58.decode(solana)).toString("hex")}` : transfer;
}

export function exitFee(amount: bigint, terms: Pick<ExitTerms, "feeBps" | "minFeeUnits">): bigint {
  const proportional = (amount * BigInt(terms.feeBps)) / 10_000n;
  const floor = BigInt(terms.minFeeUnits);
  const fee = proportional > floor ? proportional : floor;
  return fee > amount ? amount : fee;
}

const units = (value: unknown) => typeof value === "string" && /^\d{1,30}$/.test(value);

/** What the service answers for its exit terms, refused here when it is not the shape the rest of `exit` reads. */
export async function exitTerms(service: string, fetchImpl: typeof fetch = fetch): Promise<ExitTerms> {
  const host = new URL(service).host;
  const response = await fetchImpl(`${service}/exits`, { signal: AbortSignal.timeout(20_000) }).catch(() => {
    throw new Error(`Could not reach the BrainChain service at ${host} for the exit terms. Nothing was sent.`);
  });
  if (response.status === 404) throw new Error("Fast exits are off on this network");
  if (!response.ok) throw new Error(`The BrainChain service at ${host} answered ${response.status} when asked for the exit terms. Nothing was sent.`);
  const terms = (await response.json().catch(() => undefined)) as Partial<ExitTerms> | null | undefined;
  const readable =
    typeof terms?.desk === "string" &&
    isAddress(terms.desk, { strict: false }) &&
    typeof terms.token === "string" &&
    isAddress(terms.token, { strict: false }) &&
    Number.isInteger(terms.feeBps) &&
    terms.feeBps! >= 0 &&
    [terms.minFeeUnits, terms.minUnits, terms.maxUnits].every(units);
  if (!readable) throw new Error(`The BrainChain service at ${host} named the exit terms in a form exit cannot read. Nothing was sent.`);
  return terms as ExitTerms;
}

/** Why the terms cannot be signed for: a transfer goes to whatever token and desk they name, and only this release says which those are. */
export function termsProblem(network: Network, terms: Pick<ExitTerms, "desk" | "token">): string | undefined {
  const host = new URL(network.service).host;
  if (terms.token.toLowerCase() !== network.contracts.bountyToken.toLowerCase()) {
    return `The BrainChain service at ${host} names the token ${terms.token} for an exit, and ${network.name}'s ${network.bountySymbol} is ${network.contracts.bountyToken}. Nothing was sent.`;
  }
  if (terms.desk.toLowerCase() !== network.exitDesk.toLowerCase()) {
    return `The BrainChain service at ${host} names the desk ${terms.desk}, and this release of brainchain-worker pays only ${network.exitDesk}. Nothing was sent.`;
  }
  return undefined;
}

export async function exitRecord(service: string, tx: Hex, fetchImpl: typeof fetch = fetch): Promise<ExitRecord | undefined> {
  const response = await fetchImpl(`${service}/exits/${tx}`, { signal: AbortSignal.timeout(20_000) });
  if (response.status === 404) return undefined;
  if (!response.ok) throw new Error(`${service}/exits answered ${response.status}`);
  return ((await response.json()) as { exits: ExitRecord[] }).exits[0];
}

/** What `exit` needs from the chains, so the flow can be tested without them. */
export interface ExitChain {
  account: Address;
  bountyBalance(token: Address): Promise<bigint>;
  /** How many of the wallet's transactions on BrainChain are sent and not yet mined. */
  unmined(): Promise<number>;
  /** Sends the bounty token to the desk on BrainChain, naming a Solana address when given, and waits for it to be mined. */
  sendToDesk(token: Address, desk: Address, amount: bigint, solana?: string): Promise<Hex>;
}

export function createExitChain(network: Network, account: PrivateKeyAccount, receiptMs = RECEIPT_MS): ExitChain {
  const read = createPublicClient({ chain: chainOf(network), transport: http(network.rpc, { timeout: 20_000 }), pollingInterval: 1_000 });
  const wallet = createWalletClient({ account, chain: chainOf(network), transport: http(network.rpc, { timeout: 20_000 }) });
  return {
    account: account.address,
    bountyBalance: (token) => read.readContract({ address: token, abi: erc20Abi, functionName: "balanceOf", args: [account.address] }),
    async unmined() {
      const [pending, latest] = await Promise.all([read.getTransactionCount({ address: account.address, blockTag: "pending" }), read.getTransactionCount({ address: account.address })]);
      return pending - latest;
    },
    async sendToDesk(token, desk, amount, solana) {
      const hash = await wallet.sendTransaction({ to: token, data: exitCalldata(desk, amount, solana) });
      // Sent is not lost: the transfer can still land, so another run would pay the desk twice.
      const receipt = await read.waitForTransactionReceipt({ hash, timeout: receiptMs }).catch((error: unknown) => {
        throw new Error(`The transfer to the desk was sent (${hash}) and could not be confirmed (${reason(error)}). Follow it at ${network.service}/exits/${hash} before running exit again: another run sends another transfer.`);
      });
      if (receipt.status !== "success") throw new Error(`the transfer to the desk reverted (${hash})`);
      return hash;
    },
  };
}

export async function exit(
  network: Network,
  chain: ExitChain,
  options: {
    amount?: string;
    toSolana?: string;
    dry: boolean;
    log: (line: string) => void;
    fetchImpl?: typeof fetch;
    pollMs?: number;
    waitMs?: number;
    sleep?: (ms: number) => Promise<void>;
  },
): Promise<void> {
  const { log, dry } = options;
  const fetchImpl = options.fetchImpl ?? fetch;
  const sleep = options.sleep ?? ((ms: number) => new Promise((r) => setTimeout(r, ms)));
  if (options.toSolana !== undefined) {
    if (!isSolanaAddress(options.toSolana)) throw new Error(`"${options.toSolana}" is not the address of a Solana wallet, so USDC sent there could not be spent`);
    if (network.id !== "mainnet") throw new Error("--to-solana is mainnet only: Relay connects Solana with Robinhood Chain mainnet, not the testnets");
  }
  const terms = await exitTerms(network.service, fetchImpl);
  const refused = termsProblem(network, terms);
  if (refused) throw new Error(refused);
  const balance = await chain.bountyBalance(terms.token);
  const amount = options.amount === undefined ? balance : parseUnits(options.amount, 6);
  const min = BigInt(terms.minUnits);
  const max = BigInt(terms.maxUnits);
  const symbol = network.bountySymbol;
  const show = (v: bigint) => `${formatUnits(v, 6)} ${symbol}`;
  if (amount === 0n) throw new Error(`The wallet holds no ${symbol} on ${network.name}`);
  if (amount > balance) throw new Error(`The wallet holds ${show(balance)} on ${network.name}, less than ${show(amount)}`);
  if (amount < min) throw new Error(`An exit is at least ${show(min)}`);
  if (amount > max) throw new Error(`An exit is at most ${show(max)}, and nothing was sent. Give --amount up to that, and send the rest in another exit.`);
  const fee = exitFee(amount, terms);
  const net = amount - fee;
  const paid = options.toSolana === undefined
    ? `${show(net)} arrives on the parent chain (chain ${terms.payoutChainId}) after a ${show(fee)} fee.`
    : `${show(net)} after a ${show(fee)} fee is paid as USDC on Solana to ${options.toSolana}, less Relay's own fee. The desk prices that move once the transfer arrives; one that would cost more than 3% (or 0.50 USD) is paid in ${symbol} on the parent chain (chain ${terms.payoutChainId}) instead.`;
  log(`Exit ${show(amount)} from ${network.name}: ${paid}`);
  if (dry) {
    log("Dry run, nothing sent.");
    return;
  }

  const unmined = await chain.unmined();
  if (unmined > 0) throw new Error(`This wallet has a transaction on ${network.name} that is not mined yet, which may be an earlier exit, and another run would send another transfer. Nothing was sent; run exit again once it is mined.`);
  const tx = await chain.sendToDesk(terms.token, terms.desk, amount, options.toSolana);
  const follow = `${network.service}/exits/${tx}`;
  log(`Sent to the desk on ${network.name} (${tx}). Waiting for the payout, usually under a minute.`);
  const end = Date.now() + (options.waitMs ?? 1_800_000);
  let last = "";
  let record: ExitRecord | undefined;
  for (;;) {
    record = await exitRecord(network.service, tx, fetchImpl).catch(() => undefined);
    if (record?.state === "paid" || record?.state === "returned" || record?.state === "held") break;
    if (record?.reason && record.reason !== last) log(`Waiting: ${record.reason}.`);
    last = record?.reason ?? last;
    if (Date.now() > end) {
      const within = options.toSolana === undefined ? "The desk pays it or sends it back within a day" : "Within a day the desk pays it or sends it back, or holds it for a person if Relay has not settled the move";
      log(`Still waiting after ${Math.round((options.waitMs ?? 1_800_000) / 60_000)} minutes. ${within}; follow it at ${follow}.`);
      return;
    }
    await sleep(options.pollMs ?? 10_000);
  }
  if (record.state === "held") {
    log(`The desk holds this exit for a person: ${record.reason ?? "no reason given"}. Nothing more is sent for it until it is settled; follow it at ${follow}.`);
    process.exitCode = 1;
    return;
  }
  if (record.state === "returned") {
    log(`The desk sent it back on ${network.name}: ${record.reason ?? "no reason given"} (${record.returnTx}).`);
    process.exitCode = 1;
    return;
  }
  if (record.solana && record.relayRequest) {
    log(`Paid on Solana: ${show(BigInt(record.net))} as USDC to ${record.solana} (Relay request ${record.relayRequest}).`);
    return;
  }
  log(`Paid on the parent chain: ${show(BigInt(record.net))} (${record.payoutTx})${record.reason ? `. ${record.reason}` : ""}.`);
}
