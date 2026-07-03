# ClawVoice Agent Voice + TTS

AI voice and x402 wallet capabilities for OpenClaw agents.

ClawVoice by ForgeMesh Labs gives OpenClaw agents voice output, optional push-to-talk voice input, and a local Base USDC x402 wallet for paid agent calls.

Package name: `@forgemeshlabs/x402-agent-voice`

Commands: `clawvoice`, `agentvoice`, or `x402-agent-voice`

Homepage: https://forgemesh.io

Feedback: clawdbotworker@gmail.com

## What It Does

- Text-to-speech for OpenClaw agents.
- Local, hosted, or hybrid voice modes.
- Optional push-to-talk speech-to-text on supported platforms.
- x402 payments for hosted ForgeMesh Voice fallback.
- Local Base USDC x402 wallet for paid agent calls.
- Spend caps, balance checks, and withdrawal for leftover USDC.
- Plug-and-play OpenClaw / ClawHub skill packaging.

Search terms: ClawVoice, OpenClaw Voice, OpenClaw Agent Voice, AI Voice, Agent Voice, x402 Voice, Wallet Voice, Voice Skill, OpenClaw Skill.

## Install

From the release tarball:

```bash
npm install -g ./forgemeshlabs-x402-agent-voice-0.3.18.tgz
```

Then run setup:

```bash
clawvoice init --mode hybrid --mic
```

Use hosted mode if you do not want local voice setup:

```bash
clawvoice init --mode hosted
```

Short aliases also work:

```bash
agentvoice init --mode hybrid --mic
```

The old command still works:

```bash
x402-agent-voice init --mode hybrid --mic
```

## Register With OpenClaw

Global npm installs are not automatically scanned by OpenClaw. To make ClawVoice appear in the OpenClaw Skills sidebar, link the installed package into your OpenClaw skills folder:

```bash
mkdir -p ~/.openclaw/skills
ln -s "$(npm root -g)/@forgemeshlabs/x402-agent-voice" ~/.openclaw/skills/clawvoice-x402
openclaw gateway restart
```

Use the restart command your OpenClaw install supports if it differs. The symlink keeps future `npm update -g @forgemeshlabs/x402-agent-voice` updates connected to the same skill registration.

## Make Your Agent Speak Replies

ClawVoice is a speech tool, not an automatic replacement for OpenClaw's chat renderer. Your agent speaks when it calls the CLI.

For one reply:

```text
Use ClawVoice to say "hello, my agent voice is working"
```

For the rest of a chat session:

```text
Use ClawVoice to speak your responses out loud from now on.
```

After that instruction, the agent should call `clawvoice speak "<reply>"` for normal user-facing replies. Long answers should be summarized aloud and written fully in chat.

To stop current playback:

```text
Stop talking.
```

The agent should run:

```bash
clawvoice stop
```

That stops the current ClawVoice audio and disables session voice mode until you ask for spoken replies again.

## What Setup Does

Setup asks how your agent should speak:

| Mode | Meaning |
|---|---|
| `local` | Free local voice after setup. The voice runtime runs on your machine. |
| `hosted` | No local voice install. Your agent pays ForgeMesh Voice per call through x402. |
| `hybrid` | Local first, hosted fallback. This is the recommended mode. |

Setup creates a unique local Base USDC wallet the first time it runs for a user profile. If `~/.x402-agent-voice/wallet.json` already exists, setup reuses that wallet instead of replacing it.

Each machine, container, or user profile gets its own wallet unless you deliberately copy the local wallet file. Do not share `wallet.json`, check it into git, paste it into chat, or upload it to support.

## Quick Commands

```bash
clawvoice voice-check
clawvoice stop
clawvoice wallet
clawvoice balance
clawvoice withdraw --to 0xYourWallet --amount all
clawvoice products
clawvoice voice
clawvoice speak "hello world"
```

`wallet` shows the public address, chain, token, and spend policy. It does not show the private key.

## Customize Your Agent's Voice

Setup includes an optional **Customize your agent's voice** step. It lets you choose:

- Voice ID
- Language
- Hosted endpoint tier
- Preset
- Mix
- Expression
- Expression level
- Expression controls

You can also set those options during noninteractive setup:

```bash
clawvoice init --mode hybrid --mic --voice M1 --lang en --tier base --preset calm --mix narrator --expression cheerful --level 0.7 --control speed=1.1
```

Check the current voice options:

```bash
clawvoice voice
```

Set a voice ID:

```bash
clawvoice voice M1
```

Set a language code:

```bash
clawvoice voice --lang es
```

Set a hosted endpoint tier:

```bash
clawvoice voice --tier pro
```

Set a preset or mix:

```bash
clawvoice voice --preset calm
clawvoice voice --mix narrator
```

Set expression and intensity:

```bash
clawvoice voice --expression cheerful --level 0.7
```

Set expression controls:

```bash
clawvoice voice --control speed=1.1 --control pitch=0.2
```

Set everything at once:

```bash
clawvoice voice --voice F1 --lang fr --tier base --preset calm --mix narrator --expression cheerful --level 0.7 --control speed=1.1
```

Clear a preset, mix, expression, or level:

```bash
clawvoice voice --preset none
clawvoice voice --mix none
clawvoice voice --expression none
clawvoice voice --level none
clawvoice voice --clear-controls
```

List the built-in language guide:

```bash
clawvoice voice --languages
```

Then test it:

```bash
clawvoice speak "testing the new voice"
```

Voice IDs, language codes, endpoint tiers, presets, mixes, expressions, expression levels, and expression controls depend on the active local engine or hosted voice service. Defaults are `M1`, `en`, `base`, no preset, no mix, no expression, no level, and no expression controls.

### Global Language Guide

Use `clawvoice voice --lang <code>` to set the language. The hosted service may support additional aliases; these are the built-in global-friendly codes and display names.

| Code | Language | Localized display name |
|---|---|---|
| `en` | English | ClawVoice Agent Voice |
| `es` | Español | ClawVoice Voz de agente |
| `fr` | Français | ClawVoice Voix d'agent |
| `de` | Deutsch | ClawVoice Agentenstimme |
| `it` | Italiano | ClawVoice Voce agente |
| `pt` | Português | ClawVoice Voz de agente |
| `nl` | Nederlands | ClawVoice Agentstem |
| `pl` | Polski | ClawVoice Głos agenta |
| `cs` | Čeština | ClawVoice Hlas agenta |
| `hu` | Magyar | ClawVoice Ügynökhang |
| `ro` | Română | ClawVoice Vocea agentului |
| `el` | Ελληνικά | ClawVoice Φωνή πράκτορα |
| `sv` | Svenska | ClawVoice Agentröst |
| `da` | Dansk | ClawVoice Agentstemme |
| `fi` | Suomi | ClawVoice Agenttiääni |
| `no` | Norsk | ClawVoice Agentstemme |
| `ru` | Русский | ClawVoice Голос агента |
| `uk` | Українська | ClawVoice Голос агента |
| `tr` | Türkçe | ClawVoice Ajan sesi |
| `ar` | العربية | ClawVoice صوت الوكيل |
| `he` | עברית | ClawVoice קול סוכן |
| `hi` | हिन्दी | ClawVoice एजेंट आवाज़ |
| `bn` | বাংলা | ClawVoice এজেন্ট ভয়েস |
| `id` | Bahasa Indonesia | ClawVoice Suara agen |
| `ms` | Bahasa Melayu | ClawVoice Suara ejen |
| `fil` | Filipino | ClawVoice Boses ng ahente |
| `vi` | Tiếng Việt | ClawVoice Giọng nói tác nhân |
| `th` | ไทย | ClawVoice เสียงเอเจนต์ |
| `ja` | 日本語 | ClawVoice エージェント音声 |
| `ko` | 한국어 | ClawVoice 에이전트 음성 |
| `zh` | 中文 | ClawVoice 智能代理语音 |

## Recover Leftover Funds

The agent wallet is meant to hold a small working balance. If there is leftover USDC, send it back to your main wallet:

```bash
clawvoice withdraw --to 0xYourWallet --amount all
```

You can also withdraw a specific USDC amount:

```bash
clawvoice withdraw --to 0xYourWallet --amount 1.25
```

Withdrawals send Base USDC from the local agent hot wallet. The command prints a summary first and asks for confirmation before broadcasting. Use `--yes` only for automation you trust.

Important: USDC transfers on Base require a small amount of Base ETH for gas. x402 payments usually do not require you to think about ETH, but a normal wallet-to-wallet USDC transfer does.

## Voice Input

Push-to-talk voice input is optional functionality.

```bash
clawvoice install-mic
clawvoice talk
```

To talk to your agent with the microphone, run `clawvoice install-mic` once, then start a conversation with `clawvoice talk`. If local voice output is not installed, ClawVoice can still speak through hosted voice when the wallet is funded.

You can also transcribe one recording without starting a conversation:

```bash
clawvoice listen
```

There is no hold-to-talk hotkey yet. In the terminal flow, start `clawvoice talk`, speak normally, then press Enter when you are done talking. ClawVoice transcribes what you said, sends it to the agent, and speaks the reply.

`listen` records from the microphone until you press Enter, then transcribes locally with faster-whisper.

`talk` runs a conversation loop:

```text
record your voice -> transcribe locally -> send words to your agent -> speak the reply
```

Wake word and always-on listening are not shipped yet.

## Platform Support

| Capability | macOS | Linux | Windows |
|---|---|---|---|
| Wallet creation | Supported | Supported | Supported |
| Hosted x402 voice | Supported | Supported | Supported |
| Local text-to-speech | Supported | Supported | Use WSL2 |
| Playback | Supported | Supported | Partial / WSL2 recommended |
| Push-to-talk voice input | Supported with FFmpeg + faster-whisper | Supported with FFmpeg + faster-whisper | WSL2 recommended |
| Wake word / always-on listening | Not shipped | Not shipped | Not shipped |

Windows users can use wallet and hosted voice flows. Native Windows microphone recording, local voice install, and playback still need a compatibility pass. Use WSL2 for the full local path.

## Spend Safety

Hosted voice and other paid x402 calls are guarded before any payment is signed.

Default policy:

| Setting | Default |
|---|---:|
| Per-call cap | `$0.05` |
| Daily cap | `$0.25` |
| Session voice cap | `$0.10` |
| Approval before paid calls | On |

Spend records are stored locally at:

```text
~/.x402-agent-voice/spend.jsonl
```

Configuration is stored locally at:

```text
~/.x402-agent-voice/config.json
```

## Local Voice

For local or hybrid mode:

```bash
clawvoice install-voice
```

To see what it would do first:

```bash
clawvoice install-voice --dry-run
```

Local voice may download Python packages and model files. It needs Python 3.9-3.12 (onnxruntime has no wheels for 3.13+); the installer probes `python3.12`, `python3.11`, `python3.10`, `python3.9`, then `python3`, or you can point `X402_VOICE_PYTHON` at a specific interpreter. Hosted mode avoids that setup and uses x402 payments instead.

## Built-In ForgeMesh Products

The package includes a starter list of ForgeMesh x402 products:

```bash
clawvoice products
```

AgentCash and X402Scan discovery can still be used for broader x402 discovery.

## Security Notes

- Treat the generated wallet as a small-balance hot wallet.
- Each fresh user profile gets a unique local wallet. Reinstalls reuse the existing local wallet unless you reset local state.
- Do not fund it with more than you are comfortable letting an agent spend.
- Do not share `~/.x402-agent-voice/wallet.json`; it contains the private key.
- Use `clawvoice withdraw --to 0xYourWallet --amount all` to recover leftover USDC.
- The private key stays on your machine.
- The private key is not printed by setup, `wallet`, `voice-check`, or normal commands.
- Paid calls require approval unless you explicitly pass `--approve`.

## Feedback

Please send feedback, bugs, and confusing setup steps to:

```text
clawdbotworker@gmail.com
```

Helpful details:

- OS and Node version.
- Setup mode: local, hosted, or hybrid.
- Whether `voice-check` reports local server, FFmpeg, and Whisper as ready.
- Whether `speak`, `listen`, and `talk` worked.
- Any payment approval prompt that felt unclear.
