# EIF (Ethereum Interoperability Framework) Reference

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Token Bridge Types](#token-bridge-types)
- [Event Configuration](#event-configuration)
- [Rell Libraries](#rell-libraries)
- [Common Mistakes](#common-mistakes)

---

## Overview

EIF enables Chromia to interact with Ethereum and all EVM-compatible chains (Ethereum, BNB Chain, Polygon, Base, Arbitrum, etc.). It is implemented as a GTX module added to your dApp.

**Core capabilities:**
- Read EVM events and inject them into Chromia via `__evm_block` operation
- Bridge ERC-20 tokens between EVM chains and Chromia
- Bridge ERC-721/ERC-1155 NFTs to CRC2 format
- Link EVM wallet addresses to Chromia accounts
- Support MetaMask signing for Chromia operations

---

## Architecture

EIF has three main components:

1. **EIF Core** (`eif`): Main interoperability framework
2. **Event Receiver** (`eif_event_receiver`): Listens to and processes EVM events
3. **Event Connector** (`eif_event_connector`): Integrates event data into the EIF workflow

### Event Processing Flow

1. EVM contract emits an event (e.g., `Transfer`, `StakeUpdate`)
2. **Event Receiver Chain** detects the event
3. Event is inserted into Chromia via `__evm_block` special operation
4. Bridge chain decodes and validates the event
5. Corresponding action executes on Chromia (mint, update, etc.)

---

## Configuration

### chromia.yml Setup

```yaml
blockchains:
  my_bridge:
    module: bridge_module
    config:
      eif:
        chains:
          ethereum:
            network_id: 1          # Ethereum Mainnet
            contracts:
              - "0x1234...abcd"    # ERC-20 contract address
            skip_to_height: 19000000
            events: !include ./config/events.yaml
          bsc:
            network_id: 97         # BSC Testnet
            contracts:
              - "0x7532...32D0"
            skip_to_height: 26282055
            events: !include ./config/events.yaml
      gtx:
        modules:
          - "net.postchain.eif.EifGTXModule"
      sync_ext:
          - "net.postchain.eif.EifSynchronizationInfrastructureExtension"
```

### Key Config Fields

- **`network_id`**: EVM chain ID (1 = Ethereum, 56 = BSC, 97 = BSC Testnet, 137 = Polygon)
- **`contracts`**: Array of EVM contract addresses to monitor
- **`skip_to_height`**: Block height to start reading events from (skip historical blocks)
- **`events`**: Event definitions (typically in a separate YAML file)

---

## Token Bridge Types

### 1. Token Bridge (EVM-originated token)

Used when the token was originally minted on an EVM chain:

- **Deposit**: User deposits ERC-20 into bridge contract on EVM → EIF detects event → Chromia mints equivalent FT4 tokens
- **Withdraw**: User burns FT4 tokens on Chromia → Generates withdrawal proof → User submits proof to bridge contract → Tokens released on EVM after lockup period

### 2. Reverse Token Bridge (Chromia-originated token)

Used when the token was originally minted on Chromia:

- **Bridge out**: Lock tokens on Chromia → Mint wrapped tokens on EVM
- **Bridge back**: Burn wrapped tokens on EVM → Unlock on Chromia

### Withdrawal Flow (Chromia → EVM)

1. **Burn** tokens on Chromia
2. **Generate proof** of the burn transaction
3. **Submit proof** to Token Bridge contract on EVM
4. **Wait** for security lockup period
5. **Claim** tokens on EVM

---

## Event Configuration

### events.yaml Example

```yaml
Transfer:
  parameters:
    - name: from
      type: address
      indexed: true
    - name: to
      type: address
      indexed: true
    - name: value
      type: uint256

StakeUpdate:
  parameters:
    - name: staker
      type: address
      indexed: true
    - name: amount
      type: uint256
    - name: timestamp
      type: uint256
```

### Supported EVM Types

| EVM Type | Rell Mapping |
|---|---|
| `address` | `byte_array` (20 bytes) |
| `uint256` | `big_integer` |
| `bytes32` | `byte_array` (32 bytes) |
| `bool` | `boolean` |
| `string` | `text` |

---

## Rell Libraries

Add EIF libraries to your project:

```yaml
libs:
  eif:
    registry: https://gitlab.com/chromaway/eif-lib
    path: rell/src/lib/eif
    tagOrBranch: <version>
  eif_event_receiver:
    registry: https://gitlab.com/chromaway/eif-lib
    path: rell/src/lib/eif_event_receiver
    tagOrBranch: <version>
  eif_event_connector:
    registry: https://gitlab.com/chromaway/eif-lib
    path: rell/src/lib/eif_event_connector
    tagOrBranch: <version>
```

### EVM Wallet Linking (No Bridge Required)

EIF supports linking EVM wallets to Chromia accounts without bridging. The system reads ownership data from EVM chains and takes action on Chromia:

```rell
// Check if a user owns an NFT on an EVM chain
// without requiring the NFT to be bridged
```

This enables "extension layer" patterns where Chromia adds functionality to EVM assets.

---

## Common Mistakes

1. **Missing GTX module and sync extension**: Both `EifGTXModule` AND `EifSynchronizationInfrastructureExtension` are required in config.
2. **Wrong network_id**: Using mainnet ID when testing on testnet (or vice versa) → no events detected.
3. **Not setting skip_to_height**: Starting from block 0 means scanning the entire EVM chain history — extremely slow.
4. **Event parameter mismatch**: The `events.yaml` definitions must exactly match the EVM contract's event signatures. Wrong types or missing `indexed` flags → events not decoded.
5. **Forgetting lockup period**: Withdrawals from Chromia to EVM have a security lockup. Users must wait before claiming.
