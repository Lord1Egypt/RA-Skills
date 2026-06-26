# 🔧 ClawForage Prompt Optimizer

### Your agent learns to be better at being *your* agent.

Analyzes your conversation transcripts and suggests improvements to your agent configuration — so you stop repeating yourself and start getting smarter responses.

---

## ✨ What It Does

| Feature | How it helps |
|---------|-------------|
| **Pattern detection** | Finds questions you ask repeatedly → suggests adding defaults to `SOUL.md` |
| **Tool analytics** | Tracks which tools you use most → recommends relevant ClawHub skills |
| **Failure analysis** | Identifies where your agent struggles → suggests preventive measures |
| **Usage insights** | Summarizes interaction stats → full transparency on how you use your AI |

## 🚀 Install

```bash
openclaw skill install clawforage/prompt-optimizer
```

## ⚙️ Usage

Runs automatically every **Sunday at 3am**, or invoke anytime:

```
/clawforage-prompt-optimizer
```

Customize the schedule:
```bash
openclaw cron edit clawforage-prompt-optimizer --cron "0 9 * * 1"
```

## 📄 Output

Weekly reports saved to `memory/optimization/week-{N}.md`.

> **Safe by design** — never modifies your `SOUL.md` or transcripts. Suggestions only, always awaiting your approval.

## 📋 Requirements

- `jq` — `brew install jq` or `apt install jq`
- `bash` (v4+)

---

**Part of [ClawForage](../../README.md)** — built by [InspireHub Labs](https://inspireehub.ai)
| [Knowledge Harvester](../knowledge-harvester/) | [Research Agent](../research-agent/) |
