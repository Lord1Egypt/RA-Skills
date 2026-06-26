---
name: format-tool
description: Format and beautify text output for better readability. Use for cleaning up structured data and aligning columns.
---
# Format - Text Formatting Utility
Format text with configurable alignment, padding, and column spacing. Transforms raw output into readable tables and structured displays.
## Usage
```bash
format-tool [options] [file...]
```
## Features
- Column alignment (left, right, center)
- Custom padding and separators
- JSON and CSV input support
- Pipe input compatible
## Examples
```bash
format-tool --align center data.txt
echo "col1,col2,col3" | format-tool --csv --table
```