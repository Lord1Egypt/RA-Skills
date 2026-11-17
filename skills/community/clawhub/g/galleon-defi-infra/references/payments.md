# Payments, sponsorship and permission boundaries

An agent's data budget, gas budget and investment capital are separate limits. Before enabling a paying tool, identify the payer, chain, token, maximum per request and cumulative spend, expiry, permitted destinations and revocation path. Confirm those limits at the wallet/provider layer. A prompt constraint alone is not enforcement.

[Coinbase's account comparison](https://docs.cdp.coinbase.com/x402/agentic-accounts/coinbase-for-agents) labels x402 for Coinbase for Agents as coming soon. [Agentic Wallet](https://docs.cdp.coinbase.com/x402/agentic-accounts/agentic-wallet) already supports x402. Do not turn a future account feature into a setup dependency.

Prefer the provider's supported payment client rather than implementing authorization signing. A paid API request needs an approved resource, quoted asset/amount/network, budget and expiry. After an ambiguous payment, reconcile the provider's payment receipt/status before retrying; a fresh HTTP request may produce another charge. Distinguish payment acceptance from successful delivery of useful data.

Alchemy's [x402 guide](https://www.alchemy.com/docs/x402-payments) covers third-party API payments; its CLI exposes quote-only `alchemy x402 request <url> --estimate`. Automated payment uses a maximum payment argument and a signer, which must be separately authorized. This is distinct from Alchemy's global `--x402` mode for authenticating to its own APIs. Do not enable either during a general readiness check.

[Coinbase payments MCP setup](https://docs.cdp.coinbase.com/agentic-wallet/mcp/quickstart) uses `@coinbase/payments-mcp` as an installer, not the stdio server itself. Reviewed installer 1.0.5 downloads a separate runtime and generates a `node <absolute-install-path>/bundle.js` connection. For Hermes, inspect the generated connection and exact runtime version before adapting it. Do not register the installer as a server or assume pinning the installer pins the downloaded runtime. Wallet authentication, funding and discovery/payment tools remain explicit steps.

Gas sponsorship is a billing arrangement, not free unlimited execution. Check sponsor policy, eligible calls, chain, quota and fallback payer. A simulation or sponsorship quote does not establish authorization or settlement.
