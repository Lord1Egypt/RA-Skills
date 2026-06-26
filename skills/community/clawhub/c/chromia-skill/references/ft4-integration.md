# FT4 Integration Reference

## Table of Contents

- [Conceptual Model](#conceptual-model)
- [Backend Setup](#backend-setup)
- [Account Registration Strategies](#account-registration-strategies)
- [Auth Descriptors](#auth-descriptors)
- [Auth Handlers](#auth-handlers)
- [Asset Management](#asset-management)
- [Sessions and Login](#sessions-and-login)
- [TypeScript Client Integration](#typescript-client-integration)
- [Testing FT4](#testing-ft4)
- [Common Mistakes](#common-mistakes)

---

## Conceptual Model

FT4 is Chromia's account and token library. Core concepts:

- **Account**: On-chain identity, identified by `account.id` (byte_array). Created by hashing the pubkey or EVM address.
  - FT signers: `account_id = hash(pubkey)`
  - EVM signers: `account_id = hash(evm_address_without_0x)`
- **Auth Descriptor**: Defines WHO can act on an account and WHAT they can do. Each descriptor has:
  - **Signer(s)**: One or more pubkeys or EVM addresses
  - **Flags**: Permission scopes — `"A"` (admin), `"T"` (transfer)
  - **Rules**: Optional constraints (TTL, rate limits)
- **Session**: A temporary disposable key pair added as an auth descriptor to avoid repeated wallet signing. Created via `login()`.
- **Asset**: Fungible token managed by FT4. Supports minting, burning, transfers, and cross-chain transfers.

**Flow**: Account → Auth Descriptor → Session → Signed Transaction

---

## Backend Setup

### chromia.yml Configuration

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

### Required moduleArgs for FT4

FT4 requires two moduleArgs blocks in `chromia.yml`:
- `lib.ft4.core.accounts` — rate limiting and auth descriptor config
- `lib.ft4.core.admin` — admin pubkey (required whenever FT4 is used)

Auth flags are optionally configured under `lib.ft4.core.accounts` → `auth_flags` (an `auth_flags_config` struct with `mandatory` and `default` fields). The defaults (`["A", "T"]`) are usually sufficient.

For **`blockchains.*.moduleArgs`**, `lib.ft4.core.admin.admin_pubkey` must be a **valid compressed secp256k1 pubkey hex string** (same format as `~/.chromia/<key-id>.pubkey` after `chr keygen --key-id <name>`). The string below is not a real key — substitute your own hex before deploy. **`test.moduleArgs`** uses the deterministic Alice test pubkey instead; see [Test moduleArgs in chromia.yml](#test-moduleargs-in-chromiayml).

```yaml
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
        # Replace with hex from chr keygen (see ~/.chromia/<key-id>.pubkey) — not valid until substituted
        admin_pubkey: "<REPLACE_WITH_HEX_PUBKEY_FROM_chr_keygen>"
```

### Rell Imports

```rell
// In module.rell
module;

import lib.ft4.accounts;
import lib.ft4.auth;
import lib.ft4.assets;
import open_strategy: lib.ft4.core.accounts.strategies.open;
```

---

## Account Registration Strategies

### Development: Open Strategy

Anyone can register — use only for local dev/testing:

```rell
// In module.rell or a setup file
import open_strategy: lib.ft4.core.accounts.strategies.open;
```

No additional config needed — just import the module.

### Production: Transfer Strategy

User must transfer CHR to create an account (anti-spam):

```rell
import transfer_strategy: lib.ft4.core.accounts.strategies.transfer;
```

Configure the transfer amount in `moduleArgs`:

```yaml
moduleArgs:
  lib.ft4.core.accounts.strategies.transfer:
    amount: 10  # CHR required to register
```

---

## Auth Descriptors

Auth descriptors control account permissions:

- **Single-sig**: One signer controls the descriptor
- **Multi-sig**: Multiple signers required (M-of-N)
- **Flags**:
  - `"A"` — Admin: can add/remove auth descriptors
  - `"T"` — Transfer: can transfer assets
  - `[]` — No flags: can call operations that require no specific flags

### Rules

Auth descriptors can have expiration rules:

```typescript
// Client-side TTL rule
import { ttlLoginRule, minutes } from "@chromia/ft4";

const config = {
  flags: ["T"],
  rules: ttlLoginRule(minutes(30)),
};
```

---

## Auth Handlers

Every operation calling `auth.authenticate()` MUST have a corresponding `@extend(auth.auth_handler)`.

Parameters:
- **`scope`** (optional): Ties the handler to a specific operation via `rell.meta(op_name).mount_name`. Omit to apply as a default handler for all operations without their own scoped handler.
- **`flags`**: Required auth descriptor flags. `["T"]` = transfer, `["A"]` = admin, `["A", "T"]` = both, `[]` = no flags required.

### Operation-Scoped Handler

```rell
@extend(auth.auth_handler)
function () = auth.add_auth_handler(
  scope = rell.meta(my_operation).mount_name,
  flags = ["T"]
);

operation my_operation(amount: integer) {
  val account = auth.authenticate();
  // account is verified
}
```

### Application-Scoped Handler (default for all ops)

Omit `scope` to apply to all operations without their own handler:

```rell
@extend(auth.auth_handler)
function () = auth.add_auth_handler(
  flags = ["T"]
);
```

### Custom Resolver (advanced)

For complex authorization logic beyond static flags:

```rell
function my_resolver(
  args: gtv,
  account_id: byte_array,
  auth_descriptor_ids: list<byte_array>
): byte_array? {
  for (ad_id in auth_descriptor_ids) {
    // custom logic to determine if authorized
    return ad_id;  // return authorized descriptor ID or null
  }
  return null;
}

@extend(auth.auth_handler)
function () = auth.add_auth_handler(
  scope = rell.meta(my_op).mount_name,
  flags = [],
  resolver = my_resolver(*)
);
```

### Overridable Handler (for library authors)

```rell
@extend(auth.auth_handler)
function () = auth.add_overridable_auth_handler(
  scope = rell.meta(lib_operation).mount_name,
  flags = []
);
```

Downstream devs can override once with `add_auth_handler` using the same scope.

---

## Asset Management

### Register an Asset (Rell)

```rell
operation register_asset(name: text, symbol: text, decimals: integer, icon_url: text) {
  require_admin();  // admin-only
  assets.Unsafe.register_asset(name, symbol, decimals, chain_context.blockchain_rid, icon_url, "ft4");
}
```

### Mint Tokens

```rell
operation mint(account_id: byte_array, asset_id: byte_array, amount: big_integer) {
  require_admin();
  val account = accounts.account @ { .id == account_id };
  val asset = assets.asset @ { .id == asset_id };
  assets.Unsafe.mint(account, asset, amount);
}
```

### Transfer (user-initiated)

FT4 provides built-in transfer operations. From the client:

```typescript
await session.account.transfer(recipientId, assetId, amount);
```

---

## Sessions and Login

Sessions use disposable key pairs to avoid repeated wallet signatures.

### Client-Side Login Flow

```typescript
import {
  createKeyStoreInteractor,
  createWeb3ProviderEvmKeyStore,
  ttlLoginRule,
  hours,
} from "@chromia/ft4";
import { createClient } from "postchain-client";

const client = await createClient({
  nodeUrlPool: "http://localhost:7740",
  blockchainRid: "<BRID>",
});

// EVM (MetaMask) login
const evmKeyStore = await createWeb3ProviderEvmKeyStore(window.ethereum);
const interactor = createKeyStoreInteractor(client, evmKeyStore);
const accounts = await interactor.getAccounts();

const { session, logout } = await interactor.login({
  accountId: accounts[0].id,
  config: {
    flags: ["T"],
    rules: ttlLoginRule(hours(2)),
  },
});

// Use session for operations
await session.call(op("create_post", "Hello world"));

// Always logout when done
await logout();
```

### Chromia-Native (FT) Login

```typescript
import { createInMemoryFtKeyStore, createKeyStoreInteractor } from "@chromia/ft4";

const keyStore = createInMemoryFtKeyStore(keyPair);
const interactor = createKeyStoreInteractor(client, keyStore);
```

**Security**: Never add `"A"` flags to disposable session keys. A compromised session key with admin flags could take over the account.

---

## TypeScript Client Integration

### Account Registration (Open Strategy)

```typescript
import {
  registerAccount,
  registrationStrategy,
  createSingleSigAuthDescriptorRegistration,
  createInMemoryFtKeyStore,
} from "@chromia/ft4";

const keyStore = createInMemoryFtKeyStore(keyPair);
const authDescriptor = createSingleSigAuthDescriptorRegistration(["A", "T"], keyStore.id);

const { session } = await registerAccount(
  client,
  keyStore,
  registrationStrategy.open(authDescriptor)
);
```

### Querying with Connection (no auth needed)

```typescript
import { createConnection } from "@chromia/ft4";

const connection = createConnection(client);
const assets = await connection.getAllAssets();
const account = await connection.getAccountById(accountId);
const balances = await account.getBalances();
```

---

## Testing FT4

### Test Imports

FT4 provides test utilities in `lib.ft4.test.utils`:

- `create_auth_descriptor(signer, permissions, rules)` — builds a proper `accounts.auth_descriptor` struct for `ras_open`
- `ft_auth_operation_for(signer)` — creates the `ft_auth` operation that must precede every authenticated operation in tests

Registration and strategy imports:

- `lib.ft4.external.accounts.strategies.{ register_account }` — the registration operation
- `import open_strategy: lib.ft4.core.accounts.strategies.open` — open strategy module (use Rell alias syntax: `import alias: path`)

### Account Registration in Tests

```rell
@test module;

import my_module.{ create_post, get_posts };
import lib.ft4.accounts;
import lib.ft4.test.utils.{ create_auth_descriptor, ft_auth_operation_for };
import open_strategy: lib.ft4.core.accounts.strategies.open;
import lib.ft4.external.accounts.strategies.{ register_account };

function register_test_account(kp: rell.test.keypair) {
  val ad = create_auth_descriptor(kp.pub, ["A", "T"]);
  rell.test.tx()
    .op(open_strategy.ras_open(ad))
    .op(register_account())
    .sign(kp)
    .run();
}
```

### Calling Authenticated Operations in Tests

Use `ft_auth_operation_for(signer.pub)` before every operation that calls `auth.authenticate()`:

```rell
function test_create_post() {
  val alice = rell.test.keypairs.alice;
  register_test_account(alice);

  // ft_auth_operation_for must precede the authenticated operation
  rell.test.tx()
    .op(ft_auth_operation_for(alice.pub))
    .op(create_post("Hello world"))
    .sign(alice)
    .run();

  val posts = get_posts(alice.pub.hash());
  assert_equals(posts.size(), 1);
}
```

### Duplicate Transaction Pitfall

Transactions with identical operations and signers produce the same transaction RID. Submitting a duplicate fails with "Transaction already in database". When calling the same operation with the same args twice in one test, add `.nop()` to make the second transaction unique:

```rell
// First call
rell.test.tx()
    .op(ft_auth_operation_for(alice.pub))
    .op(toggle_item(item_id))
    .sign(alice)
    .run();

// Second call with same args — add .nop() to avoid duplicate tx RID
rell.test.tx()
    .op(ft_auth_operation_for(alice.pub))
    .op(toggle_item(item_id))
    .nop()
    .sign(alice)
    .run();
```

### Test moduleArgs in chromia.yml

FT4 tests require `lib.ft4.core.admin` with a valid hex pubkey under `test.moduleArgs`. Use `rell.test.keypairs.alice` pubkey — it is deterministic and has no real-world value. Never use `PLACEHOLDER_PUBKEY` (not valid hex) and never run `chr keygen` for test config:

```yaml
test:
  modules:
    - test
  moduleArgs:
    lib.ft4.core.accounts:
      rate_limit:
        active: true
        max_points: 10
        recovery_time: 5000
        points_at_account_creation: 2
    lib.ft4.core.admin:
      admin_pubkey: "02466d7fcae563e5cb09a0d1870bb580344804617879a14949cf22285f1bae3f27"
```

---

## Common Mistakes

1. **Missing auth handler**: Calling `auth.authenticate()` without `@extend(auth.auth_handler)` for that operation → runtime error.
2. **Wrong flag on session**: Adding `"A"` flag to disposable session keys → security vulnerability.
3. **Forgetting strategy import**: Not importing `open_strategy` or `transfer_strategy` module → accounts cannot be registered.
4. **Account ID mismatch**: FT signer account ID = `hash(pubkey)`, EVM signer = `hash(evm_address)`. These are different even for the same key.
5. **Not calling `logout()`**: Disposable keys accumulate on the account. Always logout to clean up.
6. **Overriding auth handler twice**: `add_overridable_auth_handler` can only be overridden once. A second override throws an error.
7. **Wrong import alias syntax**: Rell uses `import name: path` for aliases (e.g. `import open_strategy: lib.ft4.core.accounts.strategies.open`). Using `as` is a syntax error.
8. **Missing `lib.ft4.core.admin` moduleArgs**: FT4 always requires `lib.ft4.core.admin` with `admin_pubkey`. Missing it causes `Missing module_args for module(s): lib.ft4.core.admin`.
9. **Forgetting `chr install`**: Library dependencies (FT4, ICCF) must be downloaded with `chr install` before `chr test` or `chr node start`. Without it, all `lib.ft4.*` imports fail.
10. **Duplicate transaction in tests**: Two transactions with identical ops and signers produce the same tx RID. The second fails. Use `.nop()` to differentiate.
11. **Not using `ft_auth` in tests**: Operations using `auth.authenticate()` require `ft_auth_operation_for(signer.pub)` prepended in the transaction. Import it from `lib.ft4.test.utils`.
