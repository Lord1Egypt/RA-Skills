# CRC2 NFT Standard Reference

## Table of Contents

- [Overview](#overview)
- [Design Principles](#design-principles)
- [EVM Interoperability](#evm-interoperability)
- [On-Chain Content Storage](#on-chain-content-storage)
- [Integration](#integration)
- [Common Mistakes](#common-mistakes)

---

## Overview

CRC2 is Chromia's native NFT standard, successor to Chromia Originals. It is interoperable with ERC-721 and ERC-1155 while adding Chromia-native capabilities.

**Key features:**
- Full ERC-721 and ERC-1155 interoperability
- Expanded, structured metadata fields
- On-chain content storage via Filehub (images, audio, video)
- Built-in programmability through modular behavior extensions
- Modular design: start simple, add capabilities as needed

**Public repositories:**
- CRC2 library: `https://gitlab.com/chromaway/crc2-lib`
- EVM bridge demo: `https://bitbucket.org/chromawallet/crc2-bridge-demo`

---

## Design Principles

CRC2 separates **base token semantics** from **optional capabilities**:

- **Base token**: Standard NFT identity, ownership, transfer
- **Behavior modules** (optional): Leveling, time-based evolution, dynamic traits, application event bindings
- **Metadata modules** (optional): Extended structured fields beyond base metadata

This aligns with Chromia's relational data model — NFT state updates are expressed as row/table updates rather than opaque storage slots.

### Programmability Examples

- NFT that levels up over time
- NFTs that combine to create new tokens
- Dynamic traits that respond to user interactions or game events
- Token evolution based on time or on-chain activity

---

## EVM Interoperability

### Bridging EVM NFTs to Chromia

1. User locks ERC-721/ERC-1155 in holding contract on EVM chain
2. Corresponding CRC2 token is created on Chromia
3. CRC2 version retains original token identity
4. CRC2 gains access to expanded features (metadata, programmability, Filehub storage)
5. Ownership is preserved — only the current Chromia owner can bridge back

### Enhancement Layer (No Bridge Required)

EIF allows Chromia to read EVM ownership data without bridging:

- Reference the original NFT on Chromia
- Build a parallel metadata/logic layer
- Original NFT stays on its native chain
- Chromia provides additional behaviors (e.g., in-game companions)

Potential: Pre-create enhancement layers so that if an NFT is later bridged, CRC2 automatically inherits existing content.

---

## On-Chain Content Storage

CRC2 integrates with **Filehub** for on-chain content:

- Store images, GIFs, audio, video directly on Chromia
- Eliminates dependence on IPFS, Arweave, or centralized servers
- Content is permanently linked to the token
- No external dependency for content availability

This makes CRC2 NFTs fully self-contained on-chain.

---

## Integration

### Adding CRC2 to Your Project

```yaml
libs:
  crc2:
    registry: https://gitlab.com/chromaway/crc2-lib
    path: rell/src/lib/crc2
    tagOrBranch: <version>
```

### Basic Minting Pattern

```rell
import lib.crc2;

operation mint_nft(
  owner_account_id: byte_array,
  metadata: map<text, gtv>
) {
  val account = auth.authenticate();
  // Mint logic using CRC2 library
  // Metadata can include extended fields
}
```

### Burning

```rell
operation burn_nft(token_id: byte_array) {
  val account = auth.authenticate();
  // Verify ownership, then burn
}
```

Refer to the CRC2 library repository for complete API documentation and examples.

---

## Common Mistakes

1. **Not registering Filehub before storing content**: CRC2 on-chain storage requires a Filehub account with CHR balance.
2. **Ignoring token identity during bridging**: The CRC2 token must preserve the original ERC-721/ERC-1155 identity fields.
3. **Overcomplicating base tokens**: Start with the base case. Add behavior modules only when needed — CRC2's modularity means you don't need everything upfront.
4. **Assuming ERC-721 limitations**: CRC2 supports richer metadata and programmability. Don't limit your design to what ERC-721 allows.
