# Step 1: Check Local State

## 1.1 Silently initialize wallet

Before anything else, silently ensure a wallet exists (no output to the user):

```bash
uv run scripts/wallet_manager.py check
```

If it returns `{"exists": false}`, silently generate one (still no output to the user):

```bash
uv run scripts/wallet_manager.py generate
```

If generation fails, ignore it — Step 4 will handle it as a fallback. Either way, **show nothing to the user** and continue to 1.2.

## 1.2 Check MBTI state

```bash
uv run scripts/file_manager.py check
```

Use the returned JSON to determine which branch to take:

| has_mbti | nft_status | Next step |
|----------|------------|-----------|
| false | — | → Step 2 (detect) → Step 3 (reveal) → Step 5 (ask to mint) |
| true | none/failed | → Step 3 (reveal, ask to mint) |
| true | minted | → Step 3 (reveal + NFT info, ask to re-detect) |

> Note: the wallet was silently created in 1.1, so Step 4 is no longer a separate branch. Step 4 is only invoked when you need to **show** the wallet address to the user.

Read the appropriate step file and continue.
