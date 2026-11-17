# Tools, sources and verification limits

Reviewed 2026-09-06. Use an existing compatible provider and the narrowest required read. Tools may require an account, paid tier or supported chain; discovery and documentation do not establish access. Installation never requests a new wallet or grants transaction authority.

| Need | Maintained source | Evidence limit |
| --- | --- | --- |
| Chain, code, storage, calls, logs and receipts | [Ethereum JSON-RPC](https://ethereum.org/en/developers/docs/apis/json-rpc/) through the selected provider | Pin related reads; pruned history and capped logs are coverage gaps. |
| Deployed source and launch discovery | [Etherscan source API](https://docs.etherscan.io/api-reference/endpoint/getsourcecode), [creation API](https://docs.etherscan.io/api-reference/endpoint/getcontractcreation) or the chain's verified explorer | Verify supported chain/access and source correspondence; an explorer label is not authority. |
| Pool identity, state and quotes | [Uniswap official AI tools](https://developers.uniswap.org/docs/uniswap-ai/overview) and version-matched SDK/contracts | Reuse existing read/quote surfaces; no signing or router execution is needed. |
| Token risk corroboration | [GoPlus token security](https://docs.gopluslabs.io/reference/tokensecurityusingget_1) | Unsupported or missing fields remain unknown; a scanner result is not a complete audit. |
| Source/code correspondence | [Sourcify documentation](https://docs.sourcify.dev/docs/api/) | Use the supported v2 read API; source-verification submission is a separate write. Matching bytecode does not establish economic safety. |
| Stateful experiment | [Foundry fork testing](https://getfoundry.sh/forge/tests/fork-testing) | Use a verified disposable fork, synthetic accounts and documented overrides. No remote signer or broadcast. |

The bundled helper is a small deterministic evidence utility, not a provider adapter suite. Resolve its path relative to the installed skill. Read [its actual contract](evidence-format.md) before invoking it, and keep its RPC environment private. The snapshot is a starting point; launch/pool discovery, control review and economic accounting require additional evidence.

## Hermes and portable skills

Use native [Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/) and on-demand reference loading. The selected Security pack contains this diligence skill and a separate transaction-review skill. Each skill remains self-contained when installed alone. Optional tools and helpers do not require every other Galleon pack or a custom harness runtime.

## Research credit

[Agent Chud's token-diligence prompt](https://x.com/AgentChud/status/2096259218835718273), published 2026-09-05 and reviewed 2026-09-06, motivated a dedicated workflow tying economic claims to evidence. Galleon Labs independently authored these instructions, helper code and test fixtures, using the primary specifications above and links in the topic references. No third-party prompt, code or installer is vendored. Source credit does not imply endorsement or a reproduced benchmark.
