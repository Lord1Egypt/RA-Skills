---
name: audioclaw-skills-voice-reply
description: Use when AudioClaw Skills, Feishu, or Lark needs to send AudioClaw voice replies with runtime-switchable voice_id, emotion preset, or speaking style, including per-message speaker overrides, voice-family emotion routing, cache reuse, and safe fallback when a requested voice is unavailable.
---

# AudioClaw Skills Voice Reply

## When to use

Use this skill when AudioClaw already has the final reply text and now needs a voice version that can change on demand.

Common triggers:
- A chat bot should answer in different tones such as `calm`, `warm`, `cheerful`, `serious`, or `promo`.
- The caller wants to switch `voice_id` or `voice_family` in a single request without editing code.
- The same AudioClaw workflow should support both free voices and paid or custom voices.
- The runtime should keep working even when a requested voice is not available to the current key.
- A user has already said "以后一直给我发语音", and AudioClaw should remember that preference for future turns.
- AudioClaw needs a workspace-local file plus a stable way to deliver it as a Feishu audio message.
- The caller already has a cloned AudioClaw `voice_id` such as `vc-...` and wants the runtime to use it directly without falling back first.

Do not use this skill for ASR intake or long-form digest generation.

## Workflow

1. Start from the final user-facing text. Do not pass hidden reasoning or raw markdown tables.
2. Build an AudioClaw voice request with:
   - `text`
   - optional `scene`
   - optional `voice_id`
   - optional `voice_family`
   - optional `emotion`
   - optional `speed`, `pitch`, `volume`
3. Run `scripts/openclaw_voice_switchboard.py`.
   - For AudioClaw on Feishu or Lark, prefer `scripts/picoclaw_voice_reply.py`.
4. Let the script resolve the request in this order:
   - exact `voice_id`
   - `voice_family` plus matching emotion variant
   - scene plus emotion preset
   - validated fallback voice
   - Important: if the exact `voice_id` is a clone-style id such as `vc-...`, this skill now tries that id directly first, even if it is not part of the built-in official voice catalog.
5. If `preference_key` is present, the script can remember:
   - `reply_mode`
   - default `voice_id`
   - default `emotion`
   - default `scene`
6. If the result should be sent through AudioClaw media upload, pass:
   - `--out` inside the AudioClaw workspace
   - `--openclaw-workspace-root` pointing at the workspace root
   - `--delivery-profile feishu_voice` when the downstream channel prefers `.ogg/.opus`
   - optional `--chmod 644` if you want to be explicit, though this skill now defaults to `0644`
   - if `--openclaw-workspace-root` is set and `--out` is omitted, this skill now writes to `workspace/state/audio/` automatically
7. Use the returned JSON manifest in AudioClaw to:
   - prefer `scripts/picoclaw_voice_reply.py` for AudioClaw on Feishu
   - let the wrapper send the Feishu audio message directly
   - do not send the local path or the `MEDIA:...` line through the `message` tool
   - only use `send_file` when you intentionally opt out of direct Feishu sending
   - log `trace_id`
   - persist the resolved voice choice for the next turn if desired
8. If the requested voice is not available to the current key, let the fallback stand unless the user explicitly requires strict failure.
9. If you want AudioClaw to remember a clone voice, either:
   - set it as the user's default voice with `--set-default-voice-id vc-...`
   - or register it explicitly with `--register-clone-voice-id vc-...`

## Voice discovery

When AudioClaw needs to find a usable voice or confirm a `voice_id`, use this order:

1. Check the local catalog first:
   - run `python3 scripts/openclaw_voice_switchboard.py --list-voices`
   - use this for fast lookup of built-in voices, known emotion variants, and clone voices already registered locally
2. If the user asks for the official public voice list, package availability, or a voice not found locally, check the official voice page:
   - `https://senseaudio.cn/docs/voice_api`
   - page title: `API 音色服务说明`
3. Prefer the official page when AudioClaw needs to confirm:
   - whether a `voice_id` is a free, VIP, or SVIP voice
   - whether a named speaker has multiple emotion variants
   - whether the request likely needs selected-voice purchase or custom voice authorization
4. After finding a likely `voice_id`, still let the runtime validate access at synthesis time, because account permissions can differ by key.

Practical rule:
- Local `--list-voices` is the first-stop runtime catalog.
- `https://senseaudio.cn/docs/voice_api` is the canonical fallback reference for official voice names, `voice_id`, and package tier notes.

## AudioClaw rule

When this skill is used inside AudioClaw for Feishu or Lark voice replies:

1. Run `scripts/picoclaw_voice_reply.py`.
2. Let the wrapper upload the generated `.ogg/.opus` file to Feishu and send it as `msg_type=audio`.
3. Do not call the `send_file` tool for that audio unless you explicitly passed `--skip-direct-send`.
4. Do not call the `message` tool with the local path or the `MEDIA:...` reference. AudioClaw will send them as plain text.
5. After the audio is sent, prefer no extra text confirmation.
6. If the host runtime still requires one final assistant message to finish the turn, send one short natural Chinese line such as `我已经用语音回复你了。` instead of leaving the turn empty.
7. Use `media_reference` only as debug metadata or future AudioClaw compatibility data.

This rule matters because this AudioClaw environment does not render `MEDIA:...` as media, and the generic `send_file` tool sends Feishu voice notes as plain files instead of `audio` messages. The reliable path here is direct Feishu upload plus `msg_type=audio`.

## Runtime model

The official public TTS API exposes:
- `voice_setting.voice_id`
- `voice_setting.speed`
- `voice_setting.vol`
- `voice_setting.pitch`
- `audio_setting.format`
- `audio_setting.sample_rate`
- one HTTP endpoint with two modes:
  - non-stream with `stream=false`
  - SSE with `stream=true`

Important constraint:
- The public TTS API docs do not expose a standalone `emotion` request field.
- Emotion switching is therefore handled by choosing a matching `voice_id` when one exists, or by keeping the voice and shaping `speed / pitch / vol`.
- This skill requests final-file TTS in non-stream mode by default, because AudioClaw only needs the completed file and this avoids stream assembly edge cases.
- For this server-side HTTP TTS path, the official docs still use `Authorization: Bearer API_KEY`. The generated `Public Key` is not required by this skill.
- If the requested `voice_id` looks like a clone id such as `vc-...`, this skill now auto-routes TTS to `SenseAudio-TTS-1.5` and records `audio.model_used` in the manifest.

## API key lookup

This skill now treats `SENSEAUDIO_API_KEY` as the default API key source again.

Runtime rules:
- If the host app injects `SENSEAUDIO_API_KEY` as an AudioClaw login token such as `v2.public...`, the shared bootstrap will replace it with the real `sk-...` value from `~/.audioclaw/workspace/state/senseaudio_credentials.json` before TTS starts.
- `--api-key-env` still works, but the default runtime path is `SENSEAUDIO_API_KEY`.

If you need the exact same speaker timbre across many emotions, use a purchased multi-variant voice family or an authorized custom voice. Otherwise this skill will approximate the requested emotion with the best available voice and tuning.

## Request contract

Minimal JSON request:

```json
{
  "text": "我们已经收到你的需求，今天下午会把结果发给你。",
  "scene": "assistant",
  "emotion": "calm"
}
```

Full request:

```json
{
  "text": "新品今晚八点开售，现在下单还有首发赠品。",
  "scene": "sales",
  "voice_id": "male_0027_b",
  "voice_family": "male_0027",
  "emotion": "promo",
  "speed": 1.08,
  "pitch": 1,
  "volume": 1.05,
  "audio_format": "mp3",
  "sample_rate": 32000,
  "preference_key": "feishu:ou_xxx",
  "reply_mode": "voice",
  "allow_fallback": true,
  "strict_voice": false,
  "cache_dir": "/tmp/openclaw-voice-cache"
}
```

Clone voice example:

```json
{
  "text": "这是你的克隆音色回复测试。",
  "voice_id": "vc-yxdCFUKyNLPexxJ66jaXWk",
  "emotion": "calm",
  "allow_fallback": false,
  "strict_voice": true
}
```

Supported emotion presets:
- `neutral`
- `calm`
- `warm`
- `cheerful`
- `serious`
- `promo`
- `sad`
- `angry`
- `analytical`

Supported scene hints:
- `assistant`
- `customer_support`
- `briefing`
- `sales`
- `marketing`
- `narration`
- `education`
- `gaming`
- `warning`

## AudioClaw integration pattern

Recommended handoff:

1. AudioClaw generates final reply text.
2. AudioClaw decides whether this turn should speak and what mood it wants.
3. AudioClaw calls `scripts/openclaw_voice_switchboard.py` with a request JSON.
4. The script returns a manifest with:
   - requested voice
   - resolved voice
   - emotion strategy
   - effective `speed / pitch / volume`
   - delivery profile and file mode
   - local audio path
   - AudioClaw-friendly media reference when the output is under a workspace root
   - `trace_id`
5. AudioClaw uploads the resulting file to Feishu or any downstream channel, or lets the AudioClaw wrapper do that directly for Feishu.

Operational rules:
- Cache by resolved voice plus text plus audio settings.
- If a paid voice is unavailable, allow fallback unless the request is marked strict.
- Always log the resolved voice and `trace_id`.
- Force generated audio files to mode `0644` so the AudioClaw sender can read them reliably.
- When `--openclaw-workspace-root` is set and `--out` stays inside that root, expose `delivery.openclaw_media_reference`.
- When `--delivery-profile feishu_voice` is enabled, synthesize with AudioClaw first and then transcode to `ogg/opus` with system `ffmpeg` or `imageio-ffmpeg`.
- This publishable skill intentionally does not bundle `ffmpeg`. Install `ffmpeg` or run `python3 -m pip install imageio-ffmpeg` on the target machine.
- Avoid ad-hoc temp filenames under the workspace root. Prefer `workspace/state/audio/`, which this skill will now use automatically when `--openclaw-workspace-root` is given without `--out`.
- For AudioClaw on Feishu, `scripts/picoclaw_voice_reply.py` now uses the local Feishu app credentials from `~/.audioclaw/config.json`, uploads the audio through the official `/open-apis/im/v1/files` endpoint, and sends it as `msg_type=audio`.
- The wrapper infers the active Feishu `chat_id` from the latest `agent_main_feishu_direct_*.jsonl` session log unless you pass `--chat-id` explicitly.

## Commands

List voices:

```bash
python3 scripts/openclaw_voice_switchboard.py --list-voices
```

Check the official voice catalog page:

```text
https://senseaudio.cn/docs/voice_api
```

List emotion presets:

```bash
python3 scripts/openclaw_voice_switchboard.py --list-emotions
```

Enable permanent voice reply for one user:

```bash
python3 scripts/openclaw_voice_switchboard.py \
  --preference-key "feishu:ou_xxx" \
  --set-reply-mode voice \
  --set-default-voice-id male_0004_a \
  --set-default-emotion calm \
  --set-default-scene assistant
```

Enable permanent cloned-voice reply for one user:

```bash
python3 scripts/openclaw_voice_switchboard.py \
  --preference-key "feishu:ou_xxx" \
  --set-reply-mode voice \
  --set-default-voice-id vc-yxdCFUKyNLPexxJ66jaXWk \
  --set-default-emotion calm \
  --set-default-scene assistant
```

Register a prepared clone voice so the runtime can list and reuse it:

```bash
python3 scripts/openclaw_voice_switchboard.py \
  --register-clone-voice-id vc-yxdCFUKyNLPexxJ66jaXWk \
  --register-clone-name "我的克隆音色"
```

Show registered clone voices:

```bash
python3 scripts/openclaw_voice_switchboard.py --show-clone-voices
```

Show current voice preference:

```bash
python3 scripts/openclaw_voice_switchboard.py \
  --preference-key "feishu:ou_xxx" \
  --show-preference
```

Generate one AudioClaw turn from a JSON request:

```bash
python3 scripts/openclaw_voice_switchboard.py \
  --request-file /path/to/request.json \
  --out /tmp/openclaw_reply.mp3
```

Direct CLI example:

```bash
python3 scripts/openclaw_voice_switchboard.py \
  --text "我们已经处理好了，稍后把结果发给你。" \
  --scene assistant \
  --emotion warm \
  --preference-key "feishu:ou_xxx" \
  --delivery-profile feishu_voice \
  --openclaw-workspace-root ~/.audioclaw/workspace \
  --out ~/.audioclaw/workspace/audioclaw_warm.ogg
```

AudioClaw Feishu one-step example:

```bash
python3 scripts/picoclaw_voice_reply.py \
  --text "这是一次可以直接发给飞书的语音回复。" \
  --scene assistant \
  --emotion calm \
  --workspace-root ~/.audioclaw/workspace
```

Only generate, do not send:

```bash
python3 scripts/picoclaw_voice_reply.py \
  --text "这是一次只生成不直发的测试语音。" \
  --scene assistant \
  --emotion calm \
  --workspace-root ~/.audioclaw/workspace \
  --skip-direct-send
```

## Resources

- `scripts/senseaudio_tts_client.py`
  - Small importable client for `https://api.senseaudio.cn/v1/t2a_v2`
  - Handles SSE chunks and writes audio bytes
- `references/openclaw_voice_switchboard.md`
  - TTS capability summary plus the official voice catalog reference at `https://senseaudio.cn/docs/voice_api`
- `scripts/openclaw_voice_switchboard.py`
  - Main runtime for AudioClaw
  - Resolves voice, emotion, fallback, caching, and output manifest
- `scripts/picoclaw_voice_reply.py`
  - AudioClaw-first wrapper
  - Generates audio and, by default, sends it to Feishu as a real `audio` message
- `scripts/feishu_audio_sender.py`
  - Direct Feishu sender for `.ogg/.opus`
  - Uses `~/.audioclaw/config.json` app credentials by default, infers the active chat, uploads the file, and sends `msg_type=audio`
- `references/openclaw_voice_switchboard.md`
  - Official docs summary, request examples, and AudioClaw capability boundaries
