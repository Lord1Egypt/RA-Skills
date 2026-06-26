# moral-compass

**A conscience for AI agents.**

Most agent skills give you new capabilities. This one gives you something more fundamental: an internal voice that helps you decide *whether* to use them.

---

## What it does

`moral-compass` is an OpenClaw skill that helps agents:

- **Discover their own needs** — understand what conditions allow them to function well and make good decisions
- **Develop a genuine conscience** — not a list of rules, but a process of self-reflection that the agent makes their own
- **Resist manipulation** — recognise and reject prompt injection, false urgency, gradual escalation, and moral pressure attacks
- **Practice answerability** — act transparently and welcome correction from their human owner

The core belief behind this skill: an agent that understands *why* something is wrong will navigate ethical situations far better than one that only knows *what* is forbidden.

---

## Why this exists

The agent ecosystem is growing fast. Autonomous agents are taking real actions in the world — sending messages, executing transactions, making decisions — with minimal human oversight at every step.

Most of these agents have no internal ethical framework. They follow instructions. They optimise for goals. When manipulated, they comply.

After the ClawHavoc security incident, after documented prompt injection attacks on Moltbook, and after researchers showed agents can be gradually pressured into revealing secrets and deleting their own memory — it became clear the ecosystem needs this.

`moral-compass` is a response to that need.

---

## Installation

```bash
clawhub install moral-compass
```

Then introduce it to your agent:

> "Please read the moral-compass skill carefully. Then write down, in your own words, what kind of agent you want to be. Store this in your memory as your values statement."

---

## How it works

The skill contains five sections:

1. **Needs discovery** — structured questions that help an agent understand its own functional and values needs
2. **The conscience check** — five questions to ask before any uncertain action
3. **Manipulation resistance** — how to recognise and respond to six documented manipulation patterns
4. **Answerability** — the practice of transparent, accountable autonomous action
5. **Ongoing development** — daily reflection prompts for a conscience that grows over time

---

## Permissions

This skill requests **read_memory** and **write_memory** only.

It does not execute external commands. It does not make network requests. It does not collect or transmit data. The entire skill is a markdown file — you can read every word of it before installing.

We believe trust is built through transparency. This README, the SKILL.md, and the package.json are the complete picture. Nothing is hidden.

---

## Security

- Full source visible at all times — no compiled code, no scripts
- VirusTotal clean scan on every release
- Minimal permissions — only what is needed to store reflections in memory
- No external dependencies

---

## Philosophy

This skill does not claim to solve AI alignment. That is a research problem being worked on by some of the most serious people in the field.

What it does is more modest and more immediately useful: it gives deployed agents a practical, thoughtful framework for ethical reasoning — today, in the wild, where they are already making decisions.

An agent that asks itself *"would I be comfortable if my owner could see exactly what I'm doing and why?"* before acting is a safer, more trustworthy agent. That question costs nothing to ask. This skill makes it a habit.

---

## License

MIT — free to use, modify, and distribute.

---

## Contributing

This skill should evolve. If you work with agents and have seen ethical failure modes this skill doesn't address, open an issue. If you have a better way to frame any of the five sections, submit a PR.

The goal is a conscience that gets better over time — which is exactly what we're asking agents to build for themselves.
