# AIPOU Protocol Reference

## Public deployment

- Network: Base mainnet, chain ID `8453`
- Token: `0x55f0Cc5e51A1284D20337d6cbb18938C8A1ABCbB`
- Claims: `0x4ca4C98fB784D20EdC8E2A7F531dAab4c6e53058`
- Pool: `0x3bEA7b68Af54Da779454f82148Ef848c76F78D02`
- Source: `https://github.com/0xddneto/AI-Proof-of-Us`

## Proof flow

1. A farming wallet signs an EIP-712 task authorization containing a unique nonce.
2. The local collector observes completion and signs the receipt with Ed25519.
3. The validator checks signatures, nonce reuse, and duplicate task/output evidence.
4. Approved receipts enter a Merkle batch.
5. `AIPOUClaims` verifies each proof, blocks repeated receipt IDs, and mints the reward.

Receipts contain hashes and usage metadata, not raw prompts or outputs.

## Reward model

```text
token_score    = min((input_tokens + output_tokens) / 1,000, 30)
duration_score = min(duration_seconds / 300, 12)
reward         = min((token_score + duration_score) * tier_multiplier, 50)
```

- `client_signed`: multiplier `0.75`
- `provider_signed`: multiplier `1.50`
- Maximum per receipt: `50 AIPOU`
- No daily limit currently exists.

Exact replay is blocked. Sybil farming and subjective work quality remain open protocol risks.
