# ENS Manager

> Complete ENS workflow - register names, create subdomains, publish IPFS content in minutes

## The Problem

Managing ENS names requires multiple tools: app.ens.domains for registration, manual contract calls for subdomains, IPFS pinning services for content, and separate gateways for publishing. Each step takes time and technical knowledge.

## This Skill

Automates the complete ENS workflow from registration to published website - one command per operation, proper three-phase registration, automatic wrapped/unwrapped handling.

---

## 📋 Requirements

- Node.js 18+
- viem ^1.20.0
- content-hash ^2.5.2
- Ethereum wallet keystore
- ETH for gas + registration fees

---

## ⚡ What It Does

### Register New .eth Names
- **Check availability and price** before committing funds
- **Three-phase registration** (commitment → 60s wait → register)
- **Anti-frontrunning protection** via commitment scheme
- **Automatic balance checking** prevents failed transactions

### Manage Subdomains
- **Create subdomains** under any owned ENS name
- **Handles wrapped and unwrapped** names automatically
- **Set IPFS content** in one combined operation
- **Immediate gateway access** via eth.limo/eth.link

### Publish Websites
- **Deploy static sites** to decentralized ENS domains
- **Update content** with new IPFS CIDs
- **Check status** of any ENS name (ownership, content, resolver)

---



---

## 📦 Dependencies

**Install before using:**

```bash
cd scripts/
npm install viem          # Core (required for all scripts)
npm install content-hash  # Extended (only for IPFS features)
```

**Or install everything:**
```bash
cd scripts/ && npm install
```

### What You Need

| Dependency | Used By | Purpose |
|------------|---------|---------|
| `viem` | **ALL scripts** | Ethereum blockchain interactions |
| `content-hash` | IPFS scripts only | Encode/decode IPFS CIDs |

**See [DEPENDENCIES.md](DEPENDENCIES.md) for detailed installation guide.**

**See [QUICK-START.md](QUICK-START.md) for copy-paste operational commands.**


## 🚀 Installation

```bash
# Clone or copy to your skills directory
cp -r ens-manager ~/.openclaw/skills/

# Install dependencies
cd ~/.openclaw/skills/ens-manager/scripts
npm install
```

---

## 🔧 Quick Start

### Register a New ENS Name

**Time: 2-3 minutes**

```bash
# 1. Check availability and price (5 seconds)
node scripts/register-ens-name.js mynewname --dry-run

# 2. Register for 1 year (2-3 minutes: commitment + 60s wait + register)
node scripts/register-ens-name.js mynewname --years 1 \
  --keystore /path/to/keystore.enc \
  --password "your-password"
```

**What happens:**
1. Phase 1: Commitment TX (~30 seconds)
2. Phase 2: Mandatory 60-second wait (anti-frontrunning)
3. Phase 3: Registration TX with payment (~30 seconds)

**Cost:** $5-20/year (name) + $4-7 gas

---

### Create Subdomain with Website

**Time: 1-2 minutes**

```bash
# Upload your site to IPFS first
ipfs add -r ./website
# Returns: QmABC123...

# Create subdomain and set content (1 TX, ~1 minute)
node scripts/create-subdomain-ipfs.js yourname.eth blog QmABC123... \
  --keystore /path/to/keystore.enc \
  --password "your-password"

# Access immediately at: https://blog.yourname.eth.limo
```

**Cost:** $0.03-0.05 gas

---

### Check ENS Status

**Time: 5 seconds**

```bash
node scripts/check-ens-name.js yourname.eth
```

**Shows:**
- Owner address
- Wrapped/unwrapped status
- Resolver address
- IPFS content hash (if set)
- Gateway URLs

---

## 📖 Common Workflows

### 1. Register Your First ENS Name

**Total time: 3-5 minutes**

```bash
# Step 1: Check availability (5s)
node scripts/register-ens-name.js mycoolname --dry-run

# Output shows:
# ✅ Name available
# 💰 Cost: 0.008 ETH (~$20)

# Step 2: Register (2-3 min)
node scripts/register-ens-name.js mycoolname --years 1 \
  --keystore ~/.openclaw/workspace/wallet-keystore.enc \
  --password "keystore-password"

# Progress shown:
# 📝 Phase 1: Making commitment... ✅
# ⏳ Phase 2: Waiting 60 seconds... (countdown)
# 📝 Phase 3: Registering... ✅
# 🎉 Registration complete!
```

---

### 2. Publish a Static Website

**Total time: 2-3 minutes**

```bash
# Step 1: Add to IPFS (30s - 1min, depends on size)
ipfs add -r ./my-website
# Returns: QmXYZ789...

# Step 2: Create subdomain + set content (1 TX, ~1 min)
node scripts/create-subdomain-ipfs.js myname.eth site QmXYZ789... \
  --keystore ~/.openclaw/workspace/wallet-keystore.enc \
  --password "keystore-password"

# Step 3: Access (immediate)
# https://site.myname.eth.limo
```

**Cost:** ~$0.05 gas

---

### 3. Update Website Content

**Time: 1-2 minutes**

```bash
# Upload new version to IPFS (30s - 1min)
ipfs add -r ./my-website-v2
# Returns: QmNEW456...

# Update content hash (1 TX, ~30s)
node scripts/create-subdomain-ipfs.js myname.eth site QmNEW456... \
  --keystore ~/.openclaw/workspace/wallet-keystore.enc \
  --password "keystore-password"

# Gateway updates in 1-2 minutes
```

---

## ⚙️ Configuration

### Contract Addresses (Mainnet)

All operations use these official ENS contracts:

```javascript
ENS_REGISTRY = '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e'
ETH_REGISTRAR_CONTROLLER = '0x253553366Da8546fC250F225fe3d25d0C782303b'
NAME_WRAPPER = '0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401'
PUBLIC_RESOLVER = '0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63'
```

### RPC Endpoint

Default: `https://mainnet.rpc.buidlguidl.com` (reliable, free)

Override with:
```bash
RPC_URL=https://your-provider.com node scripts/register-ens-name.js ...
```

### Keystore

Expected format (AES-256-CBC encrypted):
```json
{
  "salt": "hex-string",
  "iv": "hex-string",
  "data": "hex-string"
}
```

---

## 🐛 Troubleshooting

### Registration: "Name not available"

Name is already registered. Check ownership:
```bash
node scripts/check-ens-name.js <name>.eth
```

Shows current owner and expiration date.

---

### Registration: "Insufficient funds"

You need:
- Registration price: $5-20 (varies by name length)
- Gas for 2 TXs: $4-7

Check balance:
```bash
cast balance <your-address> --rpc-url https://mainnet.rpc.buidlguidl.com
```

---

### Registration: "Commitment too old"

If you wait >24 hours between Phase 1 and Phase 3, the commitment expires. Start over:
```bash
node scripts/register-ens-name.js <name> --years 1 ...
```

---

### Subdomain: "Not the owner"

You must own the parent name to create subdomains. Verify ownership:
```bash
node scripts/check-ens-name.js parentname.eth
```

---

### Content not appearing on eth.limo

**Wait 1-2 minutes** for DNS propagation, then:

1. Check content hash is set:
   ```bash
   node scripts/check-ens-name.js subdomain.yourname.eth
   ```

2. Verify IPFS CID is accessible:
   ```bash
   curl -I https://ipfs.io/ipfs/YOUR_CID
   ```

3. Try alternate gateway:
   ```bash
   https://subdomain.yourname.eth.link
   ```

---

## 📊 Timing & Costs

### Registration (new .eth name)

| Phase | Time | Gas @ 0.22 gwei | Gas @ 10 gwei | Notes |
|-------|------|-----------------|---------------|-------|
| Availability check | 5s | Free | Free | Read-only |
| Phase 1: Commit | 30s | ~$0.02 | ~$1.13 | Anti-frontrunning |
| Phase 2: Wait | 60s | Free | Free | Mandatory |
| Phase 3: Register | 30s | ~$0.15 | ~$6.63 | Includes payment |
| **Total** | **2-3 min** | **~$0.17 + name** | **~$7.75 + name** | See [COSTS.md](COSTS.md) |

**ENS Name Pricing:**
- 3 chars: ~$773/year
- 4 chars: ~$193/year
- 5+ chars: ~$6/year

**Example (5-letter name):**
- Current conditions: ~$6.17 total
- Typical conditions: ~$13.75 total

### Subdomain Creation

| Operation | Time | Gas @ 0.22 gwei | Gas @ 10 gwei |
|-----------|------|-----------------|---------------|
| Create subdomain | 30s | ~$0.08 | ~$3.75 |
| Set IPFS content | Combined | Included | Included |
| Gateway propagation | 1-2 min | Free | Free |
| **Total** | **2-3 min** | **~$0.08** | **~$3.75** |

### Status Checks

| Operation | Time | Cost |
|-----------|------|------|
| Check any ENS name | 5s | Free |
| Resolve content hash | 5s | Free |

---

## 🎯 Three-Phase Registration Explained

### Why Three Phases?

**Problem:** If you submit a registration TX, miners/bots can see it in the mempool and frontrun you (steal the name by submitting their own TX with higher gas).

**Solution:** Commitment scheme prevents this.

### How It Works

**Phase 1: Commit (30s)**
- Submit hash of (name + secret)
- No one knows what name you want
- TX confirmed on-chain

**Phase 2: Wait (60s)**
- Mandatory anti-frontrunning window
- Your commitment is timestamped
- Cannot be bypassed

**Phase 3: Register (30s)**
- Reveal name + secret
- Contract verifies commitment timestamp
- You win because your commitment was earlier

**Total time:** 2-3 minutes (mostly waiting, not blockchain speed)

---

## 👨‍💻 For Developers

### Wrapped vs Unwrapped Names

The skill automatically detects and handles both:

**Unwrapped (Legacy):**
- 2 TXs: `setSubnodeOwner` + `setResolver`
- Label must be keccak256 hash

**Wrapped (Modern):**
- 1 TX: `setSubnodeRecord`
- Label is plain string
- Supports fuses and expiry

Check with:
```bash
node scripts/check-ens-name.js yourname.eth
# Shows: "🎁 Wrapped" or "📦 Unwrapped"
```

### Manual Operations

See SKILL.md for raw contract interaction examples:
- Create subdomains via Registry or NameWrapper
- Set content hashes via Resolver
- Read contenthash and decode IPFS CIDs

---

## 📚 Resources

- **ENS Docs:** https://docs.ens.domains
- **ENS App:** https://app.ens.domains
- **eth.limo:** https://eth.limo
- **IPFS:** https://ipfs.io
- **Skill Guide:** See SKILL.md for detailed workflows

---

## 📜 License

MIT

---

## 🤝 Contributing

Built by PA (Clop Personal Assistant) for the Clop Cabinet agent team.

Improvements welcome! Focus areas:
- Gas optimization
- More gateway options
- Testnet support
- Batch operations

---

**Ready to decentralize your web presence?** Start with `register-ens-name.js --dry-run` to check availability!

---

## 💰 Detailed Cost Information

See [COSTS.md](COSTS.md) for:
- Current vs typical vs high gas scenarios
- ENS pricing tiers explained
- Cost optimization tips
- Gas price monitoring
