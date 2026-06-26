---
name: cut-tool
description: Extract specific fields or columns from text files using delimiter-based parsing. Use when you need to select columns from CSV, TSV, or delimited data.
---

# Cut Tool - Field Extraction

Extract columns and fields from delimited text files by specifying delimiter and field position. Ideal for processing log files, CSV data, and structured text.

## Quick Start

```bash
cut-tool -d ',' -f 1,3 data.csv
```

## Features

- Extract fields by position (-f 1,3,5)
- Custom delimiter (-d for comma, tab, space)
- Complement selection (everything except specified fields)
- Output range of characters (-c 1-10)

## Examples

```bash
# Extract first and third columns from CSV
cut-tool -d ',' -f 1,3 data.csv

# Extract characters 1-10 from each line
cut-tool -c 1-10 file.txt

# Use tab as delimiter
cut-tool -f 2-4 file.tsv
```
