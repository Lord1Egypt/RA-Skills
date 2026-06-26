---
name: arxiv-survey
description: Survey arXiv papers from a given year to present on a specific theme. Automatically categorizes papers, translates abstracts to Chinese, and generates a structured markdown report.
---

# ArXiv Survey

Generate comprehensive survey reports on arXiv papers for a specific theme and time range.

## Usage

```bash
/skill arxiv-survey survey <year>:<theme>
```

### Parameters

- **year**: Starting year for paper collection (e.g., `2026`)
- **theme**: Topic or theme description (can be a short keyword or detailed description)

### Examples

```bash
/skill arxiv-survey survey 2026:AI 辅助开源贡献
/skill arxiv-survey survey 2024:RAG retrieval augmented generation
/skill arxiv-survey survey 2025:LLM code generation automated program repair
/skill arxiv-survey survey 2026:multimodal learning
```

## Workflow

1. **Search**: Query arXiv API for papers from `<year>` to present matching `<theme>`
2. **Filter**: Collect 10-50 relevant papers (more if the theme has abundant literature)
3. **Categorize**: Automatically classify papers into thematic categories based on titles and abstracts
4. **Translate**: Translate abstracts to fluent Chinese
5. **Generate Report**: Create a structured markdown file with:
   - **Table of Contents**: Categories with paper titles listed under each
   - **Detailed Content**: For each category, list papers with:
     - English title
     - Authors
     - Chinese translated abstract (expanded if full text is accessible)

## Output

Generates a markdown file: `arxiv-survey-<year>-<theme-slug>.md`

### Report Structure

```markdown
# ArXiv Survey: <Theme> (<Year>-Present)

## Table of Contents

### Category 1
- Paper Title 1
- Paper Title 2

### Category 2
- Paper Title 3

---

## Detailed Papers

### Category 1

#### Paper Title 1
**Authors**: Author List  
**arXiv**: [Link](https://arxiv.org/abs/xxxx.xxxxx)  
**Abstract (中文)**: Translated abstract...

#### Paper Title 2
...
```

## Scripts

- `scripts/survey_arxiv.sh <year> <theme>` - Main survey script that searches, categorizes, and generates the report

## Notes

- Paper count adapts to availability: niche topics may yield ~10 papers, popular topics up to 50
- Abstracts are translated to Chinese for readability
- If full paper content is accessible, abstracts may be expanded with additional context
- All file names are in English (no Chinese characters)
