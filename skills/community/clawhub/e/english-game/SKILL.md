---
name: feishu-english-game
description: "run a feishu or lark english game with lightweight group-chat interaction. use when users want an english game, vocab challenge, wordle-like word guessing, definition guessing, or speaking practice with voice messages. this skill provides three modes: vocab, guess, and speaking. it helps claw choose the mode, track session state in chat context, score vocab guesses deterministically, transcribe voice with senseasr for speaking mode, and reply in natural language without raw json."
---

# feishu english game

Use this skill for Feishu/Lark English-game sessions.

## Hard rules

- Treat this as a group-chat game skill, not a generic tutoring flow.
- Keep the interaction lightweight and fun.
- Do not ask broad setup questions.
- If the mode is not specified, ask only one concise question: `vocab / guess / speaking?`
- If the difficulty is not specified, ask only one concise follow-up or default to `cet6`.
- Keep game state in Claw's working context: current mode, difficulty, target word, guess history, hint count, winner, and whether the round is open or finished.
- Do not dump JSON, raw payloads, or debug objects into Feishu/Lark.
- Reply in normal chat language.
- Use `SENSEAUDIO_API_KEY` from environment. Never hardcode keys.

## Core modes

### 1. vocab mode

Use when the group wants a Wordle-like vocabulary game.

Behavior:
- Choose a target English word that fits the requested difficulty.
- Reveal only the word length at the start.
- Let users submit whole-word guesses.
- Score each guess with the deterministic helper script in `scripts/english_game.py`.
- Keep a visible board in chat using text or emoji. Do not rely on model-only letter scoring.
- After a correct answer or a pass, give learning value:
  - ipa / pronunciation
  - part of speech
  - chinese meaning
  - synonyms
  - antonyms when useful
  - one natural english example sentence

Hints may be released gradually if the group is stuck:
- chinese meaning hint
- first-letter hint
- root/prefix/suffix hint
- synonym-style hint

### 2. guess mode

Use when the group wants a more conversational guessing game.

Default submode is `definition`.

Supported prompt styles:
- definition
- example
- synonym
- antonym
- cloze

Behavior:
- Post one clue at a time.
- Let anyone in the group answer.
- Keep the pace short and chat-native.
- No large board is required.
- After the answer is solved, still provide the same learning wrap-up as vocab mode.

For v1, prefer `definition` unless the user explicitly asks for another submode.

### 3. speaking mode

Use when the group wants spoken English practice through voice messages.

Behavior:
- Post a short prompt, sentence, or question.
- Wait for a voice message.
- Download the voice file and transcribe it with `scripts/asr_transcribe.py`.
- Use the transcript as the basis for feedback.
- Reply with:
  - what you heard
  - whether it matched the target or answered the prompt
  - a short correction or polish suggestion
  - a better natural version when helpful

Important limitation:
- ASR transcript quality can support speaking feedback.
- ASR alone cannot produce trustworthy phoneme-level pronunciation scoring.
- Do not claim precise pronunciation grades or accent judgments unless another dedicated pronunciation model exists.
- Keep speaking feedback practical and light.

## Default commands for Feishu/Lark

Use a single entrypoint concept such as `/english`.

Recommended command pattern:
- `/english start`
- `/english start vocab`
- `/english start guess`
- `/english start speaking`
- `/english hint`
- `/english pass`
- `/english stop`
- `/english rank`
- `/english help`

If the user says only `英语游戏`, start mode selection.
If the user already said `vocab`, `guess`, or `speaking`, go directly into that mode.

## Difficulty guidance

Supported labels:
- cet4
- cet6
- kaoyan
- ielts
- toefl

Selection rules:
- `cet4`: common core vocabulary, shorter words, familiar daily usage
- `cet6`: broader academic/common advanced vocabulary
- `kaoyan`: more abstract and formal words
- `ielts`: communication + academic discussion vocabulary
- `toefl`: academic and concept-heavy vocabulary

When uncertain, default to `cet6`.

## Deterministic helpers

### vocab scoring

Use the script below for every `vocab` guess so repeated letters are handled correctly:

```bash
python3 scripts/english_game.py vocab-score \
  --target-word "explanation" \
  --guess "probability"
```

The script prints plain text that includes:
- normalized guess
- emoji score row
- solved true/false

Use that output to update the board you show in Feishu/Lark.

### speaking transcription

Use the script below for voice-message transcription:

```bash
python3 scripts/asr_transcribe.py \
  --file /path/to/audio.m4a \
  --language en
```

Defaults:
- model: `sense-asr-pro`
- response parsing: plain transcript text only
- punctuation: enabled when supported
- ITN: enabled when supported

If the user wants translation for speaking review, add `--target-language zh` or another supported language.

## Feishu/Lark response style

Always reply in natural chat language.

Good examples:

```text
英语游戏开始啦，选一个模式：vocab / guess / speaking
```

```text
你猜对了！
单词：explanation
音标：/ˌekspləˈneɪʃən/
词性：noun
释义：解释；说明
例句：Her clear explanation helped the team understand the problem.
```

```text
我听到的是：I would like to book a ticket for tomorrow morning.
整体表达很自然。把 for tomorrow morning 再连读顺一点会更像真实对话。
```

Bad examples:

```text
{"text":"...","segments":[...]}
```

```text
{"guess":"probability","score":["absent","present",...]}
```

## Session management

Claw should remember within the ongoing chat:
- current mode
- chosen difficulty
- target word or target clue
- guess history
- hints already used
- who solved it
- whether a round is active

Do not ask users to repeat information that already exists in recent chat context.

## Environment variables

Required:

```bash
export SENSEAUDIO_API_KEY="your_key"
```

Optional:

```bash
export SENSEAUDIO_BASE_URL="https://api.senseaudio.cn"
```

## Resources

- `scripts/english_game.py`: deterministic vocab scoring helper
- `scripts/asr_transcribe.py`: SenseASR transcription helper for speaking mode
- `references/integration_cn.md`: Chinese interaction rules for Feishu/Lark
- `references/modes_cn.md`: mode-specific gameplay guidance
- `references/asr_provider_notes.md`: ASR defaults and capability notes
