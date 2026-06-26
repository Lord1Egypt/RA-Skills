# Gemini Worker — Prompt Patterns

Reusable templates for common agent tasks. All patterns assume headless execution via
`gemini -p "$(cat /tmp/prompt.txt)" --yolo --include-directories ...`.

---

## Anthropic Fallback Pattern

Drop-in replacement when Anthropic returns 529. Use this when your main model is unavailable.

```
You are a senior [role — engineer / analyst / reviewer].

This task was delegated to you because the primary AI service is temporarily unavailable.
Apply the same quality standards you would expect from the primary agent.

## Task
[Paste the task that was going to claude-sonnet or claude-opus]

## Files you need
[List exact paths]

## Output
Write your complete response to: /tmp/gemini-output/result.md
Then print a 10-line summary to stdout.
```

**Usage:**
```bash
mkdir -p /tmp/gemini-output
cat > /tmp/fallback-prompt.txt << 'PROMPT'
You are a senior TypeScript engineer.
...
PROMPT

timeout 600 gemini \
  --include-directories /path/to/project,/tmp/gemini-output \
  --yolo \
  -p "$(cat /tmp/fallback-prompt.txt)"
```

---

## Validation / Review Pattern

For code review, spec compliance checks, audit tasks. Read-only.

```
You are a [senior role]. This is a READ-ONLY task — do NOT modify any source files.

## Documents to analyze
/path/to/file1.md
/path/to/file2.ts
/path/to/spec.md

## Checklist
1. [criterion 1]
2. [criterion 2]
3. [criterion 3]

## Output
Write your full report to: /path/to/output-report.md
Include: PASS/FAIL verdict, specific line references, recommended fixes.
Then print a SHORT summary (max 20 lines) to stdout.
```

---

## Dev Agent Pattern

For code generation, feature implementation, refactoring. Mimics a Claude Code task.

```
You are a senior software engineer implementing a feature.

## Spec
Read the full specification at: /path/to/spec.md

## Codebase context
Read these files before writing any code:
- /path/to/repo/src/relevant-file.ts
- /path/to/repo/src/types.ts

## Task
Implement [feature name] as described in the spec.

## Constraints
- Follow existing code style (read existing files first)
- Do NOT delete or modify existing tests
- Add JSDoc comments to new public functions
- Keep changes minimal — only what's needed for the feature

## Output
1. Write implementation to: /path/to/repo/src/feature.ts
2. Write tests to: /path/to/repo/src/feature.test.ts
3. Write a summary of what you did to: /tmp/dev-summary.md
Print the summary to stdout when done.
```

---

## File-Write Pattern

When you want structured output in a file (not stdout). Use this to avoid stdout truncation
for large outputs.

```
[Your task description here]

## Important: Write all output to files
Do NOT try to print large content to stdout — it will be truncated.

Instead:
1. Write your complete response to: /tmp/gemini-results/output.md
2. If you generate code: write each file to its correct path
3. Print only a short completion message to stdout (max 5 lines)

Confirm when done by printing: "✅ Done. Results at /tmp/gemini-results/output.md"
```

**Setup:**
```bash
mkdir -p /tmp/gemini-results
# Run Gemini, check /tmp/gemini-results/ for output
```

---

## Deep Analysis Pattern

For large codebase analysis, architecture review, security audit.

```
You are a technical analyst with access to the full codebase.
This is a READ-ONLY analysis task.

## Context files
Read everything under: /path/to/repo/src

## Task
Analyze [what] and answer:
1. [question 1]
2. [question 2]
3. [question 3]

## Output
Write a structured markdown report to: /path/to/analysis-result.md

Sections to include:
- Executive Summary (5 lines max)
- Detailed Findings (one section per question)
- Recommendations (prioritized)
```

---

## Batch Processing Pattern

For processing lists of items, one at a time, with output per item.

```
Process each item in the list below.

For each item:
1. Read the file at /path/to/items/{item}.json
2. Apply transformation: [description]
3. Write result to /path/to/output/{item}-result.json

Items: item1, item2, item3, item4, item5

After processing all items, write a summary to /path/to/batch-summary.md:
- How many processed successfully
- Any errors or skipped items
- Total items

Print "Batch complete: N/M processed" to stdout when done.
```

---

## Code Review Pattern

For PR review before merging.

```
You are a senior engineer reviewing a pull request.

## Changed files (read these)
/path/to/repo/src/changed-file1.ts
/path/to/repo/src/changed-file2.ts

## Spec this PR implements
/path/to/spec.md

## Review criteria
- Correctness vs spec
- Edge cases not handled
- Missing or incomplete tests
- Performance issues
- Security concerns
- Code style consistency

## Output
Write review to: /path/to/pr-review.md

Include:
- Verdict: LGTM / NEEDS CHANGES / BLOCKING
- Summary paragraph
- Line-level comments (file:line — comment)
- Optional: suggested code snippets for fixes

Print verdict + 3-line summary to stdout.
```

---

## Pre-fetch Helper

Gemini CLI's WebFetchTool is unreliable in headless mode. Pre-fetch web content with `curl`:

```bash
# Pre-fetch docs to a file Gemini can read
curl -sL https://example.com/api-docs \
  | python3 -c "
from html.parser import HTMLParser
import sys

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer'}
        self.current_skip = False
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.current_skip = True
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.current_skip = False
    def handle_data(self, data):
        if not self.current_skip and data.strip():
            self.texts.append(data.strip())

p = TextExtractor()
p.feed(sys.stdin.read())
print('\n'.join(p.texts[:500]))
" > /tmp/fetched-doc.txt

# Then run Gemini with access to /tmp
gemini \
  --include-directories /tmp \
  --yolo \
  -p "Read /tmp/fetched-doc.txt and write a TypeScript SDK for this API to /tmp/sdk.ts"
```
