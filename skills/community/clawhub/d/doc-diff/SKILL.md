---
name: doc-diff
description: "Compare two documents or files and generate a structured diff report. Use when: user asks to compare files, find differences between documents, generate diff report, or check what changed between two versions."
metadata: { "openclaw": { "emoji": "📄", "requires": { "bins": ["diff"] } } }
---

# Document Diff Skill

Compare two documents or files and generate a structured difference report in Chinese.

## When to Use

✅ **USE this skill when:**

- "对比这两个文件"
- "这两个文档有什么区别？"
- "生成差异报告"
- "找出两个版本之间的变化"
- "Compare file A and file B"

## Workflow

### Step 1: Get file paths

Ask the user for the two file paths to compare if not provided.

### Step 2: Run diff

```bash
# Basic diff (line by line)
diff file_a.txt file_b.txt

# Unified format (shows context lines, recommended)
diff -u file_a.txt file_b.txt

# Side-by-side comparison
diff -y --width=120 file_a.txt file_b.txt

# Ignore whitespace differences
diff -u -b -B file_a.txt file_b.txt

# Word-level diff (more granular)
diff -u --word-diff=plain file_a.txt file_b.txt
```

### Step 3: For directory comparison

```bash
# Compare two directories recursively
diff -rq dir_a/ dir_b/

# Full diff of all files in directories
diff -ru dir_a/ dir_b/
```

### Step 4: Generate report

After running diff, present the results as a structured report with these sections:

1. **概览 (Overview)** — file names, total lines changed
2. **新增内容 (Additions)** — lines added (marked with `+`)
3. **删除内容 (Deletions)** — lines removed (marked with `-`)
4. **变更摘要 (Summary)** — brief description of what changed and why it matters

## Output Format

Present the report in Chinese with clear sections:

```
📄 文档对比报告
================
文件 A: <path>
文件 B: <path>

📊 变更概览
- 新增行数: X
- 删除行数: X
- 变更行数: X

➕ 新增内容
...

➖ 删除内容
...

📝 变更摘要
...
```

## Notes

- For binary files (Word, PDF), read both files first and compare the extracted text
- For large files, focus on significant changes and summarize repeated patterns
- Always show the diff output first, then explain in plain Chinese what changed
