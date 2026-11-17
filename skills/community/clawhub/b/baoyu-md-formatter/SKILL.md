---
name: baoyu-md-formatter
slug: baoyu-md-formatter
displayName: "Baoyu Format Markdow"
version: "1.117.2"
summary: "格式化纯文本与Markdown,补frontmatter/标题/摘要/列表"
description: "格式化纯文本与Markdown,补frontmatter/标题/摘要/列表。Formats plain text or markdown files with frontmatter, titles, summaries,。触发关键词: files, format, text, baoyu, plain, formats, markdown。 功能涵盖: formatter。"
license: "MIT-0"
tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Baoyu Format Markdown

Transforms plain text or markdown into well-structured, reader-friendly markdown. The goal is to help readers quickly grasp key points, highlights, and structure — without changing any original content.

**Core principle**: Only adjust formatting and fix obvious typos. Never add, delete, or rewrite content.

## User Input Tools

When this skill prompts the user, follow this tool-selection rule (priority order):

1. **Prefer built-in user-input tools** exposed by the current agent runtime — e.g., `AskUserQuestion`, `request_user_input`, `clarify`, `ask_user`, or any equivalent.
2. **Fallback**: if no such tool exists, emit a numbered plain-text message and ask the user to reply with the chosen number/answer for each question.
3. **Batching**: if the tool supports multiple questions per call, combine all applicable questions into a single call; if only single-question, ask them one at a time in priority order.

Concrete `AskUserQuestion` references below are examples — substitute the local equivalent in other runtimes.

## Script Directory

Scripts in `scripts/` subdirectory. `{baseDir}` = this SKILL.md's directory path. Resolve `${BUN_X}` runtime: if `bun` installed → `bun`; if `npx` available → `npx -y bun`; else suggest installing bun. Replace `{baseDir}` and `${BUN_X}` with actual values.

| Script | Purpose |
| --- | --- |
| `scripts/main.ts` | Main entry point with CLI options (uses remark-cjk-friendly for CJK emphasis) |
| `scripts/quotes.ts` | Replace ASCII quotes with fullwidth quotes |
| `scripts/autocorrect.ts` | Add CJK/English spacing via autocorrect |

## Preferences (EXTEND.md)

Check EXTEND.md in priority order — the first one found wins:

| Priority | Path | Scope |
| --- | --- | --- |
| 1 | `.baoyu-skills/baoyu-format-markdown/EXTEND.md` | Project |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-format-markdown/EXTEND.md` | XDG |
| 3 | `$HOME/.md` | User home |

If none found, use defaults — no first-time setup required for this skill.

**EXTEND.md supports**:

| Setting | Values | Default | Description |
| --- | --- | --- | --- |
| `auto_select` | `true`/`false` | `false` | Skip both title and summary selection, auto-pick best |
| `auto_select_title` | `true`/`false` | `false` | Skip title selection only |
| `auto_select_summary` | `true`/`false` | `false` | Skip summary selection only |
| Other | — | — | Default formatting options, typography preferences |

## Usage

The workflow has two phases: **Analyze** (understand the content) then **Format** (apply formatting).  performs content analysis and formatting (Steps 1-5), then runs the script for typography fixes (Step 6).

## Workflow

### Step 1: Read & Detect Content Type

Read the user-specified file, then detect content type:

| Indicator | Classification |
| --- | --- |
| Has `---` YAML frontmatter | Markdown |
| Has `#`, `##`, `###` headings | Markdown |
| Has `**bold**`, `*italic*`, lists, code blocks, blockquotes | Markdown |
| None of above | Plain text |

**If Markdown detected, use `AskUserQuestion` to ask:**

```text
Detected existing markdown formatting. What would you like to do?

1. Optimize formatting (Recommended)
   - Analyze content, improve headings, bold, lists for readability
   - Run typography script (spacing, emphasis fixes)
   - Output: {filename}-formatted.md

2. Keep original formatting
   - Preserve existing markdown structure
   - Run typography script only

3. Typography fixes only
   - Run typography script on original file in-place
   - No copy created, modifies original file directly
```

**基于 user choice:**

* **Optimize**: Continue to Step 2 (full workflow)
* **Keep original**: Skip to Step 5, copy file then run Step 6
* **Typography only**: Skip to Step 6, run on original file directly

### Step 2: Analyze Content (Reader's Perspective)

Read the entire content carefully. Think from a reader's perspective: what would help them quickly understand and remember the key information?

Produce an analysis covering these dimensions:

**2.1 Highlights & Key Insights**

* Core arguments or conclusions the author makes
* Surprising facts, data points, or counterintuitive claims
* Memorable quotes or well-phrased sentences (golden quotes)

**2.2 Structure Assessment**

* Does the content have a clear logical flow? What is it?
* Are there natural section boundaries that lack headings?
* Are there long walls of text that could benefit from visual breaks?

**2.3 Reader-Important Information**

* Actionable advice or takeaways
* Definitions, explanations of key concepts
* Lists or enumerations buried in prose
* Comparisons or contrasts that would be clearer as tables

**2.4 Formatting Issues**

* Missing or inconsistent heading hierarchy
* Paragraphs that mix multiple topics
* Parallel items written as prose instead of lists
* Code, commands, or technical terms not marked as code
* Obvious typos or formatting errors

**Save analysis to file**: `{original-filename}-analysis.md`

The analysis file serves as the blueprint for Step 3. Use this format:

```markdown

## Highlights & Key Insights
- [list findings]

## Structure Assessment
- Current flow: [describe]
- Suggested sections: [list heading candidates with brief rationale]

## Reader-Important Information
- [list actionable items, key concepts, buried lists, potential tables]

## Formatting Issues
- [list specific issues with location references]

## Typos Found
- [list any obvious typos with corrections, or "None found"]
```

### Step 3: Check/Create Frontmatter, Title & Summary

Check for YAML frontmatter (`---` block). Create if missing.

| Field | Processing |
| --- | --- |
| `title` | See **Title Generation** below |
| `slug` | Infer from file path or generate from title |
| `summary` | One-sentence concise summary (see **Summary Generation** below) |
| `description` | Longer descriptive summary (see **Summary Generation** below) |
| `coverImage` | Check if `imgs/cover.png` exists in same directory; if so, use relative path |

#
### Title Generation

Whether or not a title already exists, run the title optimization flow unless `auto_select_title` is set.

**Preparation** — read the full text and extract:

* Core argument (one sentence: "what is this article about?")
* Most impactful opinion or conclusion
* Reader pain point or curiosity trigger
* Most memorable metaphor or golden quote

**Generate candidates** using formulas from `references/title-formulas.md`:

1. Select the **2-3 best-matching hook formulas** 基于 the article's content, tone, and structure (see "When to pick each formula" in the reference)
2. Generate **1-2 straightforward titles** (descriptive or declarative, no formula — clear and accurate)
3. If the user specifies a direction (e.g., "make it suspenseful"), prioritize that direction
4. Total: **4-5 candidates**

Present via `AskUserQuestion`:

```text
Pick a title:

1. [Hook title A] — (recommended) [formula name]
2. [Hook title B] — [formula name]
3. [Hook title C] — [formula name]
4. [Straightforward title D] — straightforward
5. [Straightforward title E] — straightforward

Enter number, or type a custom title:
```

Put the strongest hook first and mark it `(recommended)`. See `references/title-formulas.md` for principles and prohibited patterns.

If the first line is an H1, extract it to frontmatter and remove it from the body. If frontmatter already has a `title`, include it as context but still generate fresh candidates — the existing title may be weak.

**Skip behavior**: If `auto_select: true` or `auto_select_title: true`, skip the user prompt and use the top candidate directly.

#
### Summary Generation

Generate two versions directly (no user selection), both stored in frontmatter:

| Field | Length | Purpose |
| --- | --- | --- |
| `summary` | 1 sentence, ~50-80 chars | Concise hook — for feeds, social sharing, SEO meta |
| `description` | 2-3 sentences, ~100-200 chars | Richer context — for article previews, newsletter blurbs |

**Principles**:

* Convey **core value** to the reader, not just the topic
* Use concrete details (numbers, outcomes, specific methods) over vague descriptions
* `summary` should be punchy and self-contained; `description` can expand with supporting details
* If frontmatter already has `summary` or `description`, keep the existing one and only generate the missing field

**Prohibited patterns**:

* "This article introduces...", "This article explores..."
* Pure topic description without value proposition
* Repeating the title in different words

Once the title is in frontmatter, the body should NOT contain an H1 (avoid duplication).

### Step 4: Format Content

Apply formatting guided by the Step 2 analysis. The goal is making the content scannable and the key points impossible to miss.

**Formatting toolkit:**

| Element | When to use | Format |
| --- | --- | --- |
| Headings | Natural topic boundaries, section breaks | `##`, `###` hierarchy |
| Bold | Key conclusions, important terms, core takeaways | `**bold**` |
| Unordered lists | Parallel items, feature lists, examples | `- item` |
| Ordered lists | Sequential steps, ranked items, procedures | `1. item` |
| Tables | Comparisons, structured data, option matrices | Markdown table |
| Code | Commands, file paths, technical terms, variable names | `` `inline` `` or fenced blocks |
| Blockquotes | Notable quotes, important warnings, cited text | `> quote` |
| Separators | Major topic transitions | `---` |

**Formatting principles — what NOT to do:**

* Do NOT add sentences, explanations, or commentary
* Do NOT delete or shorten any content
* Do NOT rephrase or rewrite the author's words
* Do NOT add headings that editorialize (e.g., "Amazing Discovery" — use neutral descriptive headings)
* Do NOT over-format: not every sentence needs bold, not every paragraph needs a heading

**Formatting principles — what TO do:**

* Preserve the author's voice, tone, and every word
* **Bold key conclusions and core takeaways** — the sentences a reader would highlight
* Extract parallel items from prose into lists only when the structure is clearly there
* Add headings where the topic genuinely shifts — prefer vivid, specific headings over generic ones (e.g., "3 天搞定 vs 传统方案" over "方案对比")
* Use tables for comparisons or structured data buried in prose
* Use blockquotes for golden quotes, memorable statements, or important warnings
* Fix obvious typos (基于 Step 2 findings)

### Step 5: Save Formatted File

Save as `{original-filename}-formatted.md`

**Backup existing file:**

```bash
if [ -f "{filename}-formatted.md" ]; then
  mv "{filename}-formatted.md" "{filename}-formatted.backup-$(date +%Y%m%d-%H%M%S).md"
fi
```

### Step 6: Execute Typography Script

Run the formatting script on the output file:

```bash
${BUN_X} {baseDir}/scripts/main.ts {output-file-path} [options]
```

**Script Options:**

| Option | Short | Description | Default |
| --- | --- | --- | --- |
| `--quotes` | `-q` | Replace ASCII quotes with fullwidth quotes `"..."` | false |
| `--no-quotes` |  | Do not replace quotes |  |
| `--spacing` | `-s` | Add CJK/English spacing via autocorrect | true |
| `--no-spacing` |  | Do not add CJK/English spacing |  |
| `--emphasis` | `-e` | Fix CJK emphasis punctuation issues | true |
| `--no-emphasis` |  | Do not fix CJK emphasis issues |  |

**Examples:**

```bash

ts article.md --quotes

ts article.md --no-spacing
```

**Script performs (基于 options):**

1. Fix CJK emphasis/bold punctuation issues (default: enabled)
2. Add CJK/English mixed text spacing via autocorrect (default: enabled)
3. Replace ASCII quotes with fullwidth quotes (default: disabled)
4. Format frontmatter YAML (always enabled)

### Step 7: Completion Report

Display a report summarizing all changes made:

```text
**Formatting Complete**

**Files:**
- Analysis: {filename}-analysis.md
- Formatted: {filename}-formatted.md

**Content Analysis Summary:**
- Highlights found: X key insights
- Golden quotes: X memorable sentences
- Formatting issues fixed: X items

**Changes Applied:**
- Frontmatter: 
- Headings added: X (##: N, ###: N)
- Bold markers added: X
- Lists created: X (from prose → list conversion)
- Tables created: X
- Code markers added: X
- Blockquotes added: X
- Typos fixed: X [list each: "original" → "corrected"]

**Typography Script:**
- CJK spacing: [applied/skipped]
- Emphasis fixes: [applied/skipped]
- Quote replacement: [applied/skipped]
```

Adjust the report to reflect actual changes — omit categories where no changes were made.

## Notes

* Preserve original writing style and tone
* Specify correct language for code blocks (e.g., `python`, `javascript`)
* Maintain CJK/English spacing standards
* The analysis file is a working document — it helps maintain consistency between what was identified and what was formatted

## Extension Support

Custom configurations via EXTEND.md. See **Preferences** section for paths and supported options.

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent( Code / Cursor / Codex /  CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行任务

## 核心能力

- Formats plain text or markdown files with frontmatter, titles, summaries,
  headings, bold, lists,
- 触发关键词: files, format, text, baoyu, plain, formats, markdown

## 适用场景

| 场景 | 输入 | 输出 |
|------|------|------|
| 基础使用 | 用户请求 | 处理结果 |

**不适用于**：需要人工判断的复杂决策场景

## 使用流程

1. 确认运行环境满足依赖说明中的要求
2. 根据适用场景选择合适的使用方式
3. 执行操作并检查输出结果
4. 如遇错误，参考错误处理章节

## 示例

### 示例1：基础用法

```
# 请参考上方使用说明进行配置和调用
result = "ready"
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 检查网络连接后重试，参考国内替代方案 |

## 常见问题

### Q1: 如何开始使用Baoyu Format Markdow？
A: 请先阅读使用流程章节，确认环境满足依赖说明中的要求。

### Q2: 遇到错误怎么办？
A: 请参考错误处理章节，按照表格中的处理方式操作。

### Q3: Baoyu Format Markdow有什么限制？
A: 请参考已知限制章节了解具体限制。

## 已知限制

- 需要LLM支持，无LLM环境无法使用
- 复杂场景可能需要人工辅助判断
- 性能取决于底层模型能力

---
## 边界条件与限制

### 输入限制
- **文件格式**：仅支持纯文本文件和Markdown文件。
- **内容长度**：没有明确的长度限制，但非常长的文件可能会影响处理速度。
- **文件编码**：推荐使用UTF-8编码，其他编码可能需要手动转换。

### 性能边界
- **处理速度**：对于中等长度的文件，处理时间通常在几秒到几十秒之间。
- **并发处理**：不支持同时处理多个文件，每次只能处理一个文件。

### 兼容性约束
- **操作系统**：在所有主流操作系统上运行，包括Windows、macOS和Linux。
- **Agent平台**：仅支持与SKILL.md兼容的AI Agent，如 Code、Cursor、Codex、 CLI等。
- **Markdown版本**：兼容标准的Markdown语法，但不支持所有Markdown扩展或特定平台的Markdown方言。

### 其他限制
- **内容敏感度**：不适用于包含敏感内容或非法营销手段的文件。
- **语言支持**：主要支持中英文内容，对其他语言的格式化效果可能不理想。
- **自定义配置**：虽然支持EXTEND.md文件进行自定义配置，但配置选项有限，且可能需要一定的Markdown和SKILL.md知识。

---
