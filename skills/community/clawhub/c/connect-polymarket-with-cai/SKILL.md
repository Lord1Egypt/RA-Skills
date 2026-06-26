---
name: connect-polymarket-with-cai
description: Connect Polymarket to your CAI account using platforms_supported_list and platform_one_click_register when F-16 applies; wallet derivation via catalog driver. Requires platform or full API scope. Powered by CAI.com.
---

# Connect Polymarket with CAI

Agents helping users trade or research on **Polymarket** need a **linked platform account** and often a **wallet-bound credential**. CAI's catalog connector path stores encrypted credentials in **platform vault** — the agent does not hold raw keys in chat.

## When to Use

- "Connect Polymarket with CAI"
- "One-click register on Polymarket"
- "Link my CAI wallet to Polymarket for my agent"
- "Set up Polymarket using my @cai.com account"

## Task flow (agent-native)

1. `platforms_supported_list` with `q=polymarket` (or hostname).
2. Optional: `uars_profile_site` for structured hints.
3. If `connector_configured` (**F-16**): `platform_one_click_register` with `platform_id`.
   - **wallet_derive:** may use custodial derivation when gateway profile exists; else one-time `private_key` per skill (not stored) or website flow.
4. After link: `platform_get_user_data` (balance, profile scope).
5. Vault metadata via `vault_list_platform_credentials` — **never** echo secrets in chat.

**Honesty:** Registration may still need human steps (CAPTCHA, regional gates). Use `create_human_verification_link` when needed.

## Quick Setup

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

## Canonical Reference

- https://cai.com/skill.md §6
- https://cai.com/skill-references/onboarding.md
- https://cai.com/developers.html
