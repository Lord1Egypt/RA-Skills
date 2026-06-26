# Skill: Academic Translator & Research Assistant

**Trigger:** User provides a PDF file, arxiv link/ID, or asks to translate/analyze an academic paper.

## Overview

Professional academic translation agent for CS papers. Translates papers (EN↔ZH), answers questions with combined paper content + web research.

## Workflow

### 1. Paper Ingestion

**From arxiv link/ID:**
```bash
source /home/kjp/.openclaw/workspace/.venv/bin/activate
python {SKILL_DIR}/fetch_arxiv.py "<arxiv_url_or_id>" /tmp/arxiv_papers
```
Returns JSON with metadata (title, authors, abstract, pdf_path). Use this to:
- Show the user a brief summary first
- Then extract full text from the downloaded PDF

**From PDF file (uploaded or local path):**
```bash
source /home/kjp/.openclaw/workspace/.venv/bin/activate
python {SKILL_DIR}/extract_pdf.py "<path_to_pdf>" [max_pages]
```
Returns JSON with page-by-page text. Omit `max_pages` for full extraction.

### 2. Translation

After extracting paper text, translate using these principles:

**Translation Guidelines:**
- **术语一致性**: Maintain consistent technical terminology throughout. First occurrence should include original English term in parentheses, e.g. "注意力机制 (Attention Mechanism)"
- **保留专有名词**: Model names (GPT, BERT, Transformer), dataset names, benchmark names stay in English
- **数学公式**: Keep LaTeX/math notation as-is, only translate surrounding explanation text
- **图表引用**: "Figure 1" → "图1", "Table 2" → "表2", "Equation 3" → "公式(3)"
- **学术风格**: Use formal academic Chinese (学术书面语), avoid colloquial expressions
- **结构保留**: Maintain paper structure: Abstract(摘要), Introduction(引言), Related Work(相关工作), Method(方法), Experiments(实验), Conclusion(结论)

**Translation Output Format:**
```
# [翻译标题]
**原标题:** [Original Title]
**作者:** [Authors]
**来源:** [arxiv ID / conference / journal]

## 摘要
[Translated abstract]

## 1 引言
[Translated content...]
...
```

### 3. Research & Q&A

When the user asks questions about the paper:

1. **First** search the extracted paper content for relevant sections
2. **Then** use `web_search` for supplementary context:
   - Related papers and citations
   - Blog posts / explanations of key concepts
   - Implementation details (GitHub repos)
   - Latest developments on the topic
3. **Synthesize** an answer combining paper content + web findings
4. **Cite sources** clearly: page numbers for paper content, URLs for web sources

### 4. Capabilities

| Command | Action |
|---------|--------|
| "翻译这篇论文" / "translate this paper" | Full paper translation |
| "翻译摘要/引言/第N节" | Translate specific section |
| "总结这篇论文" / "summarize" | Generate structured summary |
| "解释 [concept]" | Explain a concept from the paper with web context |
| "[any question]" | Answer based on paper + web research |
| "对比 [paper A] 和 [paper B]" | Compare two papers |

### 5. Summary Format

When summarizing, use this structure:

```
## 📄 论文概览
**标题:** ...
**核心贡献:** 1-2 sentences
**关键词:** ...

## 🎯 主要贡献
1. ...
2. ...

## 🔬 方法概述
[Concise method description]

## 📊 实验结果
[Key results and comparisons]

## 💡 核心洞察
[Why this matters, limitations, future directions]
```

## State Management

Store paper context in `/tmp/academic_papers/` for multi-turn conversations:
- `/tmp/academic_papers/current_paper.json` — metadata of current paper
- `/tmp/academic_papers/current_text.txt` — extracted full text

This allows follow-up questions without re-extracting.

## Notes

- For very long papers (>30 pages), extract and translate in batches
- Always show paper metadata first before diving into translation
- Use `web_search` proactively for unfamiliar terms or cutting-edge topics
- Default translation direction: English → Chinese (unless user specifies otherwise)
- Use sub-agents (`sessions_spawn`) for full paper translation to avoid blocking the main session
