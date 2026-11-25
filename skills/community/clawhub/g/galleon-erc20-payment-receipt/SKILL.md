---
name: galleon-erc20-payment-receipt
description: Verify a submitted same-chain ERC-20 payment against its intended token, payer, recipient and raw amount. Use when asked whether an invoice transfer arrived or when a successful transaction or explorer screenshot is the only evidence.
license: MIT
compatibility: Use an existing read-only EVM RPC or saved JSON evidence. The optional offline helper needs Node.js 20 or later. No key or wallet is needed for the example.
metadata:
  author: Andrew Wilkinson and Galleon Labs
  version: "0.3.0"
---

# Verify a token payment

Answer whether a specific transaction contains the requested transfer and how final its block is. Start with the original payment instruction and the transaction hash. If you infer the expected terms from the very log you are checking, label the result an event description and ask for the independent obligation before calling an invoice paid.

1. Confirm the chain ID, exact ERC-20 contract, intended token owner who paid, recipient and positive raw amount. Obtain decimals from a trusted token deployment when converting a display amount. A transaction submitter, relayer or spender can differ from the token owner. For fiat-denominated invoices, resolve the agreed token amount separately.
2. Read the chain, receipt, canonical block at the receipt height and the provider’s finalized head using [the read recipe](references/reads.md). Record retrieval time and provider. A missing receipt leaves pending, unknown and replaced transactions unresolved. A mismatched block requires fresh evidence.
3. Decode Transfer events emitted by the expected contract. Compare indexed sender and recipient plus the full unsigned 256-bit data amount. Keep log indices. Check for extra same-pair transfers, forwarding by the recipient, and discrepancies. A successful transaction can contain approvals, a transfer of a different token or no transfer at all.
4. Run the [offline verifier](scripts/receipt.mjs) or perform those checks with the same precision. From this skill directory, try the bundled example:

   ```sh
   node scripts/receipt.mjs examples/synthetic.json
   ```

   The synthetic owner pays 12.5 six-decimal tokens. The result is `transfer-event-matched`, raw amount `12500000`, log index `0`, finality `rpc-finalized`. Change the expected amount to `12500001` for an amount mismatch.
5. Return the network, hash, canonical height, emitter, log index, transfer parties, exact units and finality. Distinguish event evidence, recipient balance changes and offchain invoice acceptance. For fee-on-transfer, rebasing or unfamiliar token contracts, verify implementation and balance accounting before asserting net delivery. Block-boundary balances may include other transactions. Treat conflicting evidence as unresolved.

Use bridge reconciliation for cross-chain transfers. Native currency, ERC-721/1155 tokens, service delivery and bank settlement require their own evidence. Never send or retry a payment while investigating a receipt.
