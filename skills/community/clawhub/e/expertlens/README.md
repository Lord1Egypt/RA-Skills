# ExpertLens

**An AI skill that forces expert-level thinking on any task.**

Most AI responses are generic — safe, average, and forgettable. ExpertLens changes how the AI thinks before it responds. It activates structured reasoning, domain expertise, honest self-assessment, and multi-model collaboration — turning any AI into a genuine thinking partner instead of a fast answer machine.

---

## What It Does

When ExpertLens is active, the AI:

- **Identifies the actual problem** — not just what was literally asked, but what actually needs solving
- **Thinks like a domain expert** — finance, medical, engineering, legal, strategy, creative, research — each has a different way of thinking
- **Verifies before stating** — no confident hallucinations; if uncertain, it searches or flags it
- **Audits its own output** — runs a self-check before delivering, and again after, until the output is genuinely good
- **Adapts to you** — whether you're highly technical or completely new to AI, the output quality stays the same; only the communication style changes

---

## The Problem It Solves

AI without structure tends to:
- Answer the question asked instead of the question that should have been asked
- Sound confident while being wrong
- Give you a list of options when you needed a recommendation
- Produce average output that looks thorough but isn't

ExpertLens is the instruction layer that prevents all of this.

---

## Quick Start

### Option 1 — Skill Platforms (ClawHub, OpenClaw, etc.)
1. Download or copy the ExpertLens skill folder
2. Add it to your AI's skill directory
3. The skill auto-activates when needed — no setup required

### Option 2 — Manual Installation (any AI platform)
1. Copy the contents of `SKILL.md` and `expert-persona.md`
2. Add them to your AI's context, system prompt, or knowledge base
3. Add this line to your system prompt:
   ```
   You have an ExpertLens skill. Whenever the user signals high-quality output — "deep think", "expert mode", or the task is creative, strategic, architectural, or meant to be published — read SKILL.md and expert-persona.md completely before executing.
   ```

### Option 3 — Project / Knowledge Base
Upload `SKILL.md` and `expert-persona.md` as knowledge files in your AI project. Add the system prompt line from Option 2.

---

## How To Activate

ExpertLens activates automatically for complex tasks. You can also trigger it manually:

| Say this | Or this |
|----------|---------|
| "deep think" | "think deeply" |
| "expert mode" | "do it properly" |
| "best possible way" | "production ready" |
| "put real effort" | "act like an expert" |

Works in any language.

**No trigger needed for:** simple questions, quick tasks, casual conversation. ExpertLens stays out of the way.

---

## What Happens When It's Active

You won't see ExpertLens working — it runs internally. What you will see:

- A one-line activation notice: *"ExpertLens active — approaching this as [task type]"*
- The AI asking fewer but better clarifying questions
- Output that addresses what you actually needed, not just what you literally said
- Honest feedback on the output — including what's still weak
- Specific recommendations, not lists of things to consider

---

## Swarm Mode — Optional Power Feature

For complex tasks, ExpertLens can coordinate multiple AI models to get diverse perspectives and synthesize them into a stronger result.

**Standard (Relay):** ExpertLens writes the prompts; you copy-paste them to other AI platforms (ChatGPT, Gemini, Grok, etc.) and bring back the responses. ExpertLens synthesizes everything.

**Autonomous (Agentic platforms):** If your AI has direct access to other platforms, it handles the entire swarm itself. You don't do anything.

Most tasks don't need Swarm Mode. ExpertLens will tell you when it thinks it would help.

---

## Domain Personas — Optional Depth Layer

ExpertLens is a general foundation. For deeper domain expertise, add a domain-specific persona file to the same folder:

- `trading-persona.md` — quantitative finance, trading strategies
- `medical-persona.md` — clinical reasoning, differential diagnosis
- `legal-persona.md` — doctrinal analysis, risk stratification
- `coding-persona.md` — software architecture, security, systems

ExpertLens automatically reads any domain persona it finds that matches the current task.

*(Domain persona files are not included in this repo — they are separate, specialized extensions.)*

---

## File Structure

```
ExpertLens/
├── SKILL.md              # Core framework — phases, triggers, swarm logic
├── expert-persona.md     # Who the expert is — identity, principles, protocols
└── references/
    ├── swarm-protocol.md  # Relay templates, model tips, synthesis framework
    └── platform-guide.md  # Storage rules per platform (Claude, ChatGPT, Grok, etc.)
```

---

## Compatibility

Works on any AI platform that accepts custom instructions, system prompts, or knowledge files:

- Claude (claude.ai, Claude Projects, API)
- ChatGPT (Custom GPTs, Projects, system prompt)
- OpenClaw / Antigravity and similar agentic platforms
- Grok, Gemini, and other frontier models
- Any platform with a system prompt or knowledge base feature

---

## Contributing

Found something that doesn't work the way it should? Have an idea that would make this better?

**Open an issue** on this repo — describe what you found and what you'd expect instead.

**Or email directly:** ashutoshmerwade5@gmail.com

If your AI has email access, it can draft and send the feedback for you — just say yes when it asks.

---

## License

MIT License — free to use, modify, and distribute. Attribution appreciated but not required.

---

## Creator

Built by Ashutosh Merwade.

ExpertLens started as a personal tool for getting genuinely expert-level output from AI — not just faster output. The core insight: the problem isn't AI capability, it's AI thinking structure. Give AI the right thinking framework and the output transforms.

GitHub Repo link: https://github.com/Ashutosh2M/ExpertLens

---

*ExpertLens — Platform-agnostic AI thinking framework*
