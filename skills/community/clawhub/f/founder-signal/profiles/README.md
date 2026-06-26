# Founder Signal Profiles

This directory stores the internal runtime profiles that Founder Signal actually runs.
After install, do not start by hand-editing files here unless you are debugging the
runtime itself.

Preferred setup workflow:

1. Fill one canonical config such as [`founder-signal.config.example.json`](/Users/weijingliunyu/.codex/worktrees/d515/founder-signal/founder-signal.config.example.json).
2. Validate it:

```bash
python3 -m founder_signal doctor --config founder-signal.config.json
```

3. Import it into an internal profile:

```bash
python3 -m founder_signal config import founder-signal.config.json
```

4. Run that profile:

```bash
python3 -m founder_signal run --profile ai-code-review
```

Shortcut:

```bash
python3 -m founder_signal run --config founder-signal.config.json
```

The shell runner also supports the shortcut:

```bash
bash scripts/run_founder_signal_once.sh --config founder-signal.config.json
```

Imported runtime profiles remain here under `profiles/*.json`.

Config notes:

- Use `platforms.reddit.communities`, `platforms.reddit.seed_urls`, and
  `platforms.reddit.excluded_urls` instead of legacy Reddit keys.
- Use `platforms.v2ex.communities` plus `discovery_providers` for SOV2EX,
  node-latest, and configured-seed topic discovery.
- Do not use placeholder Reddit URLs or V2EX topic IDs in any field; `POST_ID`,
  `REAL_ID`, `SUB`, `/slug/`, and `TOPIC_ID` examples are rejected.
- If automated fetch is blocked but an agent/browser has verified the post, add a
  `verified_evidence_snapshots` item with `platform`, `source_url`,
  `verification_method`, `verified_by`, and the observed `text_snapshot`.
- `draft.require_confirmation_before_public_publish` must remain `true`.
- Imported profiles are internal runtime artifacts; the canonical JSON config is the
  user-facing setup contract.

Legacy Reddit keys (`subreddits`, `seed_reddit_urls`, and `excluded_reddit_urls`) are
still accepted only inside existing internal profiles for backward compatibility.

File naming notes:

- `*.example.json` is for committed examples.
- `*.json` is for active profile files.

Each active profile must include:

- `profile_id`
- `enabled`
- `product_name`
- `product_one_liner`
- `target_audience`
- `keywords`
- either legacy Reddit fields or `platforms`
- `verified_evidence_snapshots`
- `discovery_mode`
- `history_ttl_days`
- `scoring_terms`
- `max_candidates`
- `max_action_cards`
