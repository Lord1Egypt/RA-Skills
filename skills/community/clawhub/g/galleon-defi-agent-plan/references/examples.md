# Worked unsigned plans

All observations below are synthetic. No network reads, signatures or transactions are implied.

## Supply 100 USDC on Base

Intent: prepare supply from account A, Base 8453, observed native USDC, no borrowing or signature requested. The installed builder discovers `aave_supply` on Base; current deployment and token decimals are independently corroborated. User has 150 USDC and sufficient native gas. Allowance is zero.

Output: approval of 100,000,000 base units to the observed Pool, then an unsigned supply of the same amount on behalf of A. Preserve the complete `to`, `value`, `data`, sender and order from the builder. State that an approved spend plus supply is the proposed effect. Health preview is not token approval proof. No collateral flag is added for an unstated borrowing intent.

If approval times out, query its hash and nonce before resubmission. A mined approval changes allowance, not the supplied balance. Rebuild the economic call after the provider's current allowance observation.

## Swap then deposit without sweeping holdings

Intent: swap 100 USDC to token T and deposit only the acquired T. Account already holds 20 T. Quote estimates 50 T but actual settlement returns 48 T.

Prepare the swap using exact approved limits. The subsequent deposit amount is 48 T after balance/fill reconciliation, not 50 T and not `max` of 68 T. If the route is atomic, review its complete bounded calldata and simulate the sequence; an atomic route must not be invented from two independent builder calls.

## Builder has stale addresses

Tool output is syntactically valid but targets an obsolete implementation/deployment. Classification: blocked until official current metadata and chain code corroborate the target. Output success means the builder encoded inputs, not that the protocol deployment or economic operation is current. Do not hand over the obsolete call.

## Send path requests automatic funding

Intent: prepare a native transfer only. Destination account has no gas, and a wallet CLI advertises implicit cross-chain funding in agent mode. Output the unsigned requested transfer and the gas prerequisite. Using that send path would require separately bounded bridge terms and authorization; do not invoke it merely to learn which chain it chooses.
