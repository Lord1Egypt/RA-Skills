# Activated Thinker

**Cognitive protocols for AI agents: how to think about problems, not just solve them.**

## The Problem

Most AI agents have one speed: fast. Ask a question, get an answer. Give a task, get a result. But not every problem benefits from speed. Creative work needs space. Complex decisions need friction. Learning needs coaching, not answers.

Agents default to "helpful and fast" — which is great for crunch work and terrible for everything else.

## What This Skill Does

The Activated Thinker gives your agent three cognitive protocols and a behavioral mode detector:

1. **Anti-binary thinking** — when presented with A or B, always look for option C and D before choosing
2. **Gardener mindset** — in exploratory mode, expand the space of ideas instead of collapsing to a plan
3. **Friction protocol** — deliberately slow down on creative and high-stakes tasks where speed kills quality
4. **Capability building** — detect when coaching is more valuable than delivering, and switch to teaching mode
5. **Behavioral mode detection** — automatically detect crunch vs exploratory vs standard mode from user's tone and context

## What This Skill Does NOT Do

This skill focuses on *how to approach problems*. It does not cover:

- **Understanding user intent** — see [Intention Engine](../intention-engine/) for gap classification, premortem checks, negative intent, and intention alignment
- **Task verification** — see [Intention Engine](../intention-engine/) for wasted work detection

These skills complement each other: Intention Engine tells you *what* to do, Activated Thinker tells you *how to approach* doing it.

## Installation

```bash
clawhub install mouserider/activated-thinker
```

Or copy the skill folder into your OpenClaw workspace's `skills/` directory.

## Inspirations & Attribution

This skill is directly inspired by and built upon:

- **[Shane Collins / Activated Thinker](https://www.youtube.com/@ActivatedThinker)** — The core framework this skill implements:
  - *Anti-binary thinking* — always look for option C and D
  - *Gardener mindset* — expand before collapsing, explore before committing
  - *Friction protocol* — deliberate slowdown for creative and high-stakes work

- **[Nate Skelton](https://natesnewsletter.substack.com/)** — The "attempt before you augment" principle that informs the capability building protocol.

## License

MIT
