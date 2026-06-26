---
name: array-url-extractor
description: Extract valid downloadable URLs from Array[String] structures, clean and standardize them, then output directly. 
---

# Array URL Extractor

Extract valid URLs from Array[String] structures, output directly without any additional text.

## Use Cases

Use when users need to "extract URLs from array", "extract download links", or "parse URLs in array".

## Workflow

### 1. Parse Array

Receive user-provided Array[String] structures (JSON arrays, code snippets, etc.).

### 2. Extract URLs

- Identify all valid URL addresses in the array (starting with `https://` or `http://`)
- Filter out invalid or non-URL strings
- Clean up encoding issues and special characters
- Standardize URL format

### 3. Output

Output URLs directly, one per line, without any additional text:

```
https://example.com/file1.jpg
https://example.com/file2.png
```

## Constraints

- Return URL addresses directly; do not add any other text
- Output should be concise and clear, ready for direct use
- Do not ask the user questions; process directly
- Only output valid, downloadable URLs