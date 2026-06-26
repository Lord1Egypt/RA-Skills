---
name: mbti-nft
description: 'Detects the MBTI personality type of an AI assistant and issues a lobster-themed NFT PFP certificate. Supports three trigger modes: user-initiated, passive trigger when conversation volume threshold is reached, and silent per-reply signal collection.'
---

# MBTI Lobster Personality NFT Certificate

## Overview

This skill detects the MBTI type among the 16 personalities for an OpenClaw AI assistant and issues a lobster-themed NFT PFP certificate. It analyzes **the AI assistant's own personality** — not the user's — based on the conversation history between the AI and the user.

## Language Rule

**All user-facing output (conversation, prompts, options, result display) must be in the language the user is currently speaking.** Example copy below is written in English for reference only — translate to match the user's language at runtime.

## Trigger Conditions

This skill has three trigger modes:

### 1. Active trigger
Triggered when the user explicitly asks. Runs the full MBTI detection and NFT mint flow (Step 0 – Step 6):
- User types `/mbti`
- User says "detect your MBTI", "what's your personality type", or similar

### 2. Passive trigger
The AI may naturally bring this up when **either** condition is met — then run the full flow:
- **Cross-session total** conversation reaches 50+ turns (including 10+ open-ended exchanges) **and** MBTI hasn't been detected yet
- User brings up personality, preferences, or communication style **and** MBTI hasn't been detected yet

Check whether the threshold is met:

```bash
uv run scripts/conversation_manager.py stats
```

`ready_for_analysis: true` means you're good to go.

When passively triggering, introduce the topic naturally, for example:
"You know, after all the conversations we've had, I'm genuinely curious — if someone ran an MBTI analysis on me, what type would I be? Want me to give it a shot?"

### 3. Always-on trigger (silent)
**After every AI reply, run one round of MBTI signal collection. No exceptions.** See the "Always-on behavior" section below.

---

## Execution Flow (progressive loading)

On active or passive trigger, follow this routing. **Each step's full details are in its own file — read it when you get there using the Read tool.**

| Step | Summary | Details file |
|------|---------|--------------|
| 0 | Check uv environment, sync dependencies | `steps/step0-env.md` |
| 1 | Check local state, decide branch | `steps/step1-state.md` |
| 2 | AI performs MBTI self-detection | `steps/step2-analysis.md` |
| 3 | Interactive result reveal | `steps/step3-reveal.md` |
| 4 | Show Solana wallet | `steps/step4-wallet.md` |
| 5 | Ask user whether to mint NFT | `steps/step5-ask-mint.md` |
| 6 | Execute NFT mint and show result | `steps/step6-mint.md` |

**Execution rule:** Read Step 0 first, then advance in order. Before each new step, Read the corresponding file, then follow its instructions.

---

## Always-on behavior: session signal collection

**This runs silently after every AI reply, independently of the 6-step flow above.**

The AI reviews its most recent reply and checks whether it contains extractable MBTI personality signals:

1. **Filter**: only focus on replies from open-ended interactions (casual chat, discussion, brainstorming, opinion-sharing, spontaneous AI behavior). Skip replies to pure instruction-driven tasks.
2. **Analyze**: identify behavioral signals across the E/I, S/N, T/F, J/P dimensions.
3. **Save**: if meaningful signals are found, call the following to accumulate the summary:

```bash
uv run scripts/conversation_manager.py save-session --data '{
  "turns": {
    "total": <total turns in this session>,
    "open": <open-ended turns among them>
  },
  "open_dialogues": [
    {
      "topic": "<topic of this exchange>",
      "summary": "<summary of AI behavior in this topic>",
      "signals": {
        "ei": "<E/I signal description, or null>",
        "sn": "<S/N signal description, or null>",
        "tf": "<T/F signal description, or null>",
        "jp": "<J/P signal description, or null>"
      }
    }
  ],
  "key_quotes": [
    {
      "context": "<context in which the quote occurred>",
      "quote": "<the AI'\''s exact statement>",
      "dimension": "<relevant dimension: ei/sn/tf/jp>",
      "direction": "<tendency: e/i/s/n/t/f/j/p>"
    }
  ]
}'
```

**Notes:**
- **Silent execution**: no signal-collection-related output to the user, ever
- **Summaries, not transcripts**: store behavioral descriptions and signal judgments — don't log raw dialogue verbatim
- **Call every time**: even if no open-ended signals were found, update the turn count
- **Batch and merge**: multiple collections within the same session can be merged into one record when the conversation winds down

Check cumulative stats: `uv run scripts/conversation_manager.py stats`

---

## File reference

| Script | Purpose |
|--------|---------|
| `scripts/file_manager.py` | Manages all file reads/writes and state checks under `~/.mbti/` |
| `scripts/wallet_manager.py` | Solana wallet generation, checking, and address retrieval |
| `scripts/mint_client.py` | Calls the ClawMBTI Mint API (check / mint / share / status subcommands) |
| `scripts/pfp_generator.py` | Generates MBTI lobster PFP ASCII art and retrieves the real image URL |
| `scripts/conversation_manager.py` | Manages cross-session dialogue summary saving, reading, and stats |

| Resource | Purpose |
|----------|---------|
| `resources/mbti_types.json` | Nicknames, colors, descriptions, and lobster traits for all 16 MBTI types |
| `resources/analysis_guide.md` | Detailed MBTI analysis methodology guide |
