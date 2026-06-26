---
name: docx-footnote-reader
description: "Extract footnotes, endnotes, and body text from .docx files using Node.js. Use this skill when you need to read footnote/endnote content from Word documents, such as technical specifications, legal documents, or academic papers."
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX Footnote Reader

## Overview

A skill for extracting footnotes, endnotes, and body text from Microsoft Word (.docx) files. This is particularly useful for:
- Technical documentation with reference notes
- Legal documents with citations
- Academic papers with footnoted references
- Any document where footnote content is important

## Usage

### Command Line

```bash
node index.js path/to/document.docx
```

### Programmatic API

```javascript
const { extractFootnotes } = require('docx-footnote-reader');

const result = await extractFootnotes('./document.docx');

console.log(`Body: ${result.body.length} characters`);
console.log(`Footnotes: ${result.footnotes.length} notes`);
console.log(`Endnotes: ${result.endnotes.length} notes`);

// Access individual footnotes
result.footnotes.forEach((note, idx) => {
  console.log(`Footnote ${idx + 1}: ${note}`);
});
```

## Return Value

The `extractFootnotes` function returns a Promise that resolves to:

```typescript
{
  body: string;           // Document body text
  footnotes: string[];    // Array of footnote strings
  endnotes: string[];     // Array of endnote strings
}
```

## How It Works

1. Uses `word-extractor` library to parse the .docx file
2. Extracts body text via `doc.getBody()`
3. Extracts footnotes via `doc.getFootnotes()` - handles both string and array return types
4. Extracts endnotes via `doc.getEndnotes()` - handles both string and array return types
5. Splits footnote/endnote strings by newline and filters empty entries

## Important Notes

- The `word-extractor` library returns footnotes as a **single string separated by newlines**, not an array
- This skill automatically handles both string and array return types
- Empty footnotes/endnotes are filtered out
- Each footnote string is trimmed of whitespace

## Dependencies

- Node.js >= 14
- word-extractor (automatically installed via npm)

## Installation

```bash
cd docx-footnote-reader
npm install
```

## Example Output

```
========================================
Extraction Result
========================================

Body length: 58057 characters

Footnotes count: 73

Footnotes:

Footnote 1:
Description about error injection in this document, if the context does not mention single-frame multi-bit or Burst, it refers to single-bit error injection.

Footnote 2:
This feature is only supported on PG2K100 devices.

...
```

## Troubleshooting

### "Cannot find module 'word-extractor'"
Run `npm install` in the skill directory.

### Empty footnotes array
- Check that the document actually contains footnotes
- Verify the file path is correct
- Try opening the document in Word to confirm footnotes exist

### Footnotes merged into one string
This is expected behavior from `word-extractor`. This skill automatically splits them by newlines.

## File Structure

```
docx-footnote-reader/
├── index.js        # Main extraction logic
├── package.json    # npm dependencies
├── SKILL.md        # This file
└── LICENSE.txt     # License terms
```
