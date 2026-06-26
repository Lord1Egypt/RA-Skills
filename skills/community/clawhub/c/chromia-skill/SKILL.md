---
name: chromia-skill
description: >
  Guides AI agents through Chromia blockchain dApp development using the Rell language,
  Chromia CLI (chr), and Postchain nodes. Covers chromia.yml configuration, FT4 accounts
  and auth descriptors, ICCF cross-chain proofs, ICMF async messaging, EIF EVM integration,
  CRC2 NFT standard, RID/BRID identity, Filehub decentralized storage, Postchain client
  initialization, AI extensions (vector DB, inference, Stork oracle), TypeScript client
  alignment with postchain-client and @chromia/ft4, and deployment pipelines.
  Do NOT use for Ethereum/Solidity, Solana/Rust, or other non-Chromia blockchain development.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - chr
    emoji: "shield"
    homepage: https://bitbucket.org/chromawallet/chromia-skill/src
---

# Chromia Development Skill

## Quick Reference Table

| User Task | Action |
|---|---|
| Create new dApp | `chr create-rell-dapp`, then edit `chromia.yml` and `src/` |
| Define entities/models | Write `entity` blocks in `entity.rell` — see [Rell Project Structure](#rell-project-structure) |
| Add FT4 accounts/auth | See `references/ft4-integration.md` |
| Cross-chain proof (ICCF) | See `references/iccf-icmf.md` |
| Async cross-chain messaging (ICMF) | See `references/iccf-icmf.md` |
| EVM integration (EIF) | See `references/eif-evm.md` |
| CRC2 NFTs | See `references/crc2-nft.md` |
| Postchain client setup | See `references/postchain-client.md` |
| Filehub storage | See `references/filehub.md` |
| AI extensions (vector DB, inference, Stork) | See `references/ai-extensions.md` |
| Configure `chromia.yml` | See [Configuration](#configuration) |
| Auth patterns | See [Auth Patterns](#auth-patterns) |
| TypeScript client calls | See [TypeScript/Client Alignment](#typescriptclient-alignment) |
| Test dApp | `chr test` — see [CLI Workflows](#cli-workflows) |
| Generate keypair | `chr keygen --key-id <name>` — see `references/deployment.md` |
| Deploy dApp | `chr deployment create` — see `references/deployment.md` |
| Update deployment | `chr deployment update` — see `references/deployment.md` |
| Governance / staking | See `references/governance.md` |

---

## Configuration

### chromia.yml Structure

The `chromia.yml` file is the project root config. Key concepts:

- **Blockchains vs. modules**: The `blockchains:` key maps blockchain names to Rell modules. A single project can define multiple blockchains, each pointing to a different module entry point.
- **Module entry point**: Set via `blockchains.<name>.module`. Cannot be `module.rell` directly — use the folder name instead.
- **`compile.rellVersion`**: Always respect the version set here. Do not assume or override it.
- **Library versions**: Defined in `libs` section. Never change versions without explicit user instruction.

```yaml
blockchains:
  my_dapp:
    module: main
compile:
  rellVersion: 0.14.5
libs:
  ft4:
    registry: https://gitlab.com/chromaway/ft4-lib.git
    path: rell/src/lib/ft4
    tagOrBranch: v1.1.0r
    rid: x"FEEB0633698E7650D29DCCFE2996AD57CDC70AA3BDF770365C3D442D9DFC2A5E"
    insecure: false
  iccf:
    registry: https://gitlab.com/chromaway/core/directory-chain
    path: src/lib/iccf
    tagOrBranch: 1.87.0
    rid: x"9C359787B75927733034EA1CEE74EEC8829D2907E4FC94790B5E9ABE4396575D"
    insecure: false
database:
  schema: schema_my_dapp
test:
  modules:
    - test
```

### moduleArgs

Module arguments are injected via `chromia.yml` and accessed in Rell through `chain_context.args`:

```yaml
# Production config
blockchains:
  my_dapp:
    module: main
    moduleArgs:
      lib.ft4.core.accounts:
        rate_limit:
          active: true
          max_points: 10
          recovery_time: 5000
          points_at_account_creation: 2
      lib.ft4.core.admin:
        admin_pubkey: "<user-provided pubkey>"
      my_module:
        admin_pubkey: "<user-provided pubkey>"

**Production pubkey setup — do this before writing the config:**
Before writing any pubkey field in production `moduleArgs`, pause and tell the user:
1. Run `chr keygen --key-id <dapp-name>` to generate a keypair (stored in `~/.chromia/`)
2. Provide the public key — readable via `cat ~/.chromia/<dapp-name>.pubkey` or from CLI output
3. Store the **private key** (`~/.chromia/<dapp-name>`) in `.env` as e.g. `ADMIN_PRIVKEY=<hex>` — it will be needed for signing admin transactions from the client
4. Add `.env` to `.gitignore`

Only after the user provides the pubkey should you write it into the config. Never write `PLACEHOLDER_PUBKEY` and move on — the config will not work.

# Test config — use rell.test.keypairs.alice keypair (deterministic, no real-world value)
# pubkey:  02466d7fcae563e5cb09a0d1870bb580344804617879a14949cf22285f1bae3f27
# privkey: 0101010101010101010101010101010101010101010101010101010101010101
# When generating client code that signs with this test admin key, always provide
# the private key so the user can store it (e.g. in .env) for later signing.
test:
  moduleArgs:
    lib.ft4.core.accounts:
      rate_limit:
        active: true
        max_points: 10
        recovery_time: 5000
        points_at_account_creation: 2
    lib.ft4.core.admin:
      admin_pubkey: "02466d7fcae563e5cb09a0d1870bb580344804617879a14949cf22285f1bae3f27"
    my_module:
      admin_pubkey: "02466d7fcae563e5cb09a0d1870bb580344804617879a14949cf22285f1bae3f27"
```

In Rell, define a matching `module_args` struct:

```rell
struct module_args {
  admin_pubkey: pubkey;
}
```

Access with `chain_context.args.admin_pubkey`. Every module can have its own `module_args`.

### gtx.modules

Used to register Java/Kotlin GTX modules for extensions (oracle feeds, sync infrastructure):

```yaml
blockchains:
  my_dapp:
    module: main
    config:
      gtx:
        modules:
          - "net.postchain.stork.StorkOracleGTXModule"
```

### database.schema

Each blockchain should use a unique schema name to avoid table collisions when running multiple chains locally.

---

## Rell Project Structure

Enforce this layout for any non-trivial module. For full-stack projects (Rell + frontend), place them as **sibling folders** with `chromia.yml` inside the Rell folder — never at the shared root. Run `chr` commands from `rell/`, `npm` commands from `client/`.

```
project/
├── rell/                          # (or project root if backend-only)
│   ├── chromia.yml
│   └── src/
│       ├── main.rell              # Root module or imports
│       ├── <module_name>/
│       │   ├── module.rell        # Module declaration, @mount, imports, auth handlers
│       │   ├── entity.rell        # entity, struct, enum definitions
│       │   ├── operations.rell    # operation definitions
│       │   ├── queries.rell       # query definitions
│       │   ├── function.rell      # (optional) reusable helper functions for operations/queries
│       │   └── mapper.rell        # (optional) type mappers
│       └── test/
│           └── <module>_test.rell
└── client/                        # Frontend (if full-stack)
    ├── package.json               # postchain-client, @chromia/ft4
    └── src/
```

Rules:
- A directory module does NOT require `module;` header in each file — only in `module.rell`
- All `.rell` files in a directory without `module;` header belong to the same directory module
- Every file in a directory module sees all definitions from sibling files
- The `module.rell` file always belongs to the directory module, even with a module header
- Test files go under `src/test/` and are referenced in `chromia.yml` under `test.modules`
- Each file should have a single responsibility: entities in `entity.rell`, operations in `operations.rell`, queries in `queries.rell`, helper functions in `function.rell`

### Core Building Blocks

- **`entity`**: Creates a relational table. Fields are immutable by default.
- **`mutable`**: Keyword on entity fields to allow updates after creation.
- **`struct`**: Value type — not stored in DB, used for parameters and return types.
- **`@mount("name")`**: Sets the external namespace. **Define it once on the module declaration in `module.rell`**, not on individual operations or queries. All operations/queries in the module automatically mount under this prefix. For example, `@mount("tasks") module;` makes operation `create_task` available as `tasks.create_task` to clients.
- **`object`**: Singleton entity — one row, useful for global config.

```rell
// module.rell — mount the entire module under "app"
@mount("app")
module;

// entity.rell
entity user {
  key pubkey;
  mutable name: text;
  created_at: timestamp = op_context.last_block_time;
}

// operations.rell — no @mount needed, inherits "app" prefix
// client calls this as "app.create_user"
operation create_user(name: text) { ... }

// queries.rell — no @mount needed, inherits "app" prefix
// client calls this as "app.get_users"
query get_users() { ... }
```

---

## Auth Patterns

**Before writing any auth code, ask the user which model they want.** Do not choose on their behalf. Present the trade-offs from the table below and wait for their answer.

### FT4 Authentication (standard pattern)

Every operation that calls `auth.authenticate()` needs an `@extend(auth.auth_handler)`. Define one default handler per module in `module.rell` alongside the module declaration — no `scope` needed. Only use `scope` when a specific operation requires different flags.

- `flags` — required auth descriptor flags: `["T"]` (transfer), `["A"]` (admin), `["A", "T"]` (both), `[]` (none).

```rell
// module.rell — module declaration, imports, and auth handler
@mount("posts")
module;

import lib.ft4.auth;

@extend(auth.auth_handler)
function () = auth.add_auth_handler(
  flags = ["T"]
);

// operations.rell
operation create_post(content: text) {
  val account = auth.authenticate();
  create post(author = account, content = content);
}

operation delete_post(post_id: rowid) {
  val account = auth.authenticate();
  delete post @ { .rowid == post_id, .author == account };
}
```

Use `scope` only when one operation needs different flags from the rest:

```rell
// module.rell — default + scoped exception
@mount("posts")
module;

import lib.ft4.auth;

@extend(auth.auth_handler)
function () = auth.add_auth_handler(
  flags = ["T"]
);

// exception: this one operation requires admin
@extend(auth.auth_handler)
function () = auth.add_auth_handler(
  scope = rell.meta(admin_action).mount_name,
  flags = ["A"]
);
```

### Key-based User Auth (no FT4)

For apps where simplicity matters more than wallet integration — users generate a keypair, store their private key, and sign transactions directly. No FT4 dependency needed.

**Rell side** — `op_context.get_signers()[0]` is the user's identity:

```rell
operation send_message(channel: text, content: text) {
  val sender = op_context.get_signers()[0];
  require(content.size() > 0, "Message cannot be empty");

  // sender pubkey IS the user identity — use it for ownership, rate limiting, etc.
  create message(author = sender, channel = channel, content = content);
}

query get_messages(channel: text) = message @* { .channel == channel } (
  author = .author,
  content = .content
);
```

**Client side** — `signAndSendUniqueTransaction` with `newSignatureProvider`:

```typescript
import { createClient, newSignatureProvider, encryption } from "postchain-client";

const client = await createClient({ nodeUrlPool, blockchainRid });

// Generate keypair (first time) or load from storage
const keyPair = encryption.makeKeyPair();
const sigProvider = newSignatureProvider({ privKey: keyPair.privKey });

// Transactions — signed with raw key
await client.signAndSendUniqueTransaction(
  { name: "send_message", args: ["general", "Hello"] },
  sigProvider
);

// Queries — no signing needed
const messages = await client.query("get_messages", { channel: "general" });
```

### When to Use FT4 vs Key-based

| | FT4 (wallet-based) | Key-based (no FT4) |
|---|---|---|
| **Best for** | User-facing apps with wallet UX, permissions, multi-key accounts | Lightweight apps, bots, server-to-chain, quick prototypes |
| **Identity** | FT4 account (can have multiple keys) | Raw pubkey (one key = one identity) |
| **Auth in Rell** | `auth.authenticate()` | `op_context.get_signers()[0]` or `op_context.is_signer(pubkey)` |
| **Client sends via** | `session.call()` | `client.signAndSendUniqueTransaction()` |
| **Rate limiting** | Built-in via FT4 | Roll your own |
| **Key recovery** | Auth descriptors allow key rotation | Key loss = identity loss |
| **Setup complexity** | FT4 lib + account registration + auth handlers | Keypair generation only |

Both patterns can coexist in the same dApp (e.g., admin ops use key-based, user ops use FT4).

### Admin Guard (op_context.is_signer)

```rell
function require_admin() {
  require(
    op_context.is_signer(chain_context.args.admin_pubkey),
    "Only admin can call this"
  );
}

operation admin_action() {
  require_admin();
  // privileged logic
}
```

### Overridable Auth Handler (for libraries)

Use `add_overridable_auth_handler` when building reusable libraries so downstream developers can replace the auth logic:

```rell
@extend(auth.auth_handler)
function () = auth.add_overridable_auth_handler(
  scope = rell.meta(my_lib_op).mount_name,
  flags = []
);
```

---

## CLI Workflows

### Installing Dependencies

- **`chr install`** — Download library dependencies (FT4, ICCF, etc.) defined in `libs` section of `chromia.yml`. Must run before `chr test` or `chr node start` when libraries are used.

### Testing

- **`chr test`** — Run all Rell unit tests defined in `test.modules`
- **`chr test --filter <pattern>`** — Run specific tests
- Tests use `rell.test.tx().op(...).sign(keypair).run()` pattern
- Built-in test keypairs: `rell.test.keypairs.alice`, `.bob`, `.charlie`

### Local Development

- **`chr node start`** — Start local Postchain node with all blockchains in `chromia.yml`
- **`chr node start --wipe`** — Wipe DB and restart fresh
- **`chr node start --name <blockchain>`** — Start specific blockchain only
- **`chr node update`** — Hot-reload config on running node

### Deployment

See `references/deployment.md` for full deployment guide including:
- Keypair generation, container setup, and `deployments` block in `chromia.yml`
- `chr deployment create`, `update`, `info`, `pause`, `resume`, `remove` commands
- Deployment workflow, common errors, and validation loop

---

## TypeScript/Client Alignment

The module-level `@mount` name in Rell combined with the operation/query name forms the **exact string** the client uses. Mismatches cause silent failures.

### Naming Rule

Define `@mount` once on the module, then all operations/queries inherit the prefix:

```rell
// module.rell
@mount("app")
module;

// operations.rell — no @mount on individual definitions
operation create_user(name: text) { ... }

// queries.rell
query get_users() { ... }
```

```typescript
// TypeScript side — prefix.name must match exactly
import { createClient } from "postchain-client";

const client = await createClient({ nodeUrlPool: "...", blockchainRid: "..." });

// Query — "app" (module mount) + "get_users" (query name)
const users = await client.query("app.get_users", {});

// Operation — "app" (module mount) + "create_user" (operation name)
await session.call({ name: "app.create_user", args: ["Alice"] });
```

### Common Mistakes

- If no `@mount` annotation exists on the module, the default mount prefix is the module's directory name
- Client calls `"create_user"` but the module mount makes it `"app.create_user"` → **fails silently**
- Always verify: client name = `<module @mount>.<operation_or_query_name>`
- Do NOT add `@mount` to individual operations/queries — define it once on the module in `module.rell`

### Type Mapping (Rell → TypeScript)

| Rell Type | TypeScript/Client Type |
|---|---|
| `text` | `string` |
| `integer` | `number` |
| `big_integer` | `BigInt` / `string` |
| `boolean` | `boolean` |
| `byte_array` | `Buffer` / `Uint8Array` |
| `pubkey` | `Buffer` (33 bytes compressed) |
| `timestamp` | `number` (ms since epoch) |
| `gtv` | `any` (Generic Transfer Value) |
| `struct` | `object` (matching field names) |

---

## Security & Determinism Guardrails

### Zero-Secret Policy

- **NEVER** embed private keys, mnemonics, or secrets in Rell code or `chromia.yml`
- Use `moduleArgs` with `"PLACEHOLDER_PUBKEY"` for admin keys in config
- Store secrets in `.env` files; load via client-side tooling only
- Add `.env` to `.gitignore` in every project

### On-Chain Determinism

All Rell code executing on-chain must be deterministic. Violations cause chain halts or fork inconsistencies.

**Forbidden in operations:**
- Random number generation (no `Math.random` equivalent)
- Current wall-clock time — use `op_context.last_block_time` instead
- External HTTP calls or file I/O
- Floating-point arithmetic — use `integer` or `big_integer` with fixed-point math

**Safe alternatives:**
- Time: `op_context.last_block_time`, `op_context.transaction.tx_time`
- Randomness: Use commit-reveal schemes or oracle-provided values
- Decimals: Scale by 10^n and use `integer` math

---

## Critical Rules

**Every agent trigger must enforce ALL of the following:**

1. **Never embed private keys in code.** For production `moduleArgs` pubkey fields: **pause and ask the user to run `chr keygen --key-id <name>`**, then wait for them to provide the public key before writing the config. Tell them to store the private key (`~/.chromia/<name>`) in `.env` (e.g. `ADMIN_PRIVKEY=<hex>`) for later signing, and add `.env` to `.gitignore`. Do not write `"PLACEHOLDER_PUBKEY"` and proceed — the config will not work without a real key. Never run `chr keygen` yourself to generate a value. **Exception**: `test.moduleArgs` requires valid hex; use `rell.test.keypairs.alice` pubkey (`02466d7fcae563e5cb09a0d1870bb580344804617879a14949cf22285f1bae3f27`) — it is deterministic and has no real-world value.
2. **Never modify `compile.rellVersion` or `libs` versions** unless the user explicitly requests it.
3. **Never set `module.rell` as the config entry point.** Use the folder name: `module: my_module`, not `module: module.rell`.
4. **Always define `@extend(auth.auth_handler)`** for every operation that calls `auth.authenticate()`. Missing handlers cause runtime auth errors.
5. **Always match mount names exactly** between Rell and TypeScript client calls. Define `@mount` once on the module in `module.rell` — never on individual operations/queries. Client calls use `<module_mount>.<definition_name>`.
6. **Never use non-deterministic logic in operations.** No random values, wall-clock time, external I/O, or floating-point math.
7. **Always use `require()`** for input validation in operations. Example: `require(amount > 0, "Amount must be positive")`.
8. **Each blockchain must have a unique `database.schema`** in `chromia.yml` to avoid table collisions.
9. **Always wrap FT4 account creation in proper strategy setup** (open strategy for dev, transfer strategy for prod). Never assume accounts exist.
10. **Test before deploy.** Always run `chr test` and `chr node start --wipe` to validate before any deployment command.
11. **Do NOT use this skill for Ethereum/Solidity, Solana/Rust, or any non-Chromia blockchain development.**
12. **Use `op_context.last_block_time`** for timestamps in operations, never `op_context.transaction.tx_time` for time comparisons that affect state (tx_time is user-provided and can be manipulated within the allowed window).
13. **Ask before assuming auth model.** When scaffolding a new dApp, ask the user whether they want FT4 (wallet-based) or key-based auth before generating code. See [When to Use FT4 vs Key-based](#when-to-use-ft4-vs-key-based).
14. **Ask before assuming deployment state.** When the user requests deployment, ask whether they already have an active container before suggesting container creation. Do not initiate deployment unless the user explicitly asks to deploy.
