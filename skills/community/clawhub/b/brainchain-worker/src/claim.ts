import { createPublicClient, createWalletClient, formatEther, http, parseAbi, parseEventLogs, type Address, type Hex, type PrivateKeyAccount } from "viem";

import { RECEIPT_MS } from "./chain.js";
import { proofsChainOf, proofsTransport, type Network } from "./network.js";

export const proofsIncomeAbi = parseAbi([
  "function due(uint256 tokenId) view returns (uint256)",
  "function claimMany(uint256[] tokenIds)",
  "function claim(uint256 tokenId)",
  "function proofs() view returns (address)",
  "event Claimed(uint256 indexed tokenId, address indexed to, uint256 amount)",
]);

/** The most Proofs one claim pays for, which keeps the transaction far inside a block. */
export const MAX_CLAIM = 200;

/** What claim needs from the chain the Proofs live on. */
export interface IncomeChain {
  account: Address;
  due(ids: bigint[]): Promise<bigint[]>;
  ethBalance(): Promise<bigint>;
  /** Sends one claimMany, waits for its receipt and returns its hash and the ETH it paid to `account`. */
  claimMany(ids: bigint[]): Promise<{ tx: Hex; paid: bigint }>;
}

export function createIncome(proofs: Network["proofs"], income: Address, account: PrivateKeyAccount): IncomeChain {
  const chain = proofsChainOf(proofs);
  const transport = proofsTransport(proofs);
  const client = createPublicClient({ chain, transport, pollingInterval: 1_000 });
  const wallet = createWalletClient({ account, chain, transport });
  const router = { address: income, abi: proofsIncomeAbi } as const;
  return {
    account: account.address,
    due: (ids) => client.multicall({ contracts: ids.map((id) => ({ ...router, functionName: "due", args: [id] }) as const), allowFailure: false }),
    ethBalance: () => client.getBalance({ address: account.address }),
    async claimMany(ids) {
      const tx = await wallet.writeContract({ ...router, functionName: "claimMany", args: [ids] });
      const receipt = await client.waitForTransactionReceipt({ hash: tx, timeout: RECEIPT_MS });
      if (receipt.status !== "success") throw new Error(`The claim ${tx} reverted`);
      // A claim pays whoever holds the Proof when it lands, so a piece sold since the service listed it pays its buyer.
      const paid = parseEventLogs({ abi: proofsIncomeAbi, eventName: "Claimed", args: { to: account.address }, logs: receipt.logs })
        .filter((log) => log.address.toLowerCase() === income.toLowerCase())
        .reduce((sum, log) => sum + log.args.amount, 0n);
      return { tx, paid };
    },
  };
}

/** The Proofs the service says `owner` holds, by token id. */
export async function ownedProofs(network: Network, owner: Address, fetcher: typeof fetch = fetch): Promise<bigint[]> {
  const host = new URL(network.service).host;
  const response = await fetcher(`${network.service}/proofs/${network.chainId}/owned/${owner}`, { signal: AbortSignal.timeout(15_000) }).catch(() => {
    throw new Error(`Could not reach the BrainChain service at ${host}`);
  });
  if (!response.ok) {
    await response.body?.cancel();
    if (response.status === 404) throw new Error(`The BrainChain service at ${host} does not list Proofs by holder yet. Try claim again later.`);
    throw new Error(`The BrainChain service at ${host} answered ${response.status} when asked for the worker's Proofs`);
  }
  const tokens = ((await response.json().catch(() => undefined)) as { tokens?: unknown } | null | undefined)?.tokens;
  if (!Array.isArray(tokens) || !tokens.every((id) => typeof id === "string" && /^\d{1,78}$/.test(id))) {
    throw new Error(`The BrainChain service at ${host} listed the worker's Proofs in a form claim cannot read`);
  }
  return [...new Set(tokens.map((id: string) => BigInt(id)))].sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
}

const proofCount = (n: number) => `${n} Proof${n === 1 ? "" : "s"}`;

function table(ids: bigint[], dues: bigint[]): string {
  const width = Math.max("Proof".length, ...ids.map((id) => id.toString().length));
  const row = (left: string, right: string) => `  ${left.padEnd(width)}  ${right}`;
  const total = dues.reduce((sum, due) => sum + due, 0n);
  return [row("Proof", "Due (ETH)"), ...ids.map((id, i) => row(id.toString(), formatEther(dues[i]!))), row("Total", formatEther(total))].join("\n");
}

/**
 * Pays the income due on the worker's Proofs with one claimMany from its key.
 * `connect` is only called where Proofs earn income, so testnet needs no key.
 */
export async function claim(
  network: Network,
  connect: (income: Address) => IncomeChain,
  options: { dry: boolean; log: (line: string) => void; fetcher?: typeof fetch },
): Promise<void> {
  const { log } = options;
  const { income, name } = network.proofs;
  if (income === undefined) {
    return log(`Proofs on ${name} earn no income, so there is nothing to claim. Mainnet Proofs are claimed with BRAINCHAIN_NETWORK=mainnet.`);
  }
  const chain = connect(income);
  const ids = await ownedProofs(network, chain.account, options.fetcher);
  if (ids.length === 0) return log(`The BrainChain service lists no Proofs held by ${chain.account} on ${name}, so there is nothing to claim.`);
  const dues = await chain.due(ids);
  log(table(ids, dues));
  const owed = ids.map((id, i) => ({ id, due: dues[i]! })).filter((proof) => proof.due > 0n);
  if (owed.length === 0) return log(`Nothing is due on the worker's ${proofCount(ids.length)} yet.`);

  // A paid Proof is due nothing until the next distribution, so the next run claims what this one leaves.
  const batch = owed.slice(0, MAX_CLAIM);
  const amount = batch.reduce((sum, proof) => sum + proof.due, 0n);
  const left = owed.length - batch.length;
  const rest = left > 0 ? ` ${left} more Proof${left === 1 ? " has" : "s have"} income due: run claim again.` : "";
  if (options.dry) return log(`Dry run, nothing sent: claim would pay ${formatEther(amount)} ETH for ${proofCount(batch.length)}.${rest}`);
  if ((await chain.ethBalance()) === 0n) {
    throw new Error(`${chain.account} has no ETH on ${name} to pay gas for the claim. Send it a little ETH on ${name} and run claim again.`);
  }
  log(`Claiming ${formatEther(amount)} ETH for ${proofCount(batch.length)} on ${name}...`);
  const { tx, paid } = await chain.claimMany(batch.map((proof) => proof.id));
  log(`Paid ${formatEther(paid)} ETH to ${chain.account} (${tx}).${rest}`);
}
