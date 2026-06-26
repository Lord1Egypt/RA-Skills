# Postchain Client Reference

## Table of Contents

- [Overview](#overview)
- [Client Initialization](#client-initialization)
- [Signing Model](#signing-model)
- [Queries](#queries)
- [Transactions](#transactions)
- [FT4 Connection & Session](#ft4-connection--session)
- [ICCF Proof Transactions](#iccf-proof-transactions)
- [Available Client Libraries](#available-client-libraries)
- [Failover & Node Discovery](#failover--node-discovery)
- [Common Mistakes](#common-mistakes)

---

## Overview

Postchain clients are libraries for interacting with Chromia blockchain nodes. They enable sending transactions, executing queries, and managing authentication.

**Available packages:**
- **TypeScript/JS**: `postchain-client` (npm) + `@chromia/ft4` (npm)
- **Kotlin/Java**: `net.postchain.client:postchain-client` (Maven)
- **Rust**: `postchain-client` (crates.io)
- **Go**: Chromia Go client
- **C#**: Postchain C# client
- **Python**: Postchain Python client

---

## Client Initialization

### TypeScript — Direct Connection (known node)

```typescript
import { createClient } from "postchain-client";

const client = await createClient({
  nodeUrlPool: "http://localhost:7740",
  blockchainRid: "<BlockchainRID>",  // hex string
});
```

### TypeScript — Local Development (by chain index)

```typescript
const client = await createClient({
  nodeUrlPool: "http://localhost:7740",
  blockchainIid: 0,  // internal ID, default is 0 for first chain
});
```

### TypeScript — Node Discovery (production)

```typescript
const client = await createClient({
  directoryNodeUrlPool: ["https://node1.chromia.com", "https://node2.chromia.com"],
  blockchainRid: "<BlockchainRID>",
});
```

The client auto-discovers all nodes running the target blockchain by querying the directory chain.

### Key Parameters

| Parameter | Use Case |
|---|---|
| `nodeUrlPool` | Direct connection to known node(s) |
| `directoryNodeUrlPool` | Auto-discovery via system cluster directory chain |
| `blockchainRid` | Target blockchain by its Resource Identifier |
| `blockchainIid` | Target blockchain by internal ID (local dev only) |

---

## Signing Model

Postchain separates read operations (queries) from write operations (transactions). Only transactions require signing.

There are two signing approaches:

- **Direct signing** (`postchain-client`): Raw keypair signing via `signAndSendUniqueTransaction`. The Rell side validates with `op_context.get_signers()` or `op_context.is_signer()`. No FT4 required.
- **Session signing** (`@chromia/ft4`): FT4 session-based auto-signing via `session.call()`. The Rell side validates with `auth.authenticate()` and requires a matching `@extend(auth.auth_handler)`.

| Method | Package | Signing | Rell-side validation |
|---|---|---|---|
| `client.query()` | `postchain-client` | None | N/A (read-only) |
| `connection.getAllAssets()`, `connection.getAccountById()` | `@chromia/ft4` | None | N/A (read-only) |
| `session.query()` | `@chromia/ft4` | None | N/A (read-only) |
| `client.signAndSendUniqueTransaction()` | `postchain-client` | Raw keypair (`sigProvider`) | `op_context.get_signers()` / `op_context.is_signer()` |
| `session.call()` | `@chromia/ft4` | FT4 session (auto-signed) | `auth.authenticate()` + `@extend(auth.auth_handler)` |
| `session.account.transfer()` | `@chromia/ft4` | FT4 session (auto-signed) | Built-in FT4 transfer auth (requires `"T"` flag) |

---

## Queries

Queries are read-only and never require signing, regardless of how they are called:

```typescript
// Via client (no auth context)
const result = await client.query("get_all_users", {});
const user = await client.query("get_user_by_name", { name: "Alice" });

// Via session (read-only convenience — no signing even though session exists)
const data = await session.query<TReturn>({ name: "get_user_posts", args: { user_id: userId } });
```

`session.query` uses the session's client under the hood. It does **not** sign the query — queries are always unsigned on Postchain. Use it when you already have a session and want consistent calling conventions, but it behaves identically to `client.query`.

**Important**: The query name must match `<module_mount>.<query_name>` exactly. The module mount is set via `@mount("prefix")` on the module declaration in `module.rell`. If no `@mount` is set, the default prefix is the module's directory name.

---

## Transactions

### Simple Transaction (direct signing)

Requires a signature provider and explicit signers. On the Rell side, validate with `op_context.get_signers()` or `op_context.is_signer(pubkey)`:

```typescript
import { newSignatureProvider, createClient } from "postchain-client";

const sigProvider = newSignatureProvider({ privKey, pubKey });

const { status, transactionRid } = await client.signAndSendUniqueTransaction(
  {
    operations: [
      { name: "set_name", args: ["Developer"] },
    ],
    signers: [pubKey],
  },
  sigProvider
);
```

### Multiple Operations in One Transaction

All operations in a GTX transaction are atomic — they all succeed or all fail:

```typescript
const { status } = await client.signAndSendUniqueTransaction(
  {
    operations: [
      { name: "op_one", args: [arg1] },
      { name: "op_two", args: [arg2, arg3] },
    ],
    signers: [pubKey],
  },
  sigProvider
);
```

---

## FT4 Connection & Session

### Read-Only Connection (no auth)

```typescript
import { createConnection } from "@chromia/ft4";

const connection = createConnection(client);

// General queries — no signing
const assets = await connection.getAllAssets();
const account = await connection.getAccountById(accountId);
const balances = await account.getBalances();
```

### Authenticated Session (with signing)

`session.call()` auto-signs operations with the disposable session key. On the Rell side, the operation must call `auth.authenticate()` and have a matching `@extend(auth.auth_handler)`:

```typescript
import { createKeyStoreInteractor, createWeb3ProviderEvmKeyStore } from "@chromia/ft4";

const evmKeyStore = await createWeb3ProviderEvmKeyStore(window.ethereum);
const interactor = createKeyStoreInteractor(client, evmKeyStore);
const accounts = await interactor.getAccounts();

const { session, logout } = await interactor.login({
  accountId: accounts[0].id,
});

// Queries — no signing even through session
const posts = await session.query<Post[]>({ name: "get_posts", args: {} });

// Operations — auto-signed with session key
await session.call(op("create_post", "Hello"));

// Transfers — auto-signed, requires "T" flag on auth descriptor
await session.account.transfer(recipientId, assetId, amount);

// Logout when done
await logout();
```

### Session vs Direct Signing

| Feature | Session (`@chromia/ft4`) | Direct (`postchain-client`) |
|---|---|---|
| Auth model | FT4 accounts + auth descriptors | Raw pubkey signing |
| Wallet UX | Single sign for session, then auto-sign | Sign every transaction |
| Use case | User-facing dApps with wallet UX, permissions | Lightweight apps, bots, admin scripts, server-to-chain |

---

## ICCF Proof Transactions

```typescript
import { createIccfProofTx } from "postchain-client";

const { iccfTx } = createIccfProofTx(
  client,
  txToProveRid,
  txToProveHash,
  txToProveSigners,
  sourceBlockchainRid,
  targetBlockchainRid
);

// Add target operation to the proof tx, then sign and send
```

---

## Available Client Libraries

| Language | Package | Install |
|---|---|---|
| TypeScript/JS | `postchain-client` | `npm install postchain-client` |
| TypeScript/JS (FT4) | `@chromia/ft4` | `npm install @chromia/ft4` |
| Kotlin/Java | `postchain-client` | Maven (GitLab registry) |
| Rust | `postchain-client` | `cargo add postchain-client` |
| Go | Chromia Go client | GitLab |
| C# | Postchain C# | NuGet |
| Python | Postchain Python | pip |

---

## Failover & Node Discovery

### Multiple Nodes (failover pool)

```typescript
const client = await createClient({
  nodeUrlPool: [
    "http://node1:7740",
    "http://node2:7740",
    "http://node3:7740",
  ],
  blockchainRid: "<BRID>",
});
```

The client automatically fails over to another node if one is unavailable.

### Directory-Based Discovery (production recommended)

```typescript
const client = await createClient({
  directoryNodeUrlPool: ["https://system-node1.chromia.com"],
  blockchainRid: "<BRID>",
});
```

Automatically discovers all nodes running the target chain. Adapts to cluster changes.

---

## Common Mistakes

1. **Using `blockchainIid` in production**: Internal IDs are local only. Always use `blockchainRid` for deployed chains.
2. **Operation name mismatch**: Client calls `"create_user"` but module-level `@mount("my_module")` makes it `"my_module.create_user"` → silent failure. Always use `<module_mount>.<operation_name>`.
3. **Leaking admin private keys in client code**: Admin functions with `signAndSendUniqueTransaction` expose keys. Use only in testing/setup scripts, never in production client apps.
4. **Not awaiting `createClient`**: It returns a Promise. Forgetting `await` → client is undefined.
5. **Wrong argument types**: Rell `byte_array` expects `Buffer` in TypeScript, not hex strings. Use `Buffer.from(hex, "hex")`.
