import { createPublicClient, createWalletClient, encodeFunctionData, formatUnits, parseAbi, type Address, type Hex, type PrivateKeyAccount } from "viem";

import { erc20Errors, transferErrors } from "./abi.js";
import { appealAbi, brainchainTransport, erc20Abi, explainRevert, faucetReopens, reason, RECEIPT_MS, Status } from "./chain.js";
import { chainOf, type Network } from "./network.js";
import { ethNeeded, GAS, shortOfGas } from "./standing.js";

/** TaskBoard statuses from set 3.5.0 on: a ruling that waits out its appeal window, and one under appeal. */
export const { Ruled, Appealed } = Status;

const boardAbi = [
  ...parseAbi([
    "function get(uint256 id) view returns ((address poster, uint128 bounty, uint64 deadline, uint8 status, bool accepted, bool disputed, bool disputedByModel, bytes32 model, bytes32 briefHash, bytes32 resultHash, uint64 submittedAt, uint64 gradedAt, uint64 disputedAt, uint64 postedAt, address payee, address feeRecipient, uint16 feeBps, uint16 hireThresholdBps, uint16 gradeThresholdBps, uint16 ruleThresholdBps, uint64 gradeWindow, uint64 disputeWindow, uint64 ruleWindow))",
    "function appealBond(uint256 id) view returns (uint128)",
    "function dispute(uint256 id)",
    "function appeal(uint256 id)",
    "error BadStatus()",
    "error TooLate()",
    "error NotDisputant()",
    "error NotAppellant()",
    "error TransferMismatch()",
  ]),
  ...appealAbi,
  ...erc20Errors,
  ...transferErrors,
] as const;

/** The highest gas limit seen for the bond's approval. */
const APPROVE_GAS = 50_000n;
/**
 * The appeal was estimated at 112,355 gas, yet the RPC refused it to a wallet
 * that held 2.8 times that at the going price, so it is counted high.
 */
const APPEAL_GAS = 140_000n;

export interface DisputeTask {
  status: number;
  poster: Address;
  payee: Address;
  accepted: boolean;
  disputed: boolean;
  gradedAt: bigint;
  disputeWindow: bigint;
  ruleWindow: bigint;
}

export interface DisputeChain {
  account: Address;
  now(): Promise<bigint>;
  task(id: bigint): Promise<DisputeTask>;
  /** Set 3.5.0 and later only; earlier boards have no appeals. */
  appealOf(id: bigint): Promise<{ window: bigint; ruledAt: bigint; pays: boolean }>;
  appealBond(id: bigint): Promise<bigint>;
  bountyBalance(): Promise<bigint>;
  /** What the bounty token's faucet gives, and from when this wallet can claim it; testnet only. */
  bountyFaucet(): Promise<{ amount: bigint; opensAt: bigint }>;
  claimBounty(): Promise<Hex>;
  ethBalance(): Promise<bigint>;
  /** How many transactions the wallet has sent. */
  sent(): Promise<number>;
  gasPrice(): Promise<bigint>;
  /** What the board may already take of the wallet's bounty token. */
  allowance(): Promise<bigint>;
  /** Approves the board to take `amount`, unless it already may, and returns the approval's hash when one was sent. */
  approveBounty(amount: bigint): Promise<Hex | undefined>;
  dispute(id: bigint): Promise<Hex>;
  appeal(id: bigint): Promise<Hex>;
}

export function createDisputeChain(network: Network, account: PrivateKeyAccount): DisputeChain {
  const chain = chainOf(network);
  const transport = brainchainTransport(network);
  const client = createPublicClient({ chain, transport, pollingInterval: 1_000 });
  const wallet = createWalletClient({ account, chain, transport });
  const board = { address: network.contracts.taskBoard, abi: boardAbi } as const;
  const token = { address: network.contracts.bountyToken, abi: erc20Abi } as const;

  async function send(functionName: "dispute" | "appeal", id: bigint): Promise<Hex> {
    const hash = await wallet.writeContract({ ...board, functionName, args: [id] }).catch(async (error: unknown) => {
      throw await explainRevert(error, () => client.call({ account: account.address, to: board.address, data: encodeFunctionData({ abi: boardAbi, functionName, args: [id] }) }));
    });
    const receipt = await client.waitForTransactionReceipt({ hash, timeout: RECEIPT_MS });
    if (receipt.status !== "success") throw new Error(`Transaction ${hash} reverted`);
    return hash;
  }

  return {
    account: account.address,
    async now() {
      const block = await client.getBlock();
      const wall = BigInt(Math.floor(Date.now() / 1000));
      return block.timestamp > wall ? block.timestamp : wall;
    },
    task: (id) => client.readContract({ ...board, functionName: "get", args: [id] }),
    appealOf: (id) => client.readContract({ ...board, functionName: "appealOf", args: [id] }),
    appealBond: (id) => client.readContract({ ...board, functionName: "appealBond", args: [id] }),
    bountyBalance: () => client.readContract({ ...token, functionName: "balanceOf", args: [account.address] }),
    async bountyFaucet() {
      const [amount, interval, last] = await Promise.all([
        client.readContract({ ...token, functionName: "FAUCET_AMOUNT" }),
        client.readContract({ ...token, functionName: "FAUCET_INTERVAL" }),
        client.readContract({ ...token, functionName: "lastClaim", args: [account.address] }),
      ]);
      return { amount, opensAt: last === 0n ? 0n : last + interval };
    },
    async claimBounty() {
      const hash = await wallet.writeContract({ ...token, functionName: "faucet" });
      const receipt = await client.waitForTransactionReceipt({ hash, timeout: RECEIPT_MS });
      if (receipt.status !== "success") throw new Error(`The faucet claim ${hash} reverted`);
      return hash;
    },
    ethBalance: () => client.getBalance({ address: account.address }),
    sent: () => client.getTransactionCount({ address: account.address }),
    gasPrice: () => client.getGasPrice(),
    allowance: () => client.readContract({ ...token, functionName: "allowance", args: [account.address, board.address] }),
    async approveBounty(amount) {
      const current = await client.readContract({ ...token, functionName: "allowance", args: [account.address, board.address] });
      if (current >= amount) return undefined;
      const hash = await wallet.writeContract({ ...token, functionName: "approve", args: [board.address, amount] });
      const receipt = await client.waitForTransactionReceipt({ hash, timeout: RECEIPT_MS });
      if (receipt.status !== "success") throw new Error(`Approval ${hash} reverted`);
      return hash;
    },
    dispute: (id) => send("dispute", id),
    appeal: (id) => send("appeal", id),
  };
}

const same = (a: string, b: string) => a.toLowerCase() === b.toLowerCase();
const at = (seconds: bigint) => new Date(Number(seconds) * 1000).toISOString().replace(/\.000Z$/, "Z");

/** Disputes a grade on a task the worker delivered, within the dispute window. */
export async function dispute(network: Network, chain: DisputeChain, id: bigint, log: (line: string) => void): Promise<void> {
  const [task, now] = await Promise.all([chain.task(id), chain.now()]);
  if (task.status === 0) throw new Error(`There is no task ${id} on ${network.name}.`);
  if (!same(task.payee, chain.account) && !same(task.poster, chain.account)) {
    throw new Error(`Only the poster or the account that delivered task ${id} can dispute it, and ${chain.account} is neither.`);
  }
  if (task.status !== Status.Graded || task.disputed) throw new Error(`Task ${id} is not waiting on a dispute: a grade can be disputed once, while it is graded and unsettled.`);
  const closes = task.gradedAt + task.disputeWindow;
  if (now > closes) throw new Error(`The dispute window for task ${id} closed at ${at(closes)}.`);
  const tx = await chain.dispute(id);
  log(`Disputed the grade on task ${id} (${task.accepted ? "it accepted the work" : "it rejected the work"}): ${tx}`);
  log(`Jev rules within ${task.ruleWindow / 3_600n} hours. A confident ruling decides; otherwise the grade stands.`);
}

/** Appeals the ruling on a task, as the side it went against, with the bond the board fixed when the task was posted. */
export async function appeal(network: Network, chain: DisputeChain, id: bigint, log: (line: string) => void): Promise<void> {
  const [task, now] = await Promise.all([chain.task(id), chain.now()]);
  if (task.status === 0) throw new Error(`There is no task ${id} on ${network.name}.`);
  if (task.status === Status.Disputed) throw new Error(`Task ${id} is still waiting for Jev's ruling. Appeal once it is ruled.`);
  if (task.status === Appealed) throw new Error(`Task ${id} is already under appeal; a ruling can be appealed once.`);
  if (task.status !== Ruled) throw new Error(`Task ${id} has no ruling open to appeal.`);
  const terms = await chain.appealOf(id);
  const appellant = terms.pays ? task.poster : task.payee;
  if (!same(appellant, chain.account)) {
    throw new Error(`The ruling on task ${id} ${terms.pays ? "pays the model, so only the poster" : "refunds the poster, so only the account that delivered"} can appeal it.`);
  }
  const closes = terms.ruledAt + terms.window;
  if (now > closes) throw new Error(`The appeal window for task ${id} closed at ${at(closes)}.`);
  const [bond, balance, eth, gasPrice, allowance, sent] = await Promise.all([
    chain.appealBond(id),
    chain.bountyBalance(),
    chain.ethBalance(),
    chain.gasPrice(),
    chain.allowance(),
    chain.sent(),
  ]);
  const amount = `${formatUnits(bond, 6)} ${network.bountySymbol}`;
  const holds = `The appeal bond is ${amount}, and this wallet holds ${formatUnits(balance, 6)}.`;
  // Test USDG comes from its faucet, as tBRAIN does for join; only mainnet's USDG is bridged in.
  const claims = balance < bond && network.bountyFaucet === true;
  if (balance < bond && !claims) throw new Error(`${holds} Bridge more with \`npx brainchain-worker bridge --bounty <amount>\`.`);
  const closed = (opensAt: bigint) =>
    new Error(
      `${holds} The ${network.bountySymbol} faucet allows one claim a day, and this wallet can claim again at ${at(opensAt)}` +
        (opensAt > closes ? `, after the appeal window closes at ${at(closes)}.` : `. Run appeal again then, before the appeal window closes at ${at(closes)}.`),
    );
  if (claims) {
    const faucet = await chain.bountyFaucet();
    if (now < faucet.opensAt) throw closed(faucet.opensAt);
    if (balance + faucet.amount < bond) throw new Error(`${holds} The faucet's ${formatUnits(faucet.amount, 6)} ${network.bountySymbol} a day would not make up the rest.`);
  }
  // Checked for every transaction before any is sent: an approval alone spends gas and leaves the bond approved.
  const need = ethNeeded([...(claims ? [GAS.faucet] : []), ...(allowance < bond ? [APPROVE_GAS] : []), APPEAL_GAS], gasPrice);
  if (eth < need) throw new Error(`${chain.account} holds ${shortOfGas(network, chain.account, eth, sent, need, "the appeal")} Nothing was sent.`);
  if (claims) {
    log(`Claiming ${network.bountySymbol} from the testnet faucet for the bond...`);
    const claim = await chain.claimBounty().catch((error: unknown) => {
      const opensAt = faucetReopens(error);
      throw opensAt === undefined ? error : closed(opensAt);
    });
    log(`Claimed: ${claim}`);
  }
  const approval = await chain.approveBounty(bond);
  const tx = await chain.appeal(id).catch((error: unknown) => {
    if (approval === undefined) throw error;
    throw new Error(
      `The board was approved to take the ${amount} bond (${approval}), and then the appeal failed: ${reason(error)}. ` +
        `The approval stands, so running appeal again before ${at(closes)} sends only the appeal.`,
    );
  });
  log(`Appealed the ruling on task ${id} with a ${amount} bond: ${tx}`);
  log(`Jev rules again within ${task.ruleWindow / 3_600n} hours. The bond comes back unless Jev confidently rules the same way.`);
}
