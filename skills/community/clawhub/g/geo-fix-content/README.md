# geo-fix-content

Rewrite website content to maximize AI citability — paragraph-level diagnosis with before/after rewrites.

## What it does

1. **Scans** every paragraph for 6 citability issue categories
2. **Measures** Hedge Density (target: < 0.5%)
3. **Rewrites** problem paragraphs with before/after comparison
4. **Explains** what changed and why for each rewrite
5. **Outputs** full rewritten content ready to copy-paste

## Issue Categories

| Category | What it catches |
|----------|----------------|
| Hedge Language | maybe, possibly, seems, tends to, generally... |
| Missing Data | Claims without metrics, vague comparisons |
| Missing Definitions | Unexplained jargon and acronyms |
| Poor Self-Containment | Paragraphs that can't stand alone |
| Structural Issues | Long paragraphs, prose that should be lists |
| Weak Answer Blocks | Questions without direct answers |

## Usage

```bash
# Analyze a URL
"Fix the content citability for https://example.com/blog/post"

# Analyze pasted text
"Improve this content for AI citability: [paste text]"

# Claude Code slash command
/geo-fix-content https://example.com/blog/post
```

## Output

| File | Purpose |
|------|---------|
| `content-fix-{domain}-{date}.md` | Before/after rewrites + full rewritten content |

## Installation

```bash
npx skills add Cognitic-Labs/geoskills --skill geo-fix-content
```
