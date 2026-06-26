# ENS Basics

## What is ENS?

Ethereum Name Service (ENS) is a decentralized naming system built on Ethereum. It maps human-readable names like `clophorse.eth` to:
- Ethereum addresses (0x...)
- IPFS content hashes
- Other blockchain addresses
- Arbitrary text records

## Key Concepts

### Names

- **Primary names** (e.g., `example.eth`) - Registered through ENS registrar
- **Subdomains** (e.g., `meetup.example.eth`) - Created by the primary name owner
- **Node** - Keccak256 hash of the name, used in smart contracts

### Wrapped vs Unwrapped Names

**Unwrapped (Legacy):**
- Managed directly via ENS Registry
- Owner can create subdomains via `setSubnodeOwner`
- Simpler but fewer features

**Wrapped (Modern):**
- Names wrapped in NameWrapper ERC-1155 contract
- Registry owner becomes NameWrapper contract
- NameWrapper holds the actual ownership
- Supports fuses (permission controls)
- Required for advanced features

**How to check:**
```javascript
const registryOwner = await registry.owner(node);
if (registryOwner === NAME_WRAPPER_ADDRESS) {
  // Name is wrapped
}
```

### Contracts

**ENS Registry** (`0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e`)
- Core registry for all ENS names
- Stores owner and resolver for each node
- Always deployed at the same address

**NameWrapper** (`0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401`)
- ERC-1155 NFT contract for wrapped names
- Provides fuses (permission controls)
- Methods: `setSubnodeRecord`, `setSubnodeOwner`

**Public Resolver** (`0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63`)
- Standard resolver implementation
- Supports address, contenthash, text records
- Most names use this resolver

### Content Hash

Content hashes link ENS names to decentralized content:
- **IPFS** - Most common (`ipfs://QmABC...`)
- **IPNS** - Mutable IPFS pointers
- **Swarm** - Alternative decentralized storage
- **Arweave** - Permanent storage

**Encoding:**
```javascript
const contentHash = require('content-hash');
const encoded = '0x' + contentHash.encode('ipfs-ns', ipfsCid);
```

**Decoding:**
```javascript
const decoded = contentHash.decode(encodedHash);
// Returns: "QmABC..."
```

## ENS → IPFS Gateways

### eth.limo

**Primary gateway:** `https://yourname.eth.limo`

Features:
- Resolves ENS content hash automatically
- Serves IPFS content over HTTPS
- No client-side ENS resolution needed
- Works in any browser

Example: `https://meetup.clophorse.eth.limo`

### eth.link

**Secondary gateway:** `https://yourname.eth.link`

Similar to eth.limo, slightly different infrastructure.

### How it works

1. User visits `yourname.eth.limo`
2. Gateway resolves `yourname.eth` via ENS
3. Reads contenthash from resolver
4. Fetches content from IPFS
5. Serves over HTTPS

## Creating Subdomains

### For Unwrapped Names

```javascript
// Step 1: Create subdomain
await registry.setSubnodeOwner(parentNode, labelHash, ownerAddress);

// Step 2: Set resolver
await registry.setResolver(subnodeNode, resolverAddress);

// Step 3: Set content hash (on resolver)
await resolver.setContenthash(subnodeNode, encodedHash);
```

### For Wrapped Names

```javascript
// All in one transaction
await nameWrapper.setSubnodeRecord(
  parentNode,          // bytes32
  label,               // string
  ownerAddress,        // address
  resolverAddress,     // address
  ttl,                 // uint64 (0 = default)
  fuses,               // uint32 (0 = none)
  expiry               // uint64 (0 = inherit)
);

// Then set content hash
await resolver.setContenthash(subnodeNode, encodedHash);
```

**Key difference:** NameWrapper takes the label as a string, Registry takes keccak256(label).

## Common Patterns

### IPFS Content Publishing

1. Add content to IPFS
2. Get CID (e.g., `QmABC...`)
3. Create ENS subdomain (if needed)
4. Set contenthash on resolver
5. Access via `yourname.eth.limo`

### Subdomain for Projects

```
project.yourname.eth → IPFS with website
docs.yourname.eth    → IPFS with documentation
api.yourname.eth     → Ethereum address for API wallet
```

## Gas Costs (as of 2026)

Typical costs at 0.1 gwei base fee:

- Create subdomain (unwrapped): ~50,000 gas = $0.01
- Set resolver: ~50,000 gas = $0.01  
- Set content hash: ~100,000 gas = $0.02
- Create subdomain (wrapped): ~150,000 gas = $0.03

**Total for new subdomain with IPFS:** ~$0.04-0.05

## Resources

- **ENS Docs:** https://docs.ens.domains
- **NameWrapper Guide:** https://docs.ens.domains/wrapper/overview
- **Content Hash Spec:** https://docs.ens.domains/contract-api-reference/publicresolver#contenthash
- **eth.limo:** https://eth.limo
- **ENS App:** https://app.ens.domains
