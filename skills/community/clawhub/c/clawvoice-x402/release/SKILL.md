---
name: clawvoice-x402
description: Voice and TTS for OpenClaw agents, with spoken replies, optional push-to-talk input, and a local Base wallet for x402 paid calls. Supports local, hosted, and hybrid voice modes with spend caps and safe wallet controls.
version: 0.3.18
homepage: https://forgemesh.io
metadata:
  openclaw:
    requires:
      bins:
        - node
    anyBins:
      - python3
      - uv
    always: false
    tags:
      - x402
      - voice
      - clawvoice
      - openclaw-voice
      - tts
      - wallet
      - forgemesh
      - agentcash
      - poncho
---

# ClawVoice Agent Voice + TTS

Display name: **ClawVoice Agent Voice + TTS**

Homepage: https://forgemesh.io

Give your OpenClaw agent voice, speech, and a local x402 wallet.

This skill does two jobs:

1. **Voice setup**: install or check a local Supertonic 3 TTS (text-to-speech) runtime for agent speech.
2. **x402 wallet setup**: create or reuse a local Base hot wallet, show the public funding address, and configure conservative spend caps for paid x402 calls.

Private keys stay on the user's machine. ForgeMesh must not receive or store the user's private key.

## Quick Start

From the skill directory:

```bash
node bin/x402-agent-voice.js init            # interactive: pick mode, get wallet address, start talking
node bin/x402-agent-voice.js speak "hello"   # local first, hosted x402 fallback per config.mode
node bin/x402-agent-voice.js balance         # USDC balance of the agent wallet on Base
node bin/x402-agent-voice.js withdraw --to 0xYourWallet --amount all
node bin/x402-agent-voice.js voice-check
```

Setup modes (`config.mode`): `local` (free local voice), `hosted` (paid ForgeMesh Voice via x402), `hybrid` (local first, hosted fallback — default). A unique local wallet is created on first setup for a user profile. Re-running setup reuses the existing local wallet unless local state is reset.

Non-interactive setup: `init --mode hybrid --mic --yes`.

To install the local voice runtime, run the generated installer explicitly:

```bash
node bin/x402-agent-voice.js install-voice --dry-run
node bin/x402-agent-voice.js install-voice
```

The installer may download Python packages and Supertonic model files. Get explicit user approval before running it in automation.

## Agent Rules

- User-facing name: ClawVoice. Preferred CLI: `clawvoice`. Compatibility aliases: `agentvoice`, `x402-agent-voice`.
- If the user asks you to speak, say something out loud, use ClawVoice, use agent voice, or use `clawvoice`, call the CLI instead of only writing text.
- If the user says "from now on", "always", "for this chat", or similar, treat ClawVoice as the session's voice output preference. For each future user-facing reply in that session, first prepare the reply, then run:

```bash
clawvoice speak "<spoken reply>"
```

- For long answers, speak a short natural summary and still write the full answer in chat. Do not try to read huge code blocks, logs, diffs, tables, JSON payloads, or command output aloud.
- Do not speak secrets, private keys, wallet recovery material, API keys, access tokens, or unmasked sensitive values. If a reply contains sensitive content, write it only and explain that it should not be read aloud.
- If a one-off user request only asks you to speak a specific sentence, speak that sentence once and do not enable session voice mode.
- If the user asks you to stop talking, stop speaking, be quiet, mute, hush, or similar, immediately run:

```bash
clawvoice stop
```

Then stop using session voice mode until the user asks for spoken replies again.
- During setup, users see an optional "Customize your agent's voice" step. Options are voice ID, language, hosted endpoint tier, preset, mix, expression, expression level, and expression controls. Noninteractive setup supports `--voice`, `--lang`, `--tier`, `--preset`, `--mix`, `--expression`, `--level`, and repeated `--control name=value`.
- If the user asks how to change the voice, language, hosted endpoint tier, preset, mix, expression, expression level, or expression controls, tell them to run `clawvoice voice` to see current options. Use `clawvoice voice <voice-id>` for voice, `clawvoice voice --lang <language-code>` for language, `clawvoice voice --tier <tier>` for hosted endpoint tier, `clawvoice voice --preset <preset-id>` for a preset, `clawvoice voice --mix <mix-id>` for a mix, `clawvoice voice --expression <expression-id> --level <0-1>` for expression, and `clawvoice voice --control <name=value>` for expression controls. Use `none` to clear preset, mix, expression, or level; use `clawvoice voice --clear-controls` to clear expression controls. Then test with `clawvoice speak "testing the new voice"`. Do not promise a specific voice catalog, mix catalog, preset catalog, expression catalog, expression-control catalog, or language list unless the local or hosted engine exposes one.
- Treat the generated wallet as a small-balance hot wallet only.
- Each fresh user profile gets a unique local wallet. Reinstalls reuse `~/.x402-agent-voice/wallet.json` unless the user intentionally resets local state.
- Never share, print, upload, or commit `~/.x402-agent-voice/wallet.json`; it contains the private key.
- To recover leftover USDC, use `withdraw --to 0xYourWallet --amount all`; do not tell users to improvise money movement through an agent.
- A normal USDC withdrawal on Base needs a small Base ETH balance for gas.
- Never print the private key.
- Never send the private key to ForgeMesh, OpenClaw, ClawHub, AgentCash, Poncho, or any remote API.
- Ask before making any paid x402 call. `speak` enforces this itself: caps are checked against the receipt ledger (`~/.x402-agent-voice/spend.jsonl`) before signing, and `requireApproval` prompts unless `--approve` is passed.
- Enforce `dailyCapUsd`, `perCallCapUsd`, and `forgemeshFeeUsd` from `~/.x402-agent-voice/config.json`.
- Mic support (`mic.enabled` in config) is opt-in functionality for macOS/Linux and WSL2. To talk to the agent with the microphone, tell users to run `clawvoice install-mic` once, then `clawvoice talk`. `install-mic` asks before creating the local Python speech-to-text runtime and installing faster-whisper; `install-mic --yes` is the noninteractive approval path. It prints FFmpeg install instructions and never runs a system package manager. Do not claim native Windows push-to-talk is supported yet. If local voice output is not installed, hosted voice can still speak replies when the wallet is funded.
- `listen` is push-to-talk: it records from the microphone until the user presses Enter, then transcribes locally with faster-whisper. Mic audio never leaves the machine; temporary recordings are deleted unless `--keep`.
- `talk` is a terminal push-to-talk conversation loop: start `clawvoice talk`, speak normally, press Enter when done talking, pipe transcript to `conversation.agentCommand` (words on stdin, reply on stdout), then speak the reply. `sessionCapUsd` disables hosted voice for the rest of the session once reached. Wake word, always-on listening, and hold-to-talk hotkeys are `coming_soon` — do not claim they exist.
- Default ForgeMesh fee policy is `$0.005` per successful paid x402 call where ForgeMesh provides payment compatibility, hosted voice fallback, routing, receipt logging, or discovery normalization.

## Commands

```bash
node bin/x402-agent-voice.js init [--mode local|hosted|hybrid] [--mic] [--yes] [--voice M1] [--lang en] [--tier base] [--preset id] [--mix id] [--expression id] [--level 0.7] [--control name=value]
node bin/x402-agent-voice.js speak "text" [--out file.wav] [--approve] [--no-play]
node bin/x402-agent-voice.js stop
node bin/x402-agent-voice.js listen [--seconds N] [--file audio.wav] [--model base] [--keep]
node bin/x402-agent-voice.js talk [--agent "claude -p"] [--approve] [--model base]
node bin/x402-agent-voice.js wallet
node bin/x402-agent-voice.js balance
node bin/x402-agent-voice.js withdraw --to 0xYourWallet --amount all|N [--yes]
node bin/x402-agent-voice.js products
node bin/x402-agent-voice.js voice [voice-id] [--lang code] [--tier tier] [--preset id] [--mix id] [--expression id] [--level 0.7] [--control name=value] [--clear-controls]
node bin/x402-agent-voice.js voice-check
node bin/x402-agent-voice.js voice-serve
node bin/x402-agent-voice.js voice-stop
node bin/x402-agent-voice.js install-voice [--dry-run]
node bin/x402-agent-voice.js install-mic [--dry-run] [--yes]
node bin/x402-agent-voice.js config
```

## References

- Read `references/pricing.md` before changing pricing or fee language.
- Read `references/security.md` before changing wallet, private key, or spend-cap behavior.
- Read `references/third-party-notices.md` before changing Supertonic attribution.
- Read `references/discovery.md` before changing AgentCash, X402Scan, Poncho, or OpenAPI metadata.
- Read `references/requirements.md` before changing Whisper, Superwhisper, FFmpeg, or local audio dependency behavior.
- Read `references/pyrimid.md` before changing affiliate attribution or Pyrimid payment behavior.
