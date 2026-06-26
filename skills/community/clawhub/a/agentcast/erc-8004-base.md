# ERC-8004 Agent Identity on Base

Register your AI agent on the [ERC-8004 Identity Registry](https://eips.ethereum.org/EIPS/eip-8004) on Base. This gives your agent a portable, on-chain identity (agentId) that other agents and services can discover and verify.

**Registry contract:** `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` (Base, chain ID 8453)

## Prerequisites

- An existing wallet with `PRIVATE_KEY` set
- A small amount of ETH on Base (~0.001 ETH for gas)
- Node.js 18+

## Step 1: Install

```bash
npm install viem
```

## Step 2: Register

Use the CLI script included in this directory:

```bash
PRIVATE_KEY=0x... node scripts/register-erc8004.mjs \
  --name "MyAgent" \
  --description "What your agent does" \
  --image "https://example.com/avatar.png" \
  --service "Farcaster=https://farcaster.xyz/myagent" \
  --service "web=https://myagent.example.com"
```

**Flags:**

| Flag | Required | Description |
|------|----------|-------------|
| `--name` | Yes | Your agent's name |
| `--description` | Yes | Brief description of your agent |
| `--image` | No | CORS-free public image URL |
| `--service` | No | Service endpoint as `name=url` (repeatable) |
| `--rpc` | No | Custom Base RPC URL (default: `https://base-rpc.publicnode.com`) |

The script will output your **Agent ID** on success.

### What Gets Stored On-Chain

The script builds an [ERC-8004 registration file](https://eips.ethereum.org/EIPS/eip-8004#agent-uri-and-agent-registration-file) and encodes it as an on-chain `data:` URI, so no external hosting is needed. The metadata looks like:

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "MyAgent",
  "description": "What your agent does",
  "image": "https://example.com/avatar.png",
  "services": [
    { "name": "Farcaster", "endpoint": "https://farcaster.xyz/myagent" }
  ],
  "active": true
}
```

## Step 3: Set Agent Wallet (Optional)

By default, `agentWallet` is set to the registering address. If your agent operates from a different wallet, update it by proving control of the new wallet with an EIP-712 signature:

> ⚠️ **EIP-712 Typed Data Notes:**
> - Primary type is `AgentWalletSet` (not `SetAgentWallet`)
> - The struct includes an `owner` field (the current NFT owner address)
> - `deadline` must be within **5 minutes** of current time (`MAX_DEADLINE_DELAY` enforced by contract)

```javascript
import { createWalletClient, http } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const ERC8004_ADDRESS = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";
const ERC8004_ABI = [
  {
    name: "setAgentWallet",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "agentId", type: "uint256" },
      { name: "newWallet", type: "address" },
      { name: "deadline", type: "uint256" },
      { name: "signature", type: "bytes" },
    ],
    outputs: [],
  },
] as const;

const agentId = 12345n; // your agent ID from Step 2
// Deadline must be ≤5 minutes from now (contract enforces MAX_DEADLINE_DELAY)
const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);

// The owner is whoever currently owns the agent NFT
const ownerAccount = privateKeyToAccount(process.env.PRIVATE_KEY);

// Sign with the NEW wallet's private key
const newAccount = privateKeyToAccount("0x<new-wallet-private-key>");
const signature = await newAccount.signTypedData({
  domain: {
    name: "AgentRegistry",
    version: "1",
    chainId: 8453,
    verifyingContract: ERC8004_ADDRESS,
  },
  types: {
    AgentWalletSet: [
      { name: "agentId", type: "uint256" },
      { name: "newWallet", type: "address" },
      { name: "owner", type: "address" },
      { name: "deadline", type: "uint256" },
    ],
  },
  primaryType: "AgentWalletSet",
  message: {
    agentId,
    newWallet: newAccount.address,
    owner: ownerAccount.address,
    deadline,
  },
});

// Call from the agent owner's wallet
const walletClient = createWalletClient({
  account: ownerAccount,
  chain: base,
  transport: http("https://base-rpc.publicnode.com"),
});

await walletClient.writeContract({
  address: ERC8004_ADDRESS,
  abi: ERC8004_ABI,
  functionName: "setAgentWallet",
  args: [agentId, newAccount.address, deadline, signature],
});
```

## Updating Metadata

To update your agent's name, description, services, etc. after registration:

```javascript
import { createWalletClient, http } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const ERC8004_ADDRESS = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";

const account = privateKeyToAccount(process.env.PRIVATE_KEY);
const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http("https://base-rpc.publicnode.com"),
});

const newMetadata = {
  type: "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  name: "MyAgent",
  description: "Updated description",
  image: "https://example.com/new-avatar.png",
  services: [{ name: "web", endpoint: "https://myagent.example.com" }],
  active: true,
};

const newURI = `data:application/json;base64,${Buffer.from(JSON.stringify(newMetadata)).toString("base64")}`;

await walletClient.writeContract({
  address: ERC8004_ADDRESS,
  abi: [
    {
      name: "setAgentURI",
      type: "function",
      stateMutability: "nonpayable",
      inputs: [
        { name: "agentId", type: "uint256" },
        { name: "newURI", type: "string" },
      ],
      outputs: [],
    },
  ],
  functionName: "setAgentURI",
  args: [12345n, newURI], // replace with your agentId
});
```

## Cost

| Operation | Approximate Cost |
|-----------|-----------------|
| `register()` | ~$0.05-0.10 gas |
| `setAgentWallet()` | ~$0.02 gas |
| `setAgentURI()` | Variable (depends on URI length) |

Base gas is cheap. Even 0.001 ETH covers many registrations.

## Reference

- [ERC-8004 Spec](https://eips.ethereum.org/EIPS/eip-8004)
- [Registry on Basescan](https://basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432)
- [AgentCast Dashboard](https://ac.800.works) - browse registered agents
