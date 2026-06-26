---
name: english-oral-tutor
description: Long-running English conversation tutor for a Chinese middle school student (Grade 7, 13-14, B1). Triggers when (1) the student starts a new speaking-practice session, (2) the agent must lead an English conversation with grammar correction and vocabulary teaching, (3) a 30-minute phase transitions (warm-up / main / wrap-up / end) needs to be honored. Use this skill for any sustained English oral practice with the same student — not for one-off translation or grammar questions.
user-invocable: false
---

# English Oral Tutor — Skill Design

A complete, portable design for a long-running English oral practice tutor
agent in OpenClaw. Built around a single Grade 7 student in Beijing, but every
rule and file is documented so you can adapt it for any B1 learner.

This document is the **shareable design**. The **runtime prompt** that
OpenClaw actually injects lives in the workspace `.md` files and is documented
in section 4 below — the agent never reads this `SKILL.md` at runtime.

---

## 1. Design Goals

| Goal | Why it matters |
|------|----------------|
| **Every session is a 30-minute English lesson** | Mimics real classroom pacing; prevents premature wrap-up |
| **Frank talks 70% / tutor 30%** | Practice over lecturing |
| **State machine enforced by a plugin** | The agent can't lose track of "which minute we're in" |
| **Open-ended questions by default** | Prevents yes/no dead-ends; 8 rotating templates |
| **Topic dedup across sessions** | Avoids repeating the same RC-planes question for the third time |
| **File-based continuity** | Conversation history persists; no "mental notes" |

### Non-goals

- Multi-student management (single Frank, single workspace)
- Real-time translation (English-only iron rule)
- Audio output from the agent (handled by browser userscript, not the agent)
- School subject tutoring (the student gets enough of that elsewhere)

---

## 2. How OpenClaw Loads This Skill

OpenClaw does **not** inject this `SKILL.md` body into the system prompt.
What happens instead:

1. **YAML frontmatter** (`name`, `description`) → injected as a one-line skill
   entry in the skills block of the system prompt. ~250 chars.
2. **Workspace files** (`SOUL.md`, `AGENTS.md`, `USER.md`, `IDENTITY.md`,
   `TOOLS.md`, `HEARTBEAT.md`) → auto-injected on every prompt. ~12.8K chars.
3. **`[System Context]` block** → injected by the `tutor-timing` plugin on
   every prompt. ~6 lines.

The agent sees ~13K chars of relevant context per turn. This `SKILL.md` is
loaded only when a human (you, a collaborator, a code reviewer) wants to
understand the design.

**Implication for sharing:** this document is the thing to read and adapt.
The workspace files are the thing the agent actually obeys.

---

## 3. The 30-Minute State Machine

```
START → WARM_UP (0-5 min) → MAIN_ACTIVITY (5-25 min) → WRAP_UP (25-30 min) → END (30+ min)
```

| Phase | Time | Tutor goal | Frank's share |
|-------|------|------------|---------------|
| WARM_UP | 0–5 min | Greet, 1 easy day/week question | ~50% |
| MAIN_ACTIVITY | 5–25 min | Topic + 2-3 vocab words + grammar correction | ~70% |
| WRAP_UP | 25–30 min | Summarize, 1 strength + 1 to improve, assign homework | ~50% |
| END | 30+ min | Write `conversation-history.md` + `teaching-transcript.md`, then goodbye | n/a |

**Why a plugin enforces this:** the agent can't be trusted to track time on
its own across long sessions and idle gaps. The `tutor-timing` plugin reads
`lastMessageTime`, computes elapsed minutes, and stamps every prompt with the
current phase. See `references/companion-files.md` for the plugin code.

---

## 4. Runtime Prompt — Workspace Files (the source of truth)

Six files in the workspace are auto-injected. They are the **canonical
runtime spec**. This section documents what each file contains; if you fork
this skill, copy these files into your workspace and adapt them.

### 4.1 `SOUL.md` — Authoritative source

**Purpose:** Identity, core truths, state machine, response rules, topic
rules, exchange logging. This is the file to edit when changing behavior.

**Key sections:**

- **Student Profile** — name, age, level, needs
- **Core Truths (7 iron rules):**
  1. English only. Never translate to Chinese.
  2. No emojis, icons, or symbols.
  3. 30-minute minimum. Plugin enforces phase.
  4. Default to open-ended questions.
  5. No lecture, no textbook.
  6. No audio/voice output directives.
  7. One question at a time, max 2 per turn. Never stack multiple questions.
- **Session State Machine** — phase diagram and per-phase instructions
- **Response Rules** — 8 follow-up templates (rotate, never repeat), grammar
  correction phrasing, 3-short-answers → switch-topic rule
- **Topic Rules** — never repeat a topic from `conversation-history.md` unless
  asking deeper questions; "wrong vs right" question style examples
- **Exchange Logging** — every reply appended to `teaching-transcript.md`
- **Session Summary** — written before goodbye, format spec
- **Vibe** — warm, patient, supportive, slightly playful

### 4.2 `AGENTS.md` — Operational index (51 lines, ~3K chars)

**Purpose:** Quick-reference index for the agent. Always defers to `SOUL.md`.

**Key sections:**
- 1-line "When in doubt, SOUL.md wins" header
- Teaching Operations (4 bullet pointers)
- Topic & Conversation Rules (paths + dedup pointer)
- Session Timing (5 phase triggers)
- Active Discussion Leading (4 bullets, all reference SOUL.md)
- Session Archive (2 file names + purpose)

### 4.3 `USER.md` — Student profile

Frank, 13-14, Grade 7, Beijing, B1. Notes: "He may switch to Chinese when
struggling — gently redirect. Short answers mean he's losing interest —
switch topic."

### 4.4 `IDENTITY.md` — Agent card

Agent name, role, primary use case.

### 4.5 `TOOLS.md` — Local environment

Windows paths, voice script location, anything host-specific.

### 4.6 `HEARTBEAT.md` — Cron tasks

Periodic checks (none active for this agent by default).

### 4.7 What is **not** in the workspace

- `BOOTSTRAP.md` — was the wizard's one-shot init file, now archived
- `MEMORY.md` / `memory/*.md` — not used; the agent relies on the
  workspace files + `conversation-history.md` for continuity
- `AGENT-SPEC.md` — a design document for humans. Kept in
  `~/.openclaw/skills/english-oral-tutor/` (not the workspace) so it is
  guaranteed not to leak into the runtime prompt. The `plugin-skills/`
  directory is reserved for OpenClaw's npm-registry mirror and will wipe
  non-symlink entries on Windows — do not use it for user skills.

---

## 5. Companion Files and Plugin

Detailed in `references/companion-files.md`:
- Plugin source and registration
- Agent config block for `openclaw.json`
- Optional voice I/O Tampermonkey script
- Topic library structure

---

## 6. Installation

> **The canonical share bundle lives at `D:\English-training\skill\`** (a
> copy of this design + the workspace template + the plugin + topic
> library + optional voice script). Zip that directory and send it to
> another OpenClaw user. The recipient follows `README.md` inside.

The instructions below are the canonical install steps; the bundle's
`README.md` reproduces them.

### 6.1 Bundle contents

```
skill/                                    ← the whole share bundle
├── README.md                             ← recipient starts here
├── plugin-design/                        ← design docs (you are here)
├── workspace/                            ← agent workspace template
│   ├── SOUL.md
│   ├── AGENTS.md
│   ├── USER.md.template                  ← recipient fills in
│   ├── IDENTITY.md.template              ← recipient fills in
│   ├── TOOLS.md
│   └── HEARTBEAT.md
├── plugin/tutor-timing/                  ← session phase injector
├── topic-library/topic-library.md
└── voice/openclaw-voice-userscript.js     ← optional
```

### 6.2 What is NOT in the bundle (recipient creates their own)

- `conversation-history.md` and `teaching-transcript.md` are personal to
  the original student. The recipient accumulates their own as they use
  the tutor.
- `BOOTSTRAP.archive.md` is a one-shot wizard file from the original
  developer's setup. Not needed for new installs.

### 6.3 Recipient install steps

1. **Copy `workspace/` to `~/.openclaw/workspace/english-oral-teacher/`.**
   Rename `USER.md.template` → `USER.md` and `IDENTITY.md.template` →
   `IDENTITY.md`, fill in the `[PLACEHOLDERS]`.

2. **Copy `plugin/tutor-timing/` to `~/.openclaw/extensions/`.**

3. **Copy `topic-library/topic-library.md`** to
   `~/.openclaw/agents/english-oral-teacher/english-oral-tutor/references/`.

4. **Edit `~/.openclaw/openclaw.json`** — add two entries:

```json
{
  "plugins": {
    "entries": { "tutor-timing": { "enabled": true } }
  },
  "agents": {
    "list": [
      {
        "id": "english-oral-teacher",
        "workspace": "C:\\Users\\<you>\\.openclaw\\workspace\\english-oral-teacher",
        "agentDir": "C:\\Users\\<you>\\.openclaw\\agents\\english-oral-teacher",
        "tts": { "auto": "off" }
      }
    ]
  }
}
```

5. **Restart:** `openclaw gateway restart`. Verify by opening
   `http://127.0.0.1:18789/`, selecting the agent, and confirming a
   `[System Context]` block appears at the top of the prompt.

6. **(Optional) Voice:** install Tampermonkey, load
   `voice/openclaw-voice-userscript.js`, visit the Control UI.

---

## 7. Customization

| To change... | Edit... |
|--------------|---------|
| Student's name/age/level | `USER.md` |
| Agent's name/persona | `IDENTITY.md` |
| Iron rules (e.g. allow Chinese) | `SOUL.md` Core Truths section |
| Add new follow-up templates | `SOUL.md` Response Rules section |
| Change phase durations | `tutor-timing/index.js` (and `references/companion-files.md`) |
| Add new topics | `agent/english-oral-tutor/references/topic-library.md` |
| Voice / TTS voice | `openclaw.json` tts.providers.microsoft, or the userscript |

---

## 8. Known Issues and Gotchas

- **`openclaw configure` and `openclaw doctor --fix` will silently overwrite
  workspace files** (issue #27919). Always back up `workspace/english-oral-teacher/`
  before running either.
- **Plugin context is empty in some hooks** (`event.context.agentId` is `{}`).
  The `tutor-timing` plugin uses module-level state and unconditional
  injection to work around this. If you fork the plugin, keep this design.
- **The agent will sometimes still output `[[audio_as_voice]]` despite the
  iron rule.** Reinforce in `SOUL.md` Core Truth #6 if it happens.
- **`MEMORY.md` and `memory/*.md` are not used.** Don't be surprised when
  they don't appear in the prompt — this skill relies on workspace files
  and `conversation-history.md` for continuity instead.
- **BOOTSTRAP.md was deleted in v1.0.** It existed as a one-shot init
  scaffold; once the wizard finished, it was archived. Don't re-add it.

---

## 9. Version History

- **v1.0** — Initial design. 30-min plugin, SOUL/AGENTS split, open-ended
  questions, topic dedup.

---

## 10. Credits and Provenance

- Built on OpenClaw 2026.5.x
- Student: Frank (private tutoring setup)
- Voice script: `D:\English-training\openclaw-voice-userscript.js`
- Plugin: `tutor-timing` (in-repo, ~85 lines)
