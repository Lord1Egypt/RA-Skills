# Review continuing authority

## Token allowances and typed data

An ERC-20 approval permits later spending by its spender; it need not transfer funds immediately. Read current allowance from the exact token/owner/spender tuple. Explain an unlimited approval even when current balance is small. Limit approvals to the required scope when compatible with the user's intent and token behavior; changing or revoking one is itself a wallet action.

For ERC-2612, decode the domain and message together: chain ID, verifying contract, owner, spender, value, nonce and deadline. Check live nonce and expiry. A typed signature can authorize spending without the user sending an approval transaction; “gasless” is not “no authority.” Tokens can implement variants, so do not assume the standard message type from a label. [ERC-2612 specification](https://eips.ethereum.org/EIPS/eip-2612), reviewed 2026-09-05.

Permit2 separates time-bounded allowance transfers from signature-based transfers. Inspect both the token's allowance to Permit2 and the permission granted through Permit2 to the ultimate spender; revoking one layer need not erase the other. Bind the exact token, amount, spender, expiry and relevant nonce/witness to the intended route. Do not sign opaque typed data or accept a dApp-supplied address as the canonical deployment. [Official Permit2 overview](https://developers.uniswap.org/docs/protocols/permit2/overview), reviewed 2026-09-05.

## Smart accounts, sessions and delegation

Identify the actual account type and installed authorization mechanism. Inspect permitted targets/selectors, token/native spend caps, cumulative budget, chain scope, validity window, replay/nonce protection, recipient constraints, revocation mechanism and who can alter the policy. A session described as limited may still reach a generic executor or delegatecall path that broadens its effects.

For Safe, inspect every operation in the proposed transaction, its Safe transaction hash and nonce, and current owners/threshold/modules/guard. Treat owner changes, threshold reductions, module/guard installation and delegatecall as authority changes. The existing module configuration can matter even when owner signatures look correct. Re-check onchain configuration close to execution.

Do not equate creating an unsigned Safe transaction, publishing a proposal, collecting signatures, meeting a threshold and executing it. Each has a different effect and authorization boundary. Recompute the Safe transaction hash from the exact reviewed transaction before signatures are used. [Official proposal/confirmation workflow](https://docs.safe.global/sdk/api-kit/guides/propose-and-confirm-transactions), reviewed 2026-09-05.
