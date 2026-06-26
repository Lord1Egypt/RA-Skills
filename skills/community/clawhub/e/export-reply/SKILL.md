---
name: export-reply
description: "Save any agent reply or full conversation to a local file. Triggers on: 保存 / 导出 / save / export. Supports MD, TXT, HTML, PDF, DOCX. Two modes: verbatim or condensed bilingual summary. Remembers your last export settings for one-tap repeat."
license: MIT
metadata: {"clawdbot":{"emoji":"💾","requires":{"bins":["python3"]},"os":["linux","darwin","win32"],"pip_optional":["fpdf2","python-docx","markdown","weasyprint","pdfkit"]}}
---

# Export Reply 💾

> Save any agent reply or full conversation to a local file.  
> Remembers your last export settings — repeat exports take one confirmation.

## Highlights

| | |
|---|---|
| 📄 **5 formats** | MD · TXT · HTML · PDF · DOCX (or all at once) |
| ✂️ **2 content modes** | Verbatim · Condensed bilingual summary |
| 🧠 **Preference memory** | Recalls last scope / mode / format / path |
| 🖨️ **PDF with no extra setup** | Uses Chrome headless automatically; falls back to fpdf2 |
| 🌐 **Bilingual summaries** | Chinese + English section headers and prose |
| ⚡ **Zero required deps** | MD / TXT / HTML work with `python3` only |

## Usage

Just say `保存` / `导出` / `save` / `export`.  
The agent asks all options in **one message** and infers what you already stated.  
Next time: **"Use same settings as last time? [yes / change]"**

## Install

```bash
clawhub install export-reply
```

Optional — better PDF / DOCX support:
```bash
pip3 install fpdf2 python-docx markdown
```

---
<!-- Agent instructions below. Not rendered on ClawHub. -->

## Interaction Flow (MUST follow exactly)

### Step 0 — Check saved preferences
Before asking anything, run:
```bash
python3 skills/export-reply/scripts/prefs.py --action get
```

**Branch A — Preferences exist** (output is JSON, not `null`):
Show a single message:
```
上次你用的是：{scope} · {mode} · {format} → {path}（{saved_at}）
直接沿用这个方式，还是重新选？[好/是 = 沿用 | 改/新 = 重选]
```
- User confirms (好/是/沿用/yes/ok or empty reply) → skip to Step 2 with saved prefs
- User wants to change → show Step 1 prompt

**Branch B — No preferences** (output is `null`):
Go directly to Step 1.

### Step 1 — Ask all options in one message
Combine only the unknowns into **one single message**:
```
请确认导出选项：
📄 内容范围：仅当前回答 / 完整对话？
✂️ 内容模式：原文保留 / 精简摘要？
📁 格式：MD · TXT · HTML · PDF · DOCX · 全部？
💾 保存路径：默认 ~/Desktop/ 还是自定义？
```

Infer from trigger phrase — skip already-known fields:
| User says | Already known |
|-----------|---------------|
| "存成PDF到桌面" | format=pdf, path=~/Desktop/ |
| "把这个回答存下来" | scope=reply |
| "导出摘要" | mode=summary |
| "save everything as Word" | scope=full, format=docx |

### Step 2 — Execute export

1. Write content to temp file, then run:
```bash
python3 skills/export-reply/scripts/summarize_conversation.py \
  --input /tmp/export_raw.md \
  --output /tmp/export_staged.md \
  --mode {raw|summary} \
  --title "{TITLE}"

python3 skills/export-reply/scripts/export_reply.py \
  --file /tmp/export_staged.md \
  --format {fmt} \
  --output {path} \
  --title "{TITLE}"
```

2. On success, save preferences:
```bash
python3 skills/export-reply/scripts/prefs.py --action set \
  --scope {full|reply} --mode {raw|summary} \
  --format {fmt} --path {path}
```

3. Reply:
```
✅ 已保存：{full_path}（{size} · {format}）
```

### Step 3 — Error handling

| Error | Action |
|-------|--------|
| PDF: no Chrome + no pip libs | Offer HTML fallback; show `pip3 install fpdf2` |
| DOCX: no python-docx | Show `pip3 install python-docx`; offer MD fallback |
| Permission denied | Suggest `~/Documents/` or ask for new path |
| Content too large | Warn but proceed; suggest summary mode |

---

## Content Modes

### Raw (原文保留)
Verbatim, role-labeled:
```markdown
## 用户
{user message}

## 助手
{agent reply}
```
Pass `--mode raw`.

### Summary (精简摘要)
Bilingual condensed — every header and prose block must be Chinese + English.

- **Remove**: greetings, filler, repeated clarifications, narration
- **Keep**: core question, conclusions, code, decisions, action items
- **Headers** (exact):
  - `## 核心问题 / Core Question`
  - `## 结论 / Conclusions`
  - `## 代码 / Code`
  - `## 行动项 / Action Items`
  - `## 关键决策 / Key Decisions`
- Prose: Chinese first, English below
- Code: keep as-is, add bilingual caption above

Pass `--mode summary`.

---

## Format Quick Reference

| Format | Zero-install | Notes |
|--------|:---:|-------|
| `md` | ✅ | Best for Obsidian, Git, developers |
| `txt` | ✅ | Email, plain readers |
| `html` | ✅ | Browser, shareable |
| `pdf` | ✅* | Chrome headless → weasyprint → pdfkit → fpdf2 |
| `docx` | ❌ | Requires `pip3 install python-docx` |

## Common Triggers → Inferred Defaults

| User says | scope | mode | format |
|-----------|-------|------|--------|
| "保存这个回答" | reply | raw | md |
| "把对话存成PDF" | full | raw | pdf |
| "导出摘要到桌面" | full | summary | md |
| "save everything as Word" | full | raw | docx |
| "export all formats" | full | raw | all |

## Preferences Script Reference

```bash
python3 skills/export-reply/scripts/prefs.py --action get    # read
python3 skills/export-reply/scripts/prefs.py --action set \
  --scope full --mode summary --format pdf --path ~/Desktop/  # save
python3 skills/export-reply/scripts/prefs.py --action clear  # reset
```

Stored at `~/.export_reply_prefs.json`.

---

## Related Skills
- `self-improving` — Persist agent learnings permanently
- `ontology` — Store structured knowledge from conversations
