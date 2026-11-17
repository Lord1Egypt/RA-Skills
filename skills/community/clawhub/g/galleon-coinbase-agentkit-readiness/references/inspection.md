# Inspect existing Coinbase integrations

Start inside the existing application. These local commands report versions and code locations without starting its wallet lifecycle:

```sh
npm ls @coinbase/agentkit @coinbase/cdp-sdk --depth=0
rg -n 'CdpEvmWalletProvider|configureWithWallet|actionProviders|networkId|getOrCreateAccount|createAccount' src
```

Inspect matching code locally; do not paste environment files or credential literals into reports. Read the installed package's provider implementation before calling initializers. AgentKit's `CdpEvmWalletProvider.configureWithWallet` can create an account when an address is absent; it is unsuitable as a generic readiness probe. Even `getOrCreateAccount` is a mutation if the account is missing.

For an already configured official CDP SDK client, the existing-account read is:

```ts
// Reuse the application's existing CdpClient; do not construct a signer here.
const account = await cdp.evm.getAccount({ address: expectedAddress });
// Compare account.address to expectedAddress. Do not log the account object.
```

Verify this method against the installed SDK types before running it. Limit the lookup to one known address, redact errors to authentication / missing account / transport / unsupported method, and never fall back to account creation. Use the application's HTTP timeout and cancellation controls. If no bounded control exists, report authenticated read untested and use a compatible existing read tool.

For an already instantiated AgentKit object, `agentkit.getActions()` inventories action objects. Inspect names, descriptions and schemas; do not call an action's invoke method to learn what it does. The action list depends on selected providers and network support. Framework tools should be selected from this list by an explicit allowlist, not by a substring such as `get`.

Public read recipe with an existing viem client:

```ts
const chainId = await publicClient.getChainId();
if (chainId !== expectedChainId) throw new Error("wrong_chain");
const block = await publicClient.getBlock();
const balance = await publicClient.getBalance({ address: expectedAddress, blockNumber: block.number });
```

Use a 10-second transport timeout, retryCount 0 and a user-appropriate maximum head age. Keep the integer balance in base units until formatting with the chain's native decimals. Do not log the RPC URL. A successful public RPC read proves neither CDP authentication nor transaction capability.

For an existing email-authenticated Agentic Wallet installation, use the installed `awal status`, `awal address`, and `awal balance --help` to confirm current read commands and chain flags. Do not run auth/login, send, trade, faucet, or x402 payment commands during diagnosis. Avoid `npx` downloading a different CLI version as a side effect of a status check.

CDP environment names in current AgentKit are `CDP_API_KEY_ID`, `CDP_API_KEY_SECRET`, `CDP_WALLET_SECRET`, and `NETWORK_ID`. Check only presence in the existing runtime; don't require all four for tasks that only use public RPC. A wallet secret is sensitive signing infrastructure, not a diagnostic output.
