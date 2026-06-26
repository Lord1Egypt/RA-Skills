---
name: ens-manager
description: Register ENS names, create subdomains, and publish IPFS sites without manual contract calls
version: 1.2.0
license: MIT
requirements:
  - Node.js 18+
  - viem ^1.20.0 (core, always required)
  - content-hash ^2.5.2 (optional, only for IPFS features)
  - Ethereum wallet keystore or private key
  - ETH for gas and registration
---

# ENS Manager

Complete ENS name management: register new `.eth` names, create subdomains, and publish IPFS content to decentralized gateways.

## Quick Start

### Register New ENS Name

```bash
# Check availability and price (dry run)
node scripts/register-ens-name.js mynewname --dry-run

# Register for 1 year
node scripts/register-ens-name.js mynewname \
  --years 1 \
  --keystore /path/to/keystore.enc \
  --password "your-password"
```

**What happens:**
1. **Phase 1:** Makes commitment on-chain (anti-frontrunning)
2. **Phase 2:** Waits 60 seconds (required minimum)
3. **Phase 3:** Registers name with payment

**Cost:** ~$5-20 USD/year (varies by name length and demand)

### Check ENS Name Status

```bash
node scripts/check-ens-name.js yourname.eth
```

Shows ownership, wrapped status, resolver, and content hash.

### Create Subdomain with IPFS

```bash
node scripts/create-subdomain-ipfs.js yourname.eth subdomain QmIPFS123... \
  --keystore /path/to/keystore.enc \
  --password "your-password"
```

Creates `subdomain.yourname.eth` and sets its IPFS content hash in one command.

---

## Complete Workflows

### 1. Register New ENS Name (Full Process)

**Scenario:** You want to own `mynewname.eth`

#### Step 1: Check Availability

```bash
node scripts/register-ens-name.js mynewname --dry-run
```

**Output:**
```
🦞 ENS Name Registration
========================
📛 Name: mynewname.eth
⏱️  Duration: 1 year

🔍 Checking availability...
✅ Name is available!

💰 Calculating price...
   Registration cost: 0.008 ETH
   (for 1 year)

✅ Dry run complete.
```

#### Step 2: Register

```bash
node scripts/register-ens-name.js mynewname \
  --years 1 \
  --keystore ~/.openclaw/workspace/wallet-keystore.enc \
  --password "keystore-password"
```

**What happens (three phases):**

**Phase 1: Commitment (TX 1)**
```
📝 Phase 1: Making commitment...
   Commitment: 0xabc123...
   Secret: 0xdef456...
   TX: 0x789...
   Waiting for confirmation...
```

The commitment hash prevents frontrunning (someone stealing your name by seeing your TX and submitting theirs first with higher gas).

**Phase 2: Wait 60 Seconds**
```
⏳ Phase 2: Waiting 60 seconds (anti-frontrunning protection)...
   60 seconds remaining...
   59 seconds remaining...
   ...
   ✅ Wait complete!
```

This mandatory wait ensures your commitment is on-chain before registration.

**Phase 3: Registration (TX 2 with payment)**
```
📝 Phase 3: Registering name...
   Sending 0.008 ETH...
   TX: 0xghi789...

🎉 Registration complete!

📛 Your ENS name: mynewname.eth
🔍 View on ENS: https://app.ens.domains/mynewname.eth
🔗 Registry TX: https://etherscan.io/tx/0xghi789...

Next steps:
  1. Set your address: ens.domains → Records → ETH Address
  2. Create subdomains: node create-subdomain-ipfs.js
  3. Set reverse record: ens.domains → My Account → Primary Name
```

**Total time:** ~2-3 minutes (60s wait + TX confirmations)  
**Total cost:** Registration price + ~$2-4 gas (at 10 gwei)

---

### 2. Publishing a Website to ENS

**Scenario:** You have a static website and want to publish it at `meetup.yourname.eth.limo`

#### Prerequisites

- You own `yourname.eth` (registered via Step 1 or app.ens.domains)
- Website files ready
- IPFS access (local node or Infura/Pinata)

#### Steps

**1. Add website to IPFS:**

```bash
ipfs add -r ./website
# Output: added QmABC123... website
```

**2. Create ENS subdomain and set content hash:**

```bash
node scripts/create-subdomain-ipfs.js yourname.eth meetup QmABC123... \
  --keystore ~/.openclaw/workspace/wallet-keystore.enc \
  --password "keystore-password"
```

**3. Access your site:**

Open `https://meetup.yourname.eth.limo` in any browser!

**Cost:** ~$0.05 (at 0.1 gwei base fee)

---

### 3. Updating IPFS Content

**Scenario:** You updated your website and have a new IPFS CID

**Option A: Use viem directly**

```javascript
const { createWalletClient, http, namehash } = require('viem');
const { mainnet } = require('viem/chains');
const contentHash = require('content-hash');

const node = namehash('subdomain.yourname.eth');
const encodedHash = '0x' + contentHash.encode('ipfs-ns', newCid);

await walletClient.writeContract({
  address: PUBLIC_RESOLVER,
  abi: [{
    name: 'setContenthash',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'node', type: 'bytes32' },
      { name: 'hash', type: 'bytes' }
    ],
    outputs: []
  }],
  functionName: 'setContenthash',
  args: [node, encodedHash]
});
```

**Option B: Use ENS App**

1. Go to https://app.ens.domains/subdomain.yourname.eth
2. Click "Records"
3. Edit "Content Hash"
4. Paste new IPFS CID
5. Save (sign TX)

---

### 4. Checking What's Published

```bash
node scripts/check-ens-name.js meetup.yourname.eth
```

Shows current IPFS CID and eth.limo URL.

---

## Contract Addresses (Ethereum Mainnet)

**All operations use these addresses:**

```javascript
// Core ENS contracts
const ENS_REGISTRY = '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e';

// Registration (.eth names)
const ETH_REGISTRAR_CONTROLLER = '0x253553366Da8546fC250F225fe3d25d0C782303b';

// Wrapped names (modern, with fuses)
const NAME_WRAPPER = '0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401';

// Default resolver (most common)
const PUBLIC_RESOLVER = '0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63';
```

**Where they're used:**

- **ENS_REGISTRY:** Base registry for all names (ownership, resolvers)
- **ETH_REGISTRAR_CONTROLLER:** Register/renew `.eth` names (3-phase process)
- **NAME_WRAPPER:** Create subdomains for wrapped names
- **PUBLIC_RESOLVER:** Resolve names to addresses/content hashes

---

## Three-Phase Registration Process

### Why Three Phases?

**Problem:** If you submit a registration transaction, miners or bots can see it in the mempool and frontrun you (submit their own TX with higher gas to steal the name).

**Solution:** Commitment scheme prevents this:

1. **Commit:** Submit a hash of (name + secret). No one knows what name you want.
2. **Wait:** 60 seconds minimum. Your commitment is now on-chain and timestamped.
3. **Register:** Reveal the name + secret. Since your commitment was earlier, you win.

### Phase 1: Commitment

**What happens:**
```javascript
const commitment = keccak256(
  encodePacked(
    ['string', 'address', 'uint256', 'bytes32', 'address', 'bytes[]', 'bool', 'uint16'],
    [
      name,              // 'mynewname' (without .eth)
      owner,             // Your wallet address
      duration,          // 31536000 (1 year in seconds)
      secret,            // Random bytes32 (generated)
      resolver,          // PUBLIC_RESOLVER
      [],                // data (empty for basic registration)
      true,              // reverseRecord (set primary name)
      0                  // ownerControlledFuses (0 = none)
    ]
  )
);

// Submit to ETHRegistrarController
await controller.commit(commitment);
```

**Gas cost:** ~45,000 gas (~$1-2 at 10 gwei)

### Phase 2: Wait

**Mandatory 60-second wait** ensures:
- Your commitment is confirmed on-chain
- Timestamp is set
- You can't be frontrun

**Technical reason:** The contract checks that `block.timestamp >= commitmentTimestamp + 60 seconds` when you register.

### Phase 3: Registration

**What happens:**
```javascript
await controller.register(
  name,              // 'mynewname'
  owner,             // Your address
  duration,          // 31536000 (1 year)
  secret,            // Same secret from commitment
  resolver,          // PUBLIC_RESOLVER
  [],                // data
  true,              // reverseRecord
  0,                 // fuses
  { value: price }   // Payment in ETH
);
```

**Gas cost:** ~150,000 gas (~$3-5 at 10 gwei) + registration price

**Total registration:** ~$4-7 gas + registration price (~$5-20/year)

---

## Wrapped vs Unwrapped Names

**Check if wrapped:**
```bash
node scripts/check-ens-name.js yourname.eth
```

Look for "🎁 Wrapped (NameWrapper)" or "📦 Unwrapped (Registry)".

**Key differences:**

| Feature | Wrapped | Unwrapped |
|---------|---------|-----------|
| Subdomain creation | `NameWrapper.setSubnodeRecord` | `Registry.setSubnodeOwner` + `Registry.setResolver` |
| Label parameter | String (`"meetup"`) | Bytes32 hash (keccak256) |
| Owner location | NameWrapper ERC-1155 | Registry mapping |
| Advanced features | Fuses, expiry | None |

The `create-subdomain-ipfs.js` script handles both automatically.

---


## Current vs Typical Gas Costs

Gas costs vary based on network congestion. The skill shows real-time costs during dry-run.

### Registration (2 TXs)

**Current conditions (0.22 gwei - very low):**
- Commitment: 45,000 gas = $0.02
- Registration: 265,000 gas = $0.15
- **Total gas: $0.17**

**Typical conditions (10 gwei - normal):**
- Commitment: 45,000 gas = $1.13
- Registration: 265,000 gas = $6.63
- **Total gas: $7.75**

### ENS Name Pricing Tiers (Annual Rental)

| Name Length | Cost/Year | Example |
|-------------|-----------|---------|
| 3 characters | ~$773 | `abc.eth` |
| 4 characters | ~$193 | `cool.eth` |
| 5+ characters | ~$6 | `hello.eth`, `example.eth` |

### Complete Registration Examples

**5-letter name (most common):**
- Current: Name ($6) + Gas ($0.17) = **$6.17 total**
- Typical: Name ($6) + Gas ($7.75) = **$13.75 total**

**4-letter name:**
- Current: Name ($193) + Gas ($0.17) = **$193.17 total**
- Typical: Name ($193) + Gas ($7.75) = **$200.75 total**

**Recommendation:** Use `--dry-run` to check current costs before registering.

See [COSTS.md](COSTS.md) for detailed cost breakdowns and optimization tips.

---

## Troubleshooting

### Registration: "Name not available"

The name is already registered. Try:
```bash
node scripts/check-ens-name.js <name>.eth
```

To see who owns it and when it expires.

### Registration: "insufficient funds"

You need ETH for:
1. Registration price (~$5-20 for most names)
2. Gas fees (~$4-7)

Check balance:
```bash
# In script or cast
const balance = await publicClient.getBalance({ address });
console.log('Balance:', formatEther(balance), 'ETH');
```

### Registration: "Commitment not found" or "Too soon"

If you see this during Phase 3:
- **Too soon:** Wait the full 60 seconds
- **Commitment not found:** Your Phase 1 TX didn't confirm yet. Wait longer or check TX status.

### Transaction reverts

Common causes:
1. **Not the owner** - You must own the parent name to create subdomains
2. **Name is wrapped** - Use NameWrapper methods, not Registry
3. **Gas limit too low** - Increase `gas` parameter
4. **Commitment too old** - If you wait >24 hours between Phase 1 and 3, start over

### Content not appearing on eth.limo

1. Wait a few minutes (DNS propagation)
2. Check content hash is set: `node scripts/check-ens-name.js yourname.eth`
3. Verify IPFS CID is accessible: `https://ipfs.io/ipfs/YOUR_CID`
4. Check resolver is PUBLIC_RESOLVER (most gateways only read from it)

---

## Manual Operations (Advanced)

### Unwrapped Name: Create Subdomain

```javascript
const { keccak256, encodePacked } = require('viem');

// 1. Create subdomain
const parentNode = namehash('yourname.eth');
const labelHash = keccak256(encodePacked(['string'], ['subdomain']));

await walletClient.writeContract({
  address: ENS_REGISTRY,
  abi: [{
    name: 'setSubnodeOwner',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'node', type: 'bytes32' },
      { name: 'label', type: 'bytes32' },
      { name: 'owner', type: 'address' }
    ],
    outputs: [{ name: '', type: 'bytes32' }]
  }],
  functionName: 'setSubnodeOwner',
  args: [parentNode, labelHash, ownerAddress]
});

// 2. Set resolver
const subnode = namehash('subdomain.yourname.eth');

await walletClient.writeContract({
  address: ENS_REGISTRY,
  abi: [{
    name: 'setResolver',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'node', type: 'bytes32' },
      { name: 'resolver', type: 'address' }
    ],
    outputs: []
  }],
  functionName: 'setResolver',
  args: [subnode, PUBLIC_RESOLVER]
});
```

### Wrapped Name: Create Subdomain

```javascript
await walletClient.writeContract({
  address: NAME_WRAPPER,
  abi: [{
    name: 'setSubnodeRecord',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'parentNode', type: 'bytes32' },
      { name: 'label', type: 'string' },
      { name: 'owner', type: 'address' },
      { name: 'resolver', type: 'address' },
      { name: 'ttl', type: 'uint64' },
      { name: 'fuses', type: 'uint32' },
      { name: 'expiry', type: 'uint64' }
    ],
    outputs: [{ name: '', type: 'bytes32' }]
  }],
  functionName: 'setSubnodeRecord',
  args: [
    namehash('yourname.eth'),  // parent node
    'subdomain',                // label (string!)
    ownerAddress,               // owner
    PUBLIC_RESOLVER,            // resolver
    0n,                         // ttl (0 = default)
    0,                          // fuses (0 = none)
    0n                          // expiry (0 = inherit from parent)
  ]
});
```

---

## IPFS Content Hash

### Encoding CID

```javascript
const contentHash = require('content-hash');
const ipfsCid = 'QmABC123...';
const encoded = '0x' + contentHash.encode('ipfs-ns', ipfsCid);
```

### Setting Content Hash

```javascript
await walletClient.writeContract({
  address: PUBLIC_RESOLVER,
  abi: [{
    name: 'setContenthash',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'node', type: 'bytes32' },
      { name: 'hash', type: 'bytes' }
    ],
    outputs: []
  }],
  functionName: 'setContenthash',
  args: [namehash('subdomain.yourname.eth'), encodedHash]
});
```

### Reading Content Hash

```javascript
const contenthash = await publicClient.readContract({
  address: resolverAddress,
  abi: [{
    name: 'contenthash',
    type: 'function',
    stateMutability: 'view',
    inputs: [{ name: 'node', type: 'bytes32' }],
    outputs: [{ name: '', type: 'bytes' }]
  }],
  functionName: 'contenthash',
  args: [namehash('subdomain.yourname.eth')]
});

if (contenthash && contenthash !== '0x') {
  const decoded = contentHash.decode(contenthash);
  console.log('IPFS CID:', decoded);
}
```

---

## Gateway Access

After setting a content hash, the subdomain becomes accessible via:

- **eth.limo:** `https://subdomain.yourname.eth.limo`
- **eth.link:** `https://subdomain.yourname.eth.link`
- **IPFS directly:** `https://ipfs.io/ipfs/QmABC123...`
- **dweb.link:** `https://QmABC123....ipfs.dweb.link/`

**Note:** eth.limo/eth.link may take a few minutes to update after setting a new content hash.

---

## Resources

- **ENS Documentation:** https://docs.ens.domains
- **eth.limo:** https://eth.limo
- **ENS App (UI):** https://app.ens.domains
- **NameWrapper Guide:** https://docs.ens.domains/wrapper/overview
- **Content Hash Spec:** See `references/ens-basics.md`
- **Registrar Controller:** https://etherscan.io/address/0x253553366Da8546fC250F225fe3d25d0C782303b

For detailed ENS concepts, wrapped vs unwrapped differences, and content hash encoding, read `references/ens-basics.md`.
