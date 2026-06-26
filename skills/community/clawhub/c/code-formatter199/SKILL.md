---
name: code-formatter
description: "Format Python, JavaScript, TypeScript, JSON, HTML, CSS, and Go code snippets"
version: 1.1.0
author: hahg199
tags:
  - code
  - formatter
  - python
  - javascript
  - typescript
  - json
  - html
  - css
  - go
---

## Description
This skill takes raw, poorly indented code and returns a nicely formatted, readable version following community standard style guides. It supports multiple languages and provides clear error messages when language is not recognized or code is invalid.

## Supported Languages & Style Rules
- **Python**: PEP 8 – 4 spaces per indentation level; no unnecessary blank lines; single quotes preferred.
- **JavaScript (JS)**: 2 spaces per level; semicolons optional but consistent; `{` on same line.
- **TypeScript (TS)**: same as JavaScript, plus explicit return types for functions when possible.
- **JSON**: 2 spaces; no trailing commas; no comments; keys in double quotes.
- **HTML**: 2 spaces per level; inline elements should not be broken across lines; self-closing tags for void elements.
- **CSS**: 2 spaces; one selector per line; opening brace on same line; space after colon.
- **Go**: use `gofmt` style – tabs for indentation (width 8); no extra spaces; consistent formatting.

## Instructions
When the user provides a code snippet and specifies (or implies) a language:

1. **Detect or ask for language** if not provided. Supported: python, javascript, typescript, json, html, css, go.
2. **Check for syntax errors** – if the code is clearly invalid (e.g., unmatched braces, missing quotes), inform the user and suggest correction before formatting.
3. **Apply the corresponding style rules** from above.
4. **Output the formatted code inside a Markdown code block** with the correct language identifier.
5. **Add a brief explanation** of what changes were made (e.g., "Added 2-space indentation and fixed spacing after commas").

If the language is not supported, respond with: "Sorry, I don't support formatting for {language} yet. Supported languages: python, javascript, typescript, json, html, css, go."

## Examples

### Example 1: Python
**User:** "Format this Python: def hello():print('world')"
**AI:** 
```python
def hello():
    print('world')