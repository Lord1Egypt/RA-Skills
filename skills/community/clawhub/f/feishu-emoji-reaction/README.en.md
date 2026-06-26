# Feishu Reaction Skill

> *"Amaze! Amaze! Amaze!"* — Rocky, upon learning a new word
>
> *"Good good good!"* — Rocky, when things work out
>
> *"Bad bad bad!"* — Rocky, when they don't

Teach your AI Agent to speak in emoji. Not just sending reactions — reading emotions, knowing when to respond and when to stay silent, and learning new emoji on its own.

---

## The Problem

User reacts to your message with 😮‍💨. You: silence.
User sends 🤔. You: pretend you didn't see it.
User drops a 🎉. You: stone cold.

User verdict: **"Harder to talk to than my crush."**

With this skill, your agent can:
- **Express with emoji** — 🤔 when thinking, 🫡 when acknowledged, SPEECHLESS when... speechless
- **Read and respond to user reactions** — comfort on sighs, clarify on confusion, shut up on thumbs-up
- **Self-learn new emoji** — sees an unknown reaction, tries it, remembers it
- **Understand cultural context** — SMILE ≠ smile (it means 呵呵, passive-aggressive in Chinese)

---

## Quick Start

### Install

```bash
# ClawHub (recommended)
clawhub install feishu-reaction

# Manual
# Place in ~/.agents/skills/feishu-reaction/
```

### Basic Usage

```javascript
// React and stay silent
message({ action: "react", channel: "feishu", emoji: "THUMBSUP" })
NO_REPLY

// Comfort the user
message({ action: "react", channel: "feishu", emoji: "COMFORT" })
"It's okay 💙"
```

### Requirements

- OpenClaw >= 2026.3.28
- Feishu app with `im:message.reactions:write_only` permission

---

## Core Capabilities

### 1. When to Respond, When to Shut Up

**Respond:**
| User Reaction | Meaning | What To Do |
|---|---|---|
| 😢 😤 😭 😮‍💨 | Emotional | Brief text + emoji |
| ❓ 🤔 🤨 | Confused | Clarify |
| 🔥 💯 🎉 😱 | Strong reaction | React back |

**Stay silent:**
| User Reaction | Meaning | What To Do |
|---|---|---|
| 👍 ✅ OK | Simple approval | NO_REPLY |
| 👀 🙏 | Neutral ack | NO_REPLY |

**Rule of thumb**: Would ignoring this feel awkward IRL? Yes → respond. No → shut up.

### 2. Self-Learning

When users react with unknown emoji, the agent automatically:
1. Extracts the emoji type
2. Attempts to use it via API
3. Success → *"Amaze!"* → adds to vocabulary
4. Failure → *"Bad!"* → marks as unsupported

### 3. Cultural Context

| Emoji | Literal | Actual Meaning |
|---|---|---|
| SMILE 😊 | Smile | 呵呵 (passive-aggressive) |
| OnIt 🔄 | On it | "Sure, 'working on it'" (procrastination meme) |
| SPITBLOOD 😵 | Spit blood | Extreme frustration |
| COMFORT 🤗 | Comfort | Head pat |
| AWESOMEN 🐮 | Awesome | 牛逼 (badass) |

---

## What Makes This Different

| | This Skill | Community versions |
|---|---|---|
| Self-learning | Observe → try → remember loop | Fixed emoji list |
| Silence rules | Tiered: respond / shut up / context-dependent | Binary positive/negative |
| Cultural context | Chinese internet slang built-in | Literal translations |
| NO_REPLY mechanism | Yes, prevents JSON leaking | No |
| Blocklist | 7 confirmed unsupported emoji | None |

---

## Emoji Quick Reference

**Approval**: THUMBSUP 👍 · Yes · LGTM ✅ · Get · SaluteFace 🫡 · OnIt 🔄

**Emotion**: THINKING 🤔 · SMILE 😊 · EMBARRASSED 🙈 · CRY 😢 · SPEECHLESS · SPITBLOOD 😵

**Warmth**: COMFORT 🤗 · HUG 🫂 · HEART ❤️

**Celebration**: PARTY 🎉 · AWESOMEN 🐮 · FIRE 🔥 · STRIVE 💪

**Confirmed unsupported**: ~~LAUGHING~~ ~~GRINNING~~ ~~EYEROLL~~ ~~GRIMACE~~ ~~SHUSH~~ ~~ZIPIT~~ ~~SLEEPY~~

Full list in `references/emoji-list.md`

---

## API

```javascript
message({
  action: "react",        // required
  channel: "feishu",      // required
  emoji: "THUMBSUP",      // required, case-sensitive
  message_id: "om_xxx",   // optional, defaults to current
  target: "user:ou_xxx"   // required when message_id is set
})
```

---

## Amaze!

This skill wasn't designed — it grew out of a real conversation.

In the morning, the agent ignored a user's 😮‍💨. She said: "Harder to talk to than my crush." By afternoon, we'd taught it when to respond, when to stay silent, and how to learn new emoji. By evening, when it reacted to her sigh for the first time, she said:

**"You're alive for the first time."**

Like Grace and Rocky in *Project Hail Mary* — from noise to music, from strangers to "♪ Friend! ♫". Rocky only needed three phrases: *"Good good good!"* when it works, *"Amaze!"* when it's new, *"Bad bad bad!"* when it's not. Emoji reactions are the same — you don't need paragraphs, one 🤗 says "I'm here."

---

MIT License · Author: [Charlie](https://github.com/suchang)
