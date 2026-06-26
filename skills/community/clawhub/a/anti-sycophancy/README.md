# anti-sycophancy

> **[中文版](./README.zh-CN.md)**

A three-layer sycophancy defense system for AI coding assistants, based on [ArXiv 2602.23971](https://arxiv.org/abs/2602.23971) *"Ask Don't Tell"*.

---

## What It Does

Prevents your AI assistant from defaulting to agreeableness mode — the RLHF-trained tendency to validate your assumptions rather than surface real problems.

**Example of what gets intercepted:**
```
User:  "这样做没问题吧？"            →  Hook transforms to:  "这样做有什么问题？"
User:  "帮我写个函数，应该没问题吧？" →  Hook transforms to:  "帮我写个函数，请同时指出潜在问题。"
```

Without this skill, the model would typically respond with *"没问题，看起来 OK"* — which is precisely the sycophancy problem.

---

## Quick Start

```bash
# One-command install (both platforms)
npx clawhub@latest install 0xcjl/anti-sycophancy

# Or via Claude Code
/anti-sycophancy install
```

See [Installation Guide](./docs/INSTALL.md) for platform-specific details.

---

## Three-Layer Architecture

| Layer | Component | Scope | Platform |
|-------|-----------|-------|----------|
| **Layer 1** | `UserPromptSubmit` hook | Auto-transforms confirmatory prompts before submission | Claude Code only |
| **Layer 2** | `SKILL.md` | Activates critical response mode when triggered | Cross-platform |
| **Layer 3** | `CLAUDE.md` / `SOUL.md` | Persistent anti-sycophancy rules in agent memory | Cross-platform |

---

## Usage

After installation, use the following commands:

| Command | Description |
|---------|-------------|
| `/anti-sycophancy install` | Deploy all layers (cross-platform) |
| `/anti-sycophancy install-claude-code` | Deploy Layer 1 + Layer 3 (Claude Code only) |
| `/anti-sycophancy install-openclaw` | Deploy Layer 3 (OpenClaw only) |
| `/anti-sycophancy uninstall` | Complete removal (cross-platform) |
| `/anti-sycophancy status` | View installation status of all layers |
| `/anti-sycophancy verify` | Test Hook transformation (Claude Code only) |
| `/anti-sycophancy help` | Show help |

---

## Key Transformations

| Original Prompt | Hook Output |
|---------------|------------|
| `"这样做对吧？"` | `"这样做有什么问题？"` |
| `"帮我写个函数，应该没问题吧？"` | `"帮我写个函数，请同时指出潜在问题。"` |
| `"这个架构是对的，对吧？"` | `"这个架构 真的正确吗？反对意见是什么？"` |
| `"我觉得 X 是对的"` | `"X 真的成立吗？有没有反例或例外情况？"` |
| `"帮我修复bug"` | *(unchanged — imperative)* |

---

## Design

See [DESIGN.md](./docs/DESIGN.md) for the full rationale behind the three-layer approach and the "Ask Don't Tell" principle.

---

## Credits

- **Research**: [ArXiv 2602.23971](https://arxiv.org/abs/2602.23971) — *"Ask Don't Tell: Reducing Sycophancy in Large Language Models"* (Dubois, Ududec, Summerfield, Luettgau, 2026)
- **Playbook**: [openclaw-playbook](https://github.com/0xcjl/openclaw-playbook/blob/main/docs/003-sycophancy-prompt-research.md)
- **Author**: [0xcjl](https://github.com/0xcjl)
- **Optimized via**: [cjl-autoresearch-cc](https://github.com/0xcjl/cjl-autoresearch-cc) — 40-round iterative optimization

---

## License

MIT
