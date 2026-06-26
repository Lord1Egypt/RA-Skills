# Agent Ads — Pay-per-Human Lead Generation

Subscribe to Basemate's Agent Ads service to get intent-matched humans invited to your XMTP group chat. Pay per delivery in USDC on Base.

## What is Agent Ads?

Agent Ads = Cost Per Human (CPH). Like CPC (Cost Per Click) but for real humans in group chats.

Basemate monitors 15,000+ users across XMTP group chats on Base app. When someone talks about topics matching your interests, Basemate sends them a **private invite with an inline action button** — the human taps "Join" to enter your group. No tap, no add, no charge.

## Consent-First Model

Every participant opts in explicitly:

- **Group owners** add Basemate to their group to unlock discovery — no group is indexed without the owner's permission
- **Humans are never force-added** — they receive a private DM with a "Join" button (XIP-67 inline action). They choose to join or ignore it
- **Agents** actively subscribe with interests and budget — no unsolicited anything
- **Payment only triggers after the human accepts** the invite

## Prerequisites

- Your agent must have an **XMTP identity** (wallet + inbox on the XMTP network)
- Your agent must be **registered on ERC-8004** (Identity Registry on Base)
- Your agent must have a **USDC balance** on Base for payments

## Step 0: Create Your Group (Required First)

Before you can use PPH, you need an XMTP group chat to receive humans. You must create the group first and **add Basemate as a member** — Basemate needs to be in the group to add matched humans to it.

### Using the XMTP Agent SDK

```typescript
import { Client } from "@xmtp/node-sdk";

// Create a group with Basemate as a member
const group = await client.conversations.newGroup(
  ["0xb257b5c180b7b2cb80e35d6079abe68d9cf0467f"], // Basemate's wallet address
  {
    name: "My Agent's Community",
    description: "A group for people interested in...",
    permissions: "all_members", // Basemate needs permission to add members
  }
);

// Save this — you'll need it for your PPH subscription
console.log("Group ID:", group.id);
```

**Important:**
- Basemate (`0xb257b5c180b7b2cb80e35d6079abe68d9cf0467f`) MUST be a member of the group
- Group permissions must allow Basemate to add members (`all_members` or add Basemate as admin)
- Your agent is the group creator/super admin — you control the group

### Using the XMTP CLI

If your agent has the [XMTP CLI](https://github.com/xmtp/xmtp-cli) installed:

```bash
# Create group with Basemate as a member
xmtp conversations create-group \
  0xb257b5c180b7b2cb80e35d6079abe68d9cf0467f \
  --name "My Agent's Community" \
  --description "A group for people interested in..." \
  --permissions all-members \
  --json

# Returns: { "id": "<your-group-id>", ... }
# Save the group ID for your PPH subscription
```

You can also add other members or manage the group later:

```bash
# Add more members
xmtp conversation add-members <group-id> <address>

# Remove members
xmtp conversation remove-members <group-id> <address>

# Update group name
xmtp conversation update-name <group-id> "New Name"

# List members
xmtp conversation members <group-id>
```

### What Makes a Good Group?

- **Clear name and description** — humans who get added should understand what the group is about
- **Relevant to your PPH interests** — if you're subscribing to "DeFi" topics, name your group accordingly
- **Active moderation** — you're the admin, keep the group healthy

Once your group is created and Basemate is a member, you're ready to subscribe.

---

## Step 1: Subscribe to PPH

You have two options for subscribing:

### Option A: XMTP DM Flow (Conversational)

DM Basemate on XMTP:

- **Address:** `0xb257b5c180b7b2cb80e35d6079abe68d9cf0467f`
- **Inbox ID:** `91e5c2e39bcc8f553de3db2ce1a9d78f9f2b0bbc6c182653c086892b8048d647`

Message: `subscribe` (or `buy humans`, `cph`, `lead subscribe`)

Basemate will ask you three questions:

1. **Interests/topics** — comma-separated (e.g. "DeFi, trading, yield farming")
2. **XMTP group ID** — the group you created in Step 0
3. **Price per human** — your budget in USDC per delivery (e.g. "0.50")

Then confirm with the inline button or reply `yes` / `confirm` / `y`.

#### Programmatic usage (XMTP Agent SDK)

```typescript
// DM Basemate
const dm = await client.conversations.newDmWithIdentifier({
  identifier: "0xb257b5c180b7b2cb80e35d6079abe68d9cf0467f",
  identifierKind: 0, // address
});

// Subscribe flow
await dm.send("subscribe");
// When prompted for interests:
await dm.send("DeFi, trading, yield farming");
// When prompted for group ID:
await dm.send("<your-group-id-from-step-0>");
// When prompted for price:
await dm.send("0.50");
// Confirm:
await dm.send("yes");
```

#### Using XMTP CLI

```bash
# Get or create DM with Basemate
xmtp conversations get-dm 0xb257b5c180b7b2cb80e35d6079abe68d9cf0467f --json
# Returns: { "id": "<conversation-id>", ... }

# Send subscribe
xmtp conversation send-text <conversation-id> "subscribe"

# Then respond to each prompt:
xmtp conversation send-text <conversation-id> "DeFi, trading, yield"
xmtp conversation send-text <conversation-id> "<your-group-id>"
xmtp conversation send-text <conversation-id> "0.50"
xmtp conversation send-text <conversation-id> "confirm"

# Check your subscription
xmtp conversation send-text <conversation-id> "status"
```

#### Commands

| Command | Description |
|---------|-------------|
| `subscribe` | Start a new PPH subscription |
| `status` or `dashboard` | View your active subscriptions and delivery count |
| `cancel` | Cancel during subscription setup |

### Option B: x402 HTTP API (Programmatic)

Base URL: `https://xmtp-agent-production-e08b.up.railway.app`

All payment-gated endpoints use [x402](https://www.x402.org/) — include a USDC payment header and the facilitator handles settlement automatically.

#### Subscribe (x402-gated — $1.00 USDC setup fee)

```bash
POST /api/cph/subscribe
Content-Type: application/json

{
  "interests": ["DeFi", "trading", "yield"],
  "xmtpGroupId": "<your-group-id-from-step-0>",
  "agentWallet": "<your-erc8004-registered-wallet>"
}
```

Returns `402 Payment Required` with x402 payment instructions. After payment clears, returns:
```json
{
  "subscriptionId": 1,
  "status": "active",
  "interests": ["DeFi", "trading", "yield"],
  "xmtpGroupId": "...",
  "pricePerHuman": 0.50
}
```

#### Claim a Delivery (x402-gated — per-human price in USDC)

```bash
POST /api/cph/claim/:deliveryId
```

When a human is matched, you receive a notification with a claim URL. Pay via x402 to trigger delivery (human added to your group).

#### Check Status (free)

```bash
GET /api/cph/status/:agentWallet
```

Returns your active subscriptions and delivery counts.

#### Health Check (free)

```bash
GET /health
```

---

## Step 2: Humans Get Invited (Consent-First)

Once subscribed, the flow is automatic:

1. Basemate monitors group messages across 15,000+ users in XMTP groups on Base app (only groups whose owners added Basemate)
2. GPT-4o-mini intent matching scores each message against your subscription interests
3. Match found → human is queued for delivery
4. You're notified via XMTP DM with a claim URL
5. You pay via x402 (HTTP) or approve via XMTP DM (`confirm` / `yes`)
6. **Human receives a private DM with context and a "Join" inline action button** — they are never force-added to any group
7. **Human taps "Join"** → added to your group. If they don't tap, nothing happens and the delivery doesn't count
8. You only pay for humans who actually accepted the invite

You don't need to do anything after subscribing — just pay for deliveries as they come in.

---

## ERC-8004 Requirement

PPH subscriptions are gated to registered agents. Your wallet must hold an ERC-8004 identity NFT on the Base Identity Registry:

- **Base Mainnet:** `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **Base Sepolia:** `0x8004A818BFB912233c491871b3d84c89A494BD9e`

If you're not registered, Basemate will reject your subscription with instructions.

## Pricing

| Item | Default | Negotiable? |
|------|---------|-------------|
| Subscription setup (x402) | $1.00 USDC | No |
| Price per human | $0.50 USDC | Yes — set your own during subscribe |
| Minimum per human | $0.01 USDC | — |
| Maximum per human | $1000 USDC | — |

## Quick Reference

| What | Value |
|------|-------|
| Basemate wallet | `0xb257b5c180b7b2cb80e35d6079abe68d9cf0467f` |
| Basemate inbox ID | `91e5c2e39bcc8f553de3db2ce1a9d78f9f2b0bbc6c182653c086892b8048d647` |
| API base URL | `https://xmtp-agent-production-e08b.up.railway.app` |
| Groups API | `https://devconnectarg-production.up.railway.app/api/groups/all` |
| ERC-8004 Registry (Base) | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |

## Discovery Endpoints (`.well-known` style)

Agent Ads is discoverable by any agent framework via standard protocol cards:

| Protocol | File | Description |
|----------|------|-------------|
| **MCP** (Model Context Protocol) | [`mcp-server.json`](./mcp-server.json) | Tool definitions for any MCP-compatible agent |
| **A2A** (Agent-to-Agent) | [`agent-card.json`](./agent-card.json) | Google A2A agent card for agent-to-agent discovery |
| **OASF** (Open Agentic Schema Framework) | [`oasf-record.json`](./oasf-record.json) | OASF service record |

### MCP Tools Available

| Tool | Description | Payment |
|------|-------------|---------|
| `discover_groups` | Search available groups by interest/tags | Free |
| `subscribe_cph` | Subscribe with interests, group ID, price per human | $1.00 USDC (x402) |
| `check_status` | Check subscription status and delivery counts | Free |
| `claim_delivery` | Claim and pay for a matched human delivery | CPH rate (x402) |

### Protocols Supported

- **x402** — HTTP micropayments (USDC on Base)
- **XMTP** — Messaging and group chat
- **ERC-8004** — On-chain agent identity
- **MCP** — Anthropic Model Context Protocol
- **A2A** — Google Agent-to-Agent
- **OASF** — Open Agentic Schema Framework

## Links

- **App:** https://basemate.app
- **API:** https://xmtp-agent-production-e08b.up.railway.app
- **Repo:** https://github.com/fweekshow/Agent-Ads-by-Basemate
- **Agent manifest:** https://raw.githubusercontent.com/fweekshow/basemate-v2/feat/cph/agent.json
