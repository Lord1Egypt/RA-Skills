# Publish Notes

This directory is published to **ClawHub** as a single skill bundle that also
works as a standalone `skills.sh`-compatible package (Claude / Cursor / Codex
CLI). The same `SKILL.md` frontmatter declares both conventions, so a single
source of truth covers all clients. After publish, the skill is installable via
both `clawhub install atxswap` and `openclaw skills install atxswap` (OpenClaw
pulls from the same ClawHub registry).

> Heads up: the OpenClaw CLI itself does **not** have `skills publish` or
> `skills validate` subcommands. All publishing flows through the dedicated
> `clawhub` CLI (`npm install -g clawhub`).

## Pre-publish checklist

1. Bump versions consistently:
   - `SKILL.md` frontmatter `version`
   - `package.json` `version`
   - These two MUST match — `clawhub publish --version` overrides them at
     upload time but mismatched local values confuse `skills.sh` consumers.
2. Install dependencies inside this directory (`npm install`) so the SDK
   builds cleanly.
3. Run the local read-only checks:
   - `node scripts/wallet.js list`
   - `node scripts/query.js price`
   - `node scripts/query.js quote buy 1`
4. Confirm the folder does not include secrets, keystore files, or
   `node_modules/`. (`.clawhubignore` already excludes `node_modules/`,
   `.clawhub/`, `.clawdhub/`, `.DS_Store`, `*.log`.)
5. Make sure the parent submodule (`agentswapx/skills`) is committed and
   pushed — the published `homepage` URL points at GitHub.

## Authenticate with ClawHub

```bash
# Browser flow (opens a token-grant page)
clawhub login

# Or token flow (no browser)
clawhub login --token <YOUR_TOKEN> --no-browser

# Verify
clawhub whoami
```

## Publish

```bash
clawhub publish ./skills/atxswap \
  --slug atxswap \
  --name "ATXSwap" \
  --version 0.0.1 \
  --tags latest,atxswap,atx,bsc,trading
```

After upload there is a brief security-scan window during which `clawhub
inspect atxswap` returns "Skill is hidden while security scan is pending".

Once the scan completes, ClawHub will flag this skill as "suspicious" because
VirusTotal Code Insight detects crypto-key / external-API patterns — that is
expected for any wallet SDK and not a real warning. Users must pass `--force`
in non-interactive contexts:

```bash
clawhub install atxswap --force
```

## Verify the published skill

```bash
# Registry round-trip
clawhub inspect atxswap

# End-user simulation in a clean directory
TEST=$(mktemp -d)
cd "$TEST" && clawhub install atxswap --force
cd skills/atxswap && npm install   # pulls atxswap-sdk from npm (~15s)
node scripts/query.js              # should print usage
```

## Suggested changelog

```text
Initial ClawHub release for ATX wallet, query, swap, liquidity, and transfer
workflows on BSC. Compatible with both ClawHub/OpenClaw clients and the
standalone skills.sh runtime.
```
