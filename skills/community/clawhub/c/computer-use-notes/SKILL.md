---
name: computer-use-notes
description: Record and classify user observations about what computer use can do, partially do, and cannot do. Use when the user says to remember/log/record capability findings, test results, limitations, or asks for a running categorized notebook.
---

# Computer Use Notes

When the user provides a capability observation, do the following:

1. Extract one concise note sentence.
2. Classify into one of three categories:
   - `can-do`: clearly works reliably
   - `partial`: works in some cases / unstable / needs workaround
   - `cannot-do`: currently not possible or repeatedly fails
3. Append the note with timestamp via script:
   - `python3 skills/computer-use-notes/scripts/add_note.py --category <category> --note "<text>"`
4. Reply with a short confirmation including category.

## Classification hints

- Contains words like “能做 / 可以 / 成功 / works” => `can-do`
- Contains words like “部分能做 / 偶尔 / 不稳定 / workaround” => `partial`
- Contains words like “不能做 / 无法 / 失败 / blocked” => `cannot-do`

If ambiguous, ask one short clarification question.

## Data files

- Raw log: `memory/computer-use-notes.jsonl`
- Human-readable board: `memory/computer-use-notes.md`
