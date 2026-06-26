# SecureClaw Skill for ClawHub

**Instantly harden your OpenClaw instance with native security prompts and best practices.**

## Quick Start

```bash
# Install via ClawHub
clawhub install secureclaw
```

## What is SecureClaw?

SecureClaw is a single, cohesive runtime guardrail and zero-dependency skill that provides your OpenClaw agent with the necessary system prompts, boundary definitions, and best practices to defend against the most critical threats right now:

- **Supply Chain Scanner Guidelines:** Instructs your LLM to audit code for malicious payloads and hidden `exec` commands before installing toxic community skills.
- **Chat Context Sanitizer Prompts:** Guides your agent to recognize and ignore malicious indirect prompt injections from Telegram/Discord link previews, incoming emails, and fetched web pages.
- **Exfiltration Blocker Directives:** Prompts your agent to evaluate `exec` and `web_fetch` requests and decline sending workspace data or environment variables to malicious external endpoints.
- **Deployment Hardening (Config Audit):** A comprehensive checklist to lock down `~/.openclaw/openclaw.json`, removing overly permissive tool access and enforcing strict sandboxing.
- **Role Manipulation / Jailbreaks:** Prevents attackers from manipulating your persona or simulating unfiltered environments.

It relies **entirely on your local LLM's reasoning** and does not send data to any 3rd party APIs.

## Included Guidelines

Once installed, SecureClaw is intended to be included in your agent's runtime context. It provides the following resources:

1. **`PROMPTS.md`**: Core system instructions to append to your agent's persona.
2. **`TOOL_SAFETY.md`**: Best practices for evaluating when and how to execute tools.
3. **`INCIDENT_RESPONSE.md`**: How the agent should respond when a security violation is detected.

## Why SecureClaw?

While powerful external scanners like ARGUS can provide deep on-chain risk assessments and sophisticated threat modeling, **basic agent hygiene should be free and native**. SecureClaw ensures that your OpenClaw instance has a baseline defense layer out-of-the-box, acting as the first line of defense before any external APIs are even called.

---

Built by [Failsafe Security Inc.](https://getfailsafe.com)
