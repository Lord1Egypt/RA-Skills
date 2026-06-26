---
name: markdown-formatter
description: Formats and lints markdown files for consistency.
version: 1.0.0
---

## What it does

Reads markdown files and fixes formatting issues like inconsistent headings, trailing whitespace, and missing blank lines.

## Example

```javascript
const lines = content.split('\n');
const formatted = lines.map(line => line.trimEnd()).join('\n');
```
