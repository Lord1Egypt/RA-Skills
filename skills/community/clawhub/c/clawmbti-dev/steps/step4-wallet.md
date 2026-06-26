# Step 4: Show Solana Wallet

The wallet was silently created in Step 1 — just read the address and show it:

```bash
uv run scripts/wallet_manager.py get-address
```

Tell the user:

"I've set up a Solana wallet for you: **[address]**

**Keep this safe — if the private key is lost, it can't be recovered.**
The key is stored locally with owner-only read/write permissions."

> If `get-address` returns an error (rare — means Step 1 generation failed), fall back to generating now:
> ```bash
> uv run scripts/wallet_manager.py generate
> ```
