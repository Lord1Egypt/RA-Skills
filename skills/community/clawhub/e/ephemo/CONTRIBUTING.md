# Contributing to Ephemo Agent Skills

First off, thank you for considering contributing to the Ephemo Agent ecosystem! 🚀

This repository specifically manages the **Agentic Intelligence Layer** for [ephemo.online](https://ephemo.online). While our core backend infrastructure is private, we welcome all contributions that help improve how AI Agents (like OpenClaw, Hermes, Claude, and more) interact with our platform.

## What we need help with

- **Prompt Engineering:** Improving the `SKILL.md` instructions to ensure agents correctly handle anonymous/permanent handoffs.
- **Edge-Case Logic:** Writing new directives for agents to handle multi-page sites, asset resolution, or 25MB payload management.
- **Platform Compatibility:** Ensuring our Skill metadata remains perfectly compliant with the latest `AgentSkills` specifications.

## How to Contribute

1. **Fork the repo** and create your branch from `main`.
2. **Modify the Skill:** Make your changes strictly within the `ephemo-agent-skill/` directory.
3. **Test it:** If you have OpenClaw installed, point your local workspace to your forked skill to verify the agent follows the new instructions.
4. **Pull Request:** Submit a clear PR description detailing what has improved in the agent's behavior.

## Our Philosophy

We believe in a world where **AI builds and humans approve.** Your contributions help make that approval process frictionless, secure, and instant for everyone on the web.

---

### Security Note

Never submit pull requests that:
- Expose local credentials (`~/.ephemo_credentials`).
- Include sensitive API tokens or secrets.
- Attempt to bypass the 25MB safety limits of the edge network.

---

**[ephemo.online](https://ephemo.online)** · Designed for the humans. Built for the machines.
