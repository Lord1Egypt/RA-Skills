"use strict";

const { loadWallet } = require("./wallet");

const BASE_RPC = "https://mainnet.base.org";
const USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
const ERC20_BALANCE_ABI = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
];

async function getBalances(address) {
  const { createPublicClient, http, formatUnits } = require("viem");
  const { base } = require("viem/chains");

  const client = createPublicClient({ chain: base, transport: http(BASE_RPC) });
  const [usdcRaw, ethRaw] = await Promise.all([
    client.readContract({
      address: USDC_ADDRESS,
      abi: ERC20_BALANCE_ABI,
      functionName: "balanceOf",
      args: [address],
    }),
    client.getBalance({ address }),
  ]);

  return {
    address,
    network: "base-mainnet",
    usdc: formatUnits(usdcRaw, 6),
    eth: formatUnits(ethRaw, 18),
  };
}

async function balance() {
  const wallet = loadWallet();
  const balances = await getBalances(wallet.address);
  console.log(
    JSON.stringify(
      {
        ...balances,
        note: "Fund with USDC on Base. ETH is not required for x402 exact-scheme payments.",
      },
      null,
      2,
    ),
  );
}

module.exports = { balance, getBalances };
