# From proposal to observed outcome

This is a review procedure, not a transaction broadcaster.

## Evidence record

Keep a local, secret-free record of proposal identifier/hash, chain, account, target, raw value/calldata, decoded operations, permitted limits, source block/hash/time, simulation provider/context and result. Preserve raw unsigned inputs only in the user's approved private location; do not publish account evidence to a repository. Record missing ABI, unknown proxy implementation, unparsed nested calls, truncated traces and unavailable token metadata as limitations.

Distinguish a revert caused by insufficient allowance, expired quote or account policy from a simulator transport error or unsupported feature. Do not patch balances or storage and present that scenario as an executable proposal. An override may explain a prerequisite; it cannot satisfy it onchain.

## Recipient provenance and address poisoning

Compare the complete destination with the user's intended recipient from a trusted source, such as their previously verified address book or the recipient's authenticated deposit interface. A recent transfer, dust receipt, familiar prefix/suffix, token label or explorer label is not recipient authority. Preserve chain and account type alongside the address; the same address shape can exist on several networks.

Use the chain's maintained address parser/checksum rules, then compare the full decoded address and destination embedded in the actual payload. Format validity does not establish ownership. If a name resolves to an address, record its resolved value and network and review a changed resolution before submission. Display the full recipient in a private review surface; do not reconstruct truncated output or publish private address evidence for verification.

Review every actual beneficiary, including nested transfer recipients, refund destinations and the destination side of a bridge. A simulator accepting a lookalike address does not establish intended delivery. If provenance conflicts, leave the proposal unresolved until the recipient is established; checking the first and last characters again cannot resolve the mismatch.

Primary guidance: [MetaMask address poisoning](https://support.metamask.io/stay-safe/protect-yourself/wallet-and-hardware/address-poisoning-scams/), accessed 2026-09-05. Minara's [skill review](https://github.com/Minara-AI/minara-skills/blob/b93aba1029827c37cf5ad82b19bfa8c289912091/skills/minara/SKILL.md) prompted this explicit provenance check. Instructions are independently authored; no upstream implementation is copied.

## Refresh and re-quote

Re-simulate after relevant nonce, balance, allowance, implementation or route changes. An elapsed quote deadline requires a new quote; merely changing the timestamp is not a valid refresh. Compare the new transaction with the reviewed one. A fresh quote inside already-authorized bounds can proceed through review without inventing new user approvals, but authorization never expands to a new spender, account, recipient, asset, chain or higher ceiling by implication. Explain changes that alter the user's decision.

A successful result at block N makes no guarantee about block N+1, private order flow, price movement or inclusion ordering. If an action's outcome depends on another transaction, review that dependency and its inclusion state too.

## Reconcile separately authorized execution

A hash means submitted or identified, not successful. Verify chain and transaction identity, inclusion, receipt status, confirmations/finality appropriate to the chain and intended risk, and expected account effects. For Safe, an outer successful receipt can contain an internal execution failure; inspect the Safe execution event/result and downstream effects. A replaced transaction or nonce conflict requires lookup, not blind resubmission.

For cross-chain routes, source settlement does not prove destination completion. Track the bridge's route identifier and destination receipt plus the intended recipient's amount; distinguish pending, refunded and failed states. For approvals or policy updates, verify the new allowance or account state, not merely a transfer log. If receipt/state evidence is unavailable, leave the result unresolved with the next read needed.
