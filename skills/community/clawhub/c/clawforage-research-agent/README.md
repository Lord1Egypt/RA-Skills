# 🔬 ClawForage Research Agent

### Turn scattered news into structured intelligence.

Goes beyond daily briefings — extracts entities, maps connections across articles, tracks evolving stories, and generates domain research reports that make you the smartest person in the room.

---

## ✨ What It Does

| Feature | How it helps |
|---------|-------------|
| **Entity extraction** | Identifies companies, people, products, and technologies across your knowledge base |
| **Connection mapping** | Finds shared entities across articles — reveals hidden relationships and patterns |
| **Timeline tracking** | Chronological view of developments — see how stories evolve |
| **Domain reports** | Synthesized intelligence with key developments, entity maps, and forward-looking outlook |
| **Source management** | Tiered source whitelists so you know what to trust |

## 🚀 Install

```bash
openclaw skill install clawforage/research-agent
```

**Prerequisite:** Requires the [Knowledge Harvester](../knowledge-harvester/) to populate articles first:
```bash
openclaw skill install clawforage/knowledge-harvester
```

## ⚙️ Usage

Runs automatically **Monday + Thursday at 4am**, or invoke anytime:
```
/clawforage-research-agent
```

Source whitelists are auto-created on first run, or configure manually:
```bash
mkdir -p memory/clawforage/sources
# Edit memory/clawforage/sources/{domain-slug}.md
```

## 📄 Output

Domain reports saved to `memory/research/{domain}/report-{YYYY}-{WW}.md`, containing:

- **Key Developments** — top stories synthesized into a narrative
- **Entity Map** — who's who and what they're doing
- **Connections** — cross-article patterns and evolving stories
- **Outlook** — what to watch next

## 📋 Requirements

- `jq` — `brew install jq` or `apt install jq`
- `bash` (v4+)
- `grep` with extended regex support

---

**Part of [ClawForage](../../README.md)** — built by [InspireHub Labs](https://inspireehub.ai)
| [Prompt Optimizer](../prompt-optimizer/) | [Knowledge Harvester](../knowledge-harvester/) |
