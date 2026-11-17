<div align="center">

# 🧠 english-memory-method

**Turn "memorizing English articles" from rote grinding into a path you can actually walk.**

Paste any English article, and it produces a **13-section study plan** (self-contained HTML):
sentence-by-sentence linking marks, hooks welded into question chains, a retelling ladder, terminology tables, collapsed self-tests — all in one file.

![Version](https://img.shields.io/badge/version-2.3.0-blue)
![Platforms](https://img.shields.io/badge/platforms-16+-teal)
![Skill Sections](https://img.shields.io/badge/skill_sections-13-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Standard](https://img.shields.io/badge/Agent_Skills-standard-red)

[Install](#-quick-start) · [Features](#-features) · [How it works](#-how-it-works13-section-closed-loop) · [Platforms](#-platform-support) · [中文](readme.md)

</div>

---

## ✨ Features

| | Feature | In one line |
|---|---|---|
| 🧠 | **Chained retelling** | Hooks are welded into question chains: each link is *inferred* from the previous one — whatever can be derived doesn't need memorizing |
| 📖 | **Close reading** | Chinese translation + full connected-speech marking (⌒ linking / weak forms / flap t / h-dropping) + term highlighting |
| 📚 | **Terminology tables** | Word-formation breakdown (roots & affixes) + IPA + memory hooks — know the root, and new words become familiar ones |
| 💬 | **Life examples for phrases** | Every collocation gets a plain-English daily sentence, **ready to mimic** (no translation — think in English) |
| 🗂 | **13-section closed loop** | Strategy → close reading → hooks & chains → retelling ladder → three-pass → review → self-test → accumulation |
| 🔒 | **Collapsed self-tests** | Fill the blanks first; answers hide behind "▶ 查看本段答案" toggles, auto-hidden when printing |
| 🖥 | **16+ platforms, one command** | Claude Code / Codex / Trae / Lingma / Comate / CodeBuddy / WorkBuddy / Kimi / MiniMax… |
| 📄 | **Self-contained single file** | Each plan is one HTML: inline SVG, collapsible, print-friendly, zero external dependencies |

---

## 🚀 Quick Start

**Windows (PowerShell)**:

```powershell
irm https://cdn.jsdelivr.net/gh/yxdwind/english-memory-method@main/install.ps1 | iex
```

**macOS / Linux**:

```bash
curl -fsSL https://cdn.jsdelivr.net/gh/yxdwind/english-memory-method@main/install.sh | bash
```

**Claude Code (zero CLI)**:

```
/plugin marketplace add yxdwind/english-memory-method
/plugin install english-memory-method
```

**npm / npx**:

```bash
npx english-memory-method
```

> The installer auto-detects **every installed platform** and deploys to each one (16+ aliases — see [Platform Support](#-platform-support)).
> If jsdelivr lags, switch to the official source: `irm https://raw.githubusercontent.com/yxdwind/english-memory-method/main/install.ps1 | iex`

**Trigger**: paste an English article + ask for a memorization plan. No restart needed.

---

## 📖 How it works (13-section closed loop)

| # | Section | What it does |
|---|---|---|
| 1 | Strategy | Detect genre & skeleton, estimate length and days |
| 2 | Structure map | Compress the article into one SVG map |
| 3 | Close reading | Translation + linking marks + term highlighting, sentence by sentence |
| 4 | Keyword table | 1–2 hook words per sentence + Chinese cues |
| 5 | Question chain | Weld hooks into 4–7 signpost questions — self-QA when retelling |
| 6 | Retelling ladder | L1 hooks → L2 chain → L3 titles → L4 bare hands → L5 tell someone |
| 7 | Three-pass method | Read ×3 → retell with hooks → retell with the chain |
| 8 | Spaced review | 5 min → tonight → next day → day 3 → day 7/15 |
| 9 | Fill-in-blank test | 2–5 blanks per paragraph; answers collapsed |
| 10 | Phrase list | 8–15 collocations + life examples |
| 11 | Terminology | Word-formation breakdown + IPA + memory hooks |
| 12 | Memory hooks | Alliteration / rhyme / parallelism / contrast / signposts / quotes |
| 13 | Retelling toolkit | 10 techniques: stall recovery / delivery / practice tips |

**Core idea**: isolated hooks = broken points — you memorize the hooks, the order, AND the mapping. Triple burden.
v2 welds hooks into chains: each link is *inferred* from the previous one — **whatever can be logically derived doesn't need memorizing**.

---

## 🖥 Platform Support

Built on the open **Agent Skills standard** (`skills/<name>/SKILL.md`). Three tiers:

- **L1 · Native skill install**: AutoClaw / OpenClaw / Claude Code / Codex / Trae / Lingma / Comate / CodeBuddy / WorkBuddy / Kimi Code / MiniMax / Qwen Work / Windsurf / Continue / Roo Code
- **L2 · Rule injection** (Markdown plans): Cursor / Qoder / GitHub Copilot / Gemini CLI / Cline / Aider — adapters in [`platforms/`](platforms/README.md)
- **L3 · Manual**: paste `SKILL.md` content into any platform's custom instructions

Full matrix (21 platforms × install methods): **[platforms/README.md](platforms/README.md)**.

---

## 📜 Version History

<details>
<summary><b>Expand: all changes from v2.1 → v2.3.0</b></summary>

**v2.1**: sentence-by-sentence close reading — per-sentence translation (any language) + full connected-speech marking (⌒ linking / weak forms / flap t / h-dropping) with American IPA.

**v2.1.1**: ① "7.5 Retelling Toolkit" — 10 universal techniques appended after memory hooks; ② multi-platform support — installer deploys to 16 agent platforms, with rule adapters for platforms without skills.

**v2.2.0**: terminology — ① inline term highlighting in close reading; ② "6.5 Terminology" table (term / word-formation / IPA / Chinese / memory hook); all 30 existing plans upgraded.

**v2.2.1**: fill-in-blank answers hidden behind per-section toggles; auto-hidden when printing.

**v2.3.0**: ① phrase list upgraded to a 3-column table with life examples; ② all sections renumbered 1–13.

</details>

---

## 🎯 Use cases

CET-4/6, Kaoyan, IELTS/TOEFL intensive listening & recitation, adult self-study, AI-assisted language learning.
Companion methods (same series): the 5-step intensive-listening diagnosis, and the 4-step linked-speech breakdown.

## 📄 License

[MIT](LICENSE)
