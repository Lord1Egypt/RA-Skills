# Usage of Ergo Platform

### Why Ergo was Selected as the Path Forward for Celaut

Ergo was selected because its principles align with those of Celaut, as reflected in the Ergo Manifesto (available in [Ergo Manifesto](https://ergoplatform.org/en/blog/2021-04-26-the-ergo-manifesto/)).
Furthermore, its advanced technology and a community dedicated to these ideals reinforce its suitability.

It has been observed that no other network genuinely upholds these principles, as many tend to corporatize the products built on them, centralizing control in one way or another *(according to the developers of celaut-project/nodo).*

For this reason, Ergo is considered the path forward.

**P.D.**  Ergo was chosen as the initial network to implement the necessary contracts for Celaut, although it is not necessarily the only ledger to be used. Celaut allows the simultaneous use of multiple ledgers, providing flexibility in its implementation across different networks.


### Reputation system implementation

The reputation system in the Nodo allows nodes to share their opinion about other nodes in the network. This system leverages the **Ergo** blockchain to manage **reputation proofs**. Here's how it works:

- Each node has a **reputation proof**, represented by a **token in Ergo**.
- The boxes containing this token record the node's opinions about other reputation proofs in the network.
- In this way, each node assigns a different reputation to its peers, enabling a decentralized and transparent evaluation system.

### Payment System implementation

The payment system between nodes is also implemented on **Ergo**. Here's how it is structured:

#### 1. Client Registration and Authentication

- Each node shares its **wallet** payment address with its clients.
- Clients (other nodes or external entities) register with the node and receive a **private key** to authenticate themselves.

#### 2. ERG Deposits (Gas)

- To increase their gas amount, the client generates a **deposit token** — a **local identifier (UUID)** created and stored in the client's SQLite database, **not** an on-chain EIP-4 asset — and creates a normal **Ergo transaction** transferring a certain amount of native ERG, embedding that identifier in register **R4** of the transaction.
- The client then notifies the node once the transaction carrying the deposit token has been transferred.

#### 3. Deposit Verification

- The node verifies that the **deposit token** (the R4 identifier) belongs to the client.
- If valid and the funds have been transferred to the node's **wallet**, the client’s gas is increased according to the amount of ERGs received.
- The deposit token is then marked `payed` (the legal states are `pending` / `payed` / `rejected`).

#### 4. Wallet Management in the Nodo

The node controls a **single wallet**, derived from `ledgers.ergo.WALLET_MNEMONIC`.
The flow is:

```
client  ->  single wallet  ->  cold wallet (when both thresholds are met)
```

- **Single wallet** (hot): the address clients pay directly to, and the wallet the
  node signs with (payments to other nodes, reputation proofs). There is no separate
  receiver/auxiliary wallet and no intermediate transfer between node wallets.
- **Cold wallet** (`ledgers.ergo.payments.COLD_WALLET`): a **public address only** —
  never a mnemonic inside Nodo. Excess funds are swept here for safekeeping.

#### 5. Cold-wallet sweep

A maintenance thread periodically computes, in integer nanoERG:

```
excess = balance - HOT_WALLET_LIMITS - fee
```

and sweeps `excess` to the cold wallet only when it is at least
`COLD_WALLET_MIN_TRANSFER` **and** a valid Ergo output. The hot-wallet limit, the
transaction fee, and the technical minimum box value are always retained. When
`COLD_WALLET` is empty, nothing is swept. A configurable percentage
(`DONATION_PERCENTAGE`, default 0%) of the swept amount may go to a donation wallet.
Amounts, destination, and transaction id are logged; mnemonics never are.

`HOT_WALLET_LIMITS` and `COLD_WALLET_MIN_TRANSFER` are decimal ERG strings, parsed once
with `Decimal` into nanoERG; all subsequent arithmetic is integer nanoERG.

#### Difference Between Wallet and Address

- **Wallet**: when the node has the **mnemonic**, it can sign transactions.
- **Address**: a **public address** (e.g. the cold wallet) the node can only send to.

The node operator can manually provide the mnemonic for the single wallet if the node
has been reinstalled. This same wallet is used to add reputation proofs to the network.

### Sharing Information Between Celaut Nodes

When a node shares information with another, it provides two key elements:

1. The **ID of its reputation proof**.
2. The payment **contract**, whose `script` is the raw **ErgoTree / propositionBytes** of
   the wallet's P2PK payment boxes. A readable address is derived only locally, for UI or
   logs; it is never the value exchanged between nodes.


#### Contract Definition

```protobuf
message Contract {
    message ScriptTemplate {
        repeated string tags = 1;
        string prose = 2;
        bytes formal = 3;
    }
    message Ledger {
        repeated string tags = 1;
        string prose = 2;
        bytes formal = 3;
    }
    ScriptTemplate template = 1;
    bytes script = 2;  // Or Contract address on Ethereum-like networks.
    string token_id = 3;
    Ledger ledger = 4;
}
```

##### Reputation System
The reputation system utilizes the following fields:
- `contract`: Contains the sigma script of the box that holds each proof
- `ledger`: Specifies the ledger system in use, which is set to `"ergo"`
- `token_id`: Maps to the reputation proof ID, corresponding to the `token_id` in Ergo

##### Payment System
The payment system implements these fields:
- `contract`/`script` xattr: the raw ErgoTree/propositionBytes of the box that receives each payment
- `ledger`: Identifies the ledger system as `"ergo"`
- `script`: the raw **ErgoTree / propositionBytes** of the wallet's P2PK payment box
- `token_id`: `"ERG"` for native-ERG payments