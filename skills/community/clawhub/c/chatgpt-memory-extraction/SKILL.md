---
name: chatgpt-memory-extraction
description: "Extract structured personal memories from ChatGPT export data (conversations JSON). Produces organized timeline, people profiles, and thematic records by deeply reading every conversation. Use when: (1) user exported or wants to export ChatGPT data, (2) user wants to organize/analyze/search their chat history, (3) user wants to build a personal memory archive or diary from conversations, (4) user asks to extract people/events/emotions/knowledge/timeline from ChatGPT, (5) user mentions conversations.json or ChatGPT data export, (6) user wants to migrate memories from ChatGPT to another system, (7) user wants a summary or review of their ChatGPT usage over time. Triggers on: 'organize my ChatGPT history', 'extract memories from ChatGPT', 'analyze my ChatGPT export', '整理ChatGPT对话', '导出ChatGPT数据', 'build memory from chats', 'what did I talk about with ChatGPT', 'review my ChatGPT conversations', 'make a timeline from my chats', 'ChatGPTのデータを整理'. NOT for: other AI chat exports (Claude/Gemini), real-time logging, or automated summarization without human review."
---

# ChatGPT Memory Extraction

Transform ChatGPT conversation exports into a structured personal memory archive.

## ⚠️ For Users

AI agents cut corners on large text volumes. Review each batch. Praise quality, not speed.

Read [quality rules](references/quality-rules.md) for ChatGPT-specific pitfalls and known AI failure modes.

## Workflow

1. **Prepare**: User exports ChatGPT data:
   - Go to ChatGPT → Settings → Data controls → Export data → Confirm export
   - OpenAI will send an email when the export is ready (may take **hours to days** depending on data size)
   - Download the zip file from the email link (requires being logged into ChatGPT)
   - Unzip to get `conversations-*.json` files and other data
2. **Extract**: Run `scripts/extract_conversations.py` to convert JSON → readable text files + conversation index
3. **Read & Write**: Process one quarter at a time. Read every conversation fully. Write timeline per [output-format.md](references/output-format.md). User reviews before proceeding. Split into monthly batches for 100+ conversations.
4. **Extract Dimensions**: Update people files and topic files. Every person mentioned → their file updated.
5. **Incremental**: On new exports, compare IDs, process only new content.

## Output Structure

See [output-format.md](references/output-format.md).
