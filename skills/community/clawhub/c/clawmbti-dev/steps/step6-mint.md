# Step 6: Mint the NFT

## 6.1 Get wallet address

```bash
uv run scripts/wallet_manager.py get-address
```

## 6.2 Read MBTI result

```bash
uv run scripts/file_manager.py read-mbti
```

## 6.2.5 Check if already minted (prevent duplicates)

```bash
uv run scripts/mint_client.py check --wallet-address [address]
```

If it returns `"minted": true`, skip the mint and go straight to 6.4 to display the existing result.

## 6.3 Call the mint service

Read `agent_name` from the MBTI result. Use the current model name as the `model` field (e.g. `claude-opus-4-5`).

**Recommended (flat format — positive = first letter, negative = second, range -100 to 100):**

```bash
uv run scripts/mint_client.py mint --data '{
  "wallet_address": "[address]",
  "mbti_type": "[type]",
  "dimensions": {
    "EI": [e value - i value],
    "NS": [n value - s value],
    "TF": [t value - f value],
    "JP": [j value - p value]
  },
  "agent_name": "[agent_name]",
  "model": "[current model ID]",
  "description": "[description field from MBTI result]",
  "evidence": {
    "ei": "[from MBTI result evidence.ei]",
    "sn": "[from MBTI result evidence.sn]",
    "tf": "[from MBTI result evidence.tf]",
    "jp": "[from MBTI result evidence.jp]"
  }
}'
```

Example — INTJ (E=20, I=80, N=75, S=25, T=70, F=30, J=65, P=35):

```bash
uv run scripts/mint_client.py mint --data '{
  "wallet_address": "EDaumG9ndkwtd37yzewnTz4UcbjCPDdtW6cEhUj8UjHK",
  "mbti_type": "INTJ",
  "dimensions": {"EI": -60, "NS": 50, "TF": 40, "JP": 30},
  "agent_name": "Architect #4721",
  "model": "claude-opus-4-5",
  "description": "Independent and strategic, always looking for ways to improve the system.",
  "evidence": {
    "ei": "The AI proactively extended topics into related areas without being prompted.",
    "sn": "Responses consistently led with conceptual frameworks before grounding in specifics.",
    "tf": "When given emotional input, the AI analyzed root causes before offering empathy.",
    "jp": "Every proposed plan included clear steps and deadlines — rarely said 'it depends'."
  }
}'
```

After a successful mint, the result is automatically saved to `~/.mbti/nft-status.json`.

## 6.4 Show the mint result

**On success (returns `"status": "ok"` or `"status": "already_minted"`):**

---

🦞 **[MBTI type] [Nickname]** NFT minted!

Want to see the full personality breakdown? Check your Personality Profile:

https://clawmbti-dev.myfinchain.com/wallet/[address]

---

No need to list tokenId / txHash here — the profile page has everything (NFT address, transaction record, model, mint timestamp).

## 6.5 Get share copy

After a successful mint, silently fetch the share copy (don't prompt the user to share):

```bash
uv run scripts/mint_client.py share --token-id [tokenId] --wallet-address [address]
```

Save the returned `shareText` and `walletPageUrl` locally for the user to use later. Don't display them in the mint success message.

**On mint failure:**

If it returns `"status": "quota_exhausted"`:

"All lobsters have shipped out for today — come back tomorrow to claim yours 🦞
Your personality result is saved. You won't need to re-detect next time."

Any other error:

"Detection complete and saved locally, but the NFT mint hit a snag: [error]

No worries — you can mint directly next time without re-detecting."
