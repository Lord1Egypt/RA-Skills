"use strict";

const { loadWallet } = require("./wallet");
const { askYesNo, isInteractive } = require("./prompt");

const BASE_RPC = "https://mainnet.base.org";
const USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
const ERC20_ABI = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "transfer",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
];

function parseFlags(args) {
  const flags = { to: null, amount: null, yes: false };
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--to") flags.to = args[++i];
    else if (arg === "--amount") flags.amount = args[++i];
    else if (arg === "--yes" || arg === "-y") flags.yes = true;
  }
  return flags;
}

function usage() {
  console.log(`Usage:
  x402-agent-voice withdraw --to 0xYourWallet --amount all
  x402-agent-voice withdraw --to 0xYourWallet --amount 1.25

Sends USDC from the local agent hot wallet on Base to another wallet.
The agent wallet needs a small Base ETH balance for gas.`);
}

function parseUsdcAmount(amount, balanceRaw) {
  const { parseUnits } = require("viem");
  if (!amount) throw new Error("Missing --amount. Use --amount all or --amount 1.25");
  if (amount.toLowerCase() === "all") return balanceRaw;
  if (!/^\d+(\.\d{1,6})?$/.test(amount)) {
    throw new Error("Invalid --amount. Use a USDC amount with up to 6 decimals, or use all.");
  }
  return parseUnits(amount, 6);
}

async function withdraw(args) {
  const flags = parseFlags(args);
  if (!flags.to || !flags.amount) {
    usage();
    process.exit(1);
  }

  const { createPublicClient, createWalletClient, formatUnits, http, isAddress } = require("viem");
  const { privateKeyToAccount } = require("viem/accounts");
  const { base } = require("viem/chains");

  if (!isAddress(flags.to)) throw new Error(`Invalid destination address: ${flags.to}`);

  const wallet = loadWallet();
  if (flags.to.toLowerCase() === wallet.address.toLowerCase()) {
    throw new Error("Destination is the agent wallet itself. Choose a different wallet.");
  }

  const account = privateKeyToAccount(wallet.privateKey);
  const publicClient = createPublicClient({ chain: base, transport: http(process.env.BASE_RPC_URL || BASE_RPC) });
  const walletClient = createWalletClient({ account, chain: base, transport: http(process.env.BASE_RPC_URL || BASE_RPC) });

  const [balanceRaw, ethRaw] = await Promise.all([
    publicClient.readContract({
      address: USDC_ADDRESS,
      abi: ERC20_ABI,
      functionName: "balanceOf",
      args: [account.address],
    }),
    publicClient.getBalance({ address: account.address }),
  ]);

  const amountRaw = parseUsdcAmount(flags.amount, balanceRaw);
  if (amountRaw <= 0n) throw new Error("Nothing to withdraw. USDC balance is zero.");
  if (amountRaw > balanceRaw) {
    throw new Error(`Insufficient USDC. Balance is ${formatUnits(balanceRaw, 6)} USDC.`);
  }

  if (ethRaw <= 0n) {
    throw new Error("The agent wallet has no Base ETH for gas. Add a tiny amount of Base ETH, then retry.");
  }

  const gas = await publicClient.estimateContractGas({
    account,
    address: USDC_ADDRESS,
    abi: ERC20_ABI,
    functionName: "transfer",
    args: [flags.to, amountRaw],
  });

  const summary = {
    from: account.address,
    to: flags.to,
    network: "base-mainnet",
    token: "USDC",
    amount: formatUnits(amountRaw, 6),
    fullBalance: flags.amount.toLowerCase() === "all",
    estimatedGasUnits: gas.toString(),
    note: "This sends USDC from the local agent hot wallet. The private key is not printed.",
  };

  console.log(JSON.stringify(summary, null, 2));

  if (!flags.yes) {
    if (!isInteractive()) {
      throw new Error("Refusing to withdraw without confirmation in a noninteractive shell. Re-run with --yes.");
    }
    const ok = await askYesNo("\nSend this withdrawal now?", false);
    if (!ok) {
      console.log("Withdrawal cancelled.");
      return;
    }
  }

  const hash = await walletClient.writeContract({
    address: USDC_ADDRESS,
    abi: ERC20_ABI,
    functionName: "transfer",
    args: [flags.to, amountRaw],
  });

  console.log(JSON.stringify({
    ok: true,
    tx: hash,
    explorer: `https://basescan.org/tx/${hash}`,
  }, null, 2));
}

module.exports = { withdraw };
