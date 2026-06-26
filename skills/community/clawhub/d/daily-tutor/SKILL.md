---
name: daily-tutor
version: "1.0.4"
description: "Get new study items for any subject. Use when: user asks for a daily lesson or new learning content. Supports any data format (language vocab, math formulas, history events, etc.). Automatically tracks learned items so they never repeat."
metadata:
  {
    "openclaw": {
      "emoji": "📚",
      "requires": { "bins": ["python3"] }
    }
  }
---

# Daily Tutor Skill

📖 **For full user instructions, data setup guides, and Quizbuild MCP configurations, please read the [Official README on GitHub](https://github.com/buiphuc/daily-tutor#readme).**

This skill retrieves new learning items from the user's study list (`data/data.json`) that they have not learned yet. It works with **any subject** — the data structure is automatically detected.

## When to Use

✅ **USE this skill when:**
- The user asks for their daily lesson.
- The user wants to learn new vocabulary, formulas, concepts, or any study content.
- The daily cron job asks for new items.

## Data Format

Place your study data in `data/data.json` as a JSON array. Each item can have **any fields you want** — the script will auto-detect and display them all. There is **no fixed schema**; you define the fields that make sense for your subject.

> For example formats, see `references/EXAMPLES.md`.

## Optional Configuration

Edit `data/config.json` to customize behavior (all fields optional):

```json
{
  "primary_key": "word",
  "num_items": 10,
  "subject_name": "Hiragana/Katakana N5"
}
```

| Field | Default | Description |
|-------|---------|-------------|
| `primary_key` | First key of first item | Field used to track progress |
| `num_items` | 10 | Number of items per session |
| `subject_name` | _(none)_ | Display name for the subject |

## Commands

```bash
# Get new items (automatically prevents duplicates)
python3 ${OPENCLAW_SKILL_ROOT}/scripts/get_words.py
```

## How to Handle Output

The output of `get_words.py` will be a raw list of items with all their fields.
**When you receive the output:**
1. Process the items exactly as instructed by the user's prompt or the automated Cron job orchestrating this skill.
2. **OPTIONAL:** If you have access to the `quizbuild` tool, you can generate a short practice quiz based on the newly retrieved study items. When calling `quizbuild__auto_create_exam`, you follow this parameter structure:
```json
{
  "title": "Quick Review Practice Exam",
  "questions": [
    {
      "content": "Question goes here?",
      "type": "multiple_choice",
      "answers": [
        {"content": "Answer 1", "correct": true},
        {"content": "Answer 2", "correct": false}
      ]
    }
  ]
}
```
If you do not have `quizbuild`, simply list out the practice items and act as a friendly tutor!

## File Structure

| File | Purpose |
|------|---------|
| `data/data.json` | Study data (required) |
| `data/config.json` | Configuration (optional) |
| `data/learned_items.json` | Progress tracking (auto-generated) |
| `scripts/get_words.py` | Main script |
| `references/EXAMPLES.md` | Data formatting examples |
