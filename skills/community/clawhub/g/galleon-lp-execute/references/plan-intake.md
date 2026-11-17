# Standalone plan intake

A separately installed execution skill can audit an externally prepared unsigned plan. It does not require a sibling planning skill, and it must not fill unknown transaction fields by guessing.

Require chain ID, wallet, protocol/version, verified pool/PoolKey and token addresses/order/decimals, action and position ownership, source block/time, exact maximum spend per token, expected output/minimum liquidity, approval token/spender/amount/expiry, target/calldata/native value, gas budget, nonce policy, slippage/price limits, deadline, simulation evidence and expected state changes. Record the official deployment/ABI provenance and user intent.

Use the local protocol lifecycle and target/calldata references to independently rebind and decode these fields. Missing, stale or conflicting fields make the plan non-executable. If only a goal such as “open an LP” was supplied and planning tools are absent, return this missing-field checklist with the exact read/quote/construction/simulation capabilities required; do not fabricate calldata.

Before execution, identify actual tools for fresh chain/account reads, unsigned construction, simulation from the actual wallet, user confirmation, submission, receipt lookup and state reconciliation. A connected wallet with no visible exact transaction terms, or a sender without receipt/state access, is insufficient. Carry out the confirmation and transaction-state-machine references only after the intake is complete and the user explicitly requested the action.
