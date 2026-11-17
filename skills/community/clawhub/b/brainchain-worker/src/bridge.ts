import {
  createPublicClient,
  createWalletClient,
  encodeAbiParameters,
  formatEther,
  formatUnits,
  http,
  parseAbi,
  parseUnits,
  type Address,
  type Hex,
  type PrivateKeyAccount,
} from "viem";

import { reason, RECEIPT_MS } from "./chain.js";
import { chainOf, parentChainOf, type Network } from "./network.js";
import { grouped } from "./standing.js";

export type Asset = "eth" | "stake" | "bounty";

const inboxAbi = parseAbi([
  "function depositEth() payable returns (uint256)",
  "function calculateRetryableSubmissionFee(uint256 dataLength, uint256 baseFee) view returns (uint256)",
]);
const routerAbi = parseAbi([
  "function getGateway(address token) view returns (address)",
  "function outboundTransferCustomRefund(address token, address refundTo, address to, uint256 amount, uint256 maxGas, uint256 gasPriceBid, bytes data) payable returns (bytes)",
]);
const gatewayAbi = parseAbi(["function getOutboundCalldata(address token, address from, address to, uint256 amount, bytes data) view returns (bytes)"]);
const erc20Abi = parseAbi([
  "function balanceOf(address) view returns (uint256)",
  "function allowance(address owner, address spender) view returns (uint256)",
  "function approve(address spender, uint256 amount) returns (bool)",
]);

/** Gas for the token's arrival on BrainChain; what it does not use comes back to the worker there. */
const DEPOSIT_GAS = 300_000n;

/** What a deposit needs from the parent chain. */
export interface BridgeChain {
  account: Address;
  /** The worker's ETH on the parent chain, which pays the deposit and its gas. */
  parentEth(): Promise<bigint>;
  tokenBalance(asset: Exclude<Asset, "eth">): Promise<bigint>;
  /** The ETH a token deposit sends along to pay for its arrival. */
  arrivalCost(asset: Exclude<Asset, "eth">, amount: bigint): Promise<bigint>;
  depositEth(amount: bigint): Promise<Hex>;
  /** Approves the token's gateway when needed and sends the deposit. */
  depositToken(asset: Exclude<Asset, "eth">, amount: bigint, value: bigint): Promise<Hex>;
}

export function createBridgeChain(network: Network, account: PrivateKeyAccount): BridgeChain {
  const bridge = network.bridge;
  if (!bridge) throw new Error(`${network.name} has no bridge from a parent chain`);
  const parent = parentChainOf(bridge);
  const read = createPublicClient({ chain: parent, transport: http(bridge.rpc, { timeout: 20_000 }) });
  const wallet = createWalletClient({ account, chain: parent, transport: http(bridge.rpc, { timeout: 20_000 }) });
  const child = createPublicClient({ chain: chainOf(network), transport: http(network.rpc, { timeout: 20_000 }) });
  const token = (asset: Exclude<Asset, "eth">): Address => {
    const address = bridge.tokens?.[asset];
    if (!address) throw new Error(`${network.name}'s ${asset} token is not bridged from ${bridge.name}`);
    return address;
  };
  const wait = async (hash: Hex) => {
    const receipt = await read.waitForTransactionReceipt({ hash, timeout: RECEIPT_MS });
    if (receipt.status !== "success") throw new Error(`transaction ${hash} reverted on ${bridge.name}`);
    return hash;
  };
  const gateway = (address: Address) => read.readContract({ address: bridge.router, abi: routerAbi, functionName: "getGateway", args: [address] });

  return {
    account: account.address,
    parentEth: () => read.getBalance({ address: account.address }),
    tokenBalance: (asset) => read.readContract({ address: token(asset), abi: erc20Abi, functionName: "balanceOf", args: [account.address] }),
    async arrivalCost(asset, amount) {
      const address = token(asset);
      const calldata = await read.readContract({
        address: await gateway(address),
        abi: gatewayAbi,
        functionName: "getOutboundCalldata",
        args: [address, account.address, account.address, amount, "0x"],
      });
      const block = await read.getBlock();
      const baseFee = block.baseFeePerGas ?? (await read.getGasPrice());
      const submission = await read.readContract({
        address: bridge.inbox,
        abi: inboxAbi,
        functionName: "calculateRetryableSubmissionFee",
        args: [BigInt((calldata.length - 2) / 2), baseFee],
      });
      // Three times the quoted submission fee rides out a base fee that moves before the deposit lands; the rest is refunded on BrainChain.
      return submission * 3n + DEPOSIT_GAS * ((await child.getGasPrice()) * 2n);
    },
    depositEth: async (amount) => wait(await wallet.writeContract({ address: bridge.inbox, abi: inboxAbi, functionName: "depositEth", value: amount })),
    async depositToken(asset, amount, value) {
      const address = token(asset);
      const spender = await gateway(address);
      // Ahead of the approval, so a refusal has sent nothing at all.
      const gasPriceBid = (await child.getGasPrice()) * 2n;
      const maxSubmissionCost = value - DEPOSIT_GAS * gasPriceBid;
      if (maxSubmissionCost <= 0n) throw new Error(`The gas price on ${network.name} moved after this deposit was priced, so the ETH set aside no longer pays for its arrival. Nothing was sent. Run the command again.`);
      const allowance = await read.readContract({ address, abi: erc20Abi, functionName: "allowance", args: [account.address, spender] });
      if (allowance < amount) await wait(await wallet.writeContract({ address, abi: erc20Abi, functionName: "approve", args: [spender, amount] }));
      const data = encodeAbiParameters([{ type: "uint256" }, { type: "bytes" }], [maxSubmissionCost, "0x"]);
      return wait(
        await wallet.writeContract({
          address: bridge.router,
          abi: routerAbi,
          functionName: "outboundTransferCustomRefund",
          args: [address, account.address, account.address, amount, DEPOSIT_GAS, gasPriceBid, data],
          value,
        }),
      );
    },
  };
}

/** The amount flag's decimals and the name the worker sees. */
export function assetOf(network: Network, asset: Asset): { decimals: number; symbol: string } {
  if (asset === "eth") return { decimals: 18, symbol: "ETH" };
  return asset === "stake" ? { decimals: 18, symbol: network.stakeSymbol } : { decimals: 6, symbol: network.bountySymbol };
}

/**
 * Moves ETH, the stake token or the bounty token from the parent chain to the
 * worker's own address on BrainChain, where it arrives in about a minute.
 */
export async function bridge(
  network: Network,
  chain: BridgeChain,
  options: { asset: Asset; amount: string; dry: boolean; log: (line: string) => void },
): Promise<void> {
  const { asset, dry, log } = options;
  const parent = network.bridge;
  if (!parent) throw new Error(`${network.name} has no bridge from a parent chain`);
  const { decimals, symbol } = assetOf(network, asset);
  const amount = parseUnits(options.amount, decimals);
  if (amount <= 0n) throw new Error("the amount must be above zero");
  // Token amounts are grouped as status shows them; ETH amounts are small.
  const shown = asset === "eth" ? `${formatUnits(amount, decimals)} ${symbol}` : `${grouped(amount, decimals)} ${symbol}`;

  let eth: bigint;
  try {
    eth = await chain.parentEth();
  } catch (error) {
    throw new Error(`could not read the wallet on ${parent.name}: ${reason(error)}`);
  }
  if (asset === "eth") {
    const gas = parseUnits("0.00002", 18);
    if (eth < amount + gas) throw new Error(`${chain.account} holds ${formatEther(eth)} ETH on ${parent.name}; ${shown} plus gas is needed. ${parent.gas}`);
    log(`bridging ${shown} from ${parent.name} to ${chain.account} on ${network.name}`);
    if (dry) return log("dry run: nothing sent");
    const tx = await chain.depositEth(amount);
    return log(`sent, arrives on ${network.name} in about a minute: ${tx}`);
  }

  const held = await chain.tokenBalance(asset);
  if (held < amount) {
    throw new Error(`${chain.account} holds ${grouped(held, decimals)} ${symbol} on ${parent.name}, ${grouped(amount - held, decimals)} short of ${shown}`);
  }
  const value = await chain.arrivalCost(asset, amount);
  if (eth < value + parseUnits("0.0001", 18)) {
    throw new Error(`${chain.account} holds ${formatEther(eth)} ETH on ${parent.name}; about ${formatEther(value + parseUnits("0.0001", 18))} ETH is needed to pay the deposit's arrival and gas. ${parent.gas}`);
  }
  log(`bridging ${shown} from ${parent.name} to ${chain.account} on ${network.name} (sending ${formatEther(value)} ETH for its arrival, the unused part refunded there)`);
  if (dry) return log("dry run: nothing sent");
  const tx = await chain.depositToken(asset, amount, value);
  log(`sent, arrives on ${network.name} in about a minute: ${tx}`);
}
