---
slug: cn-json-diff
name: JSON Diff
version: "1.0.0"
description: "Compare two JSON files and show differences. Support nested structures, arrays, and value changes. Pure Python standard library, no API key required."
keywords: json, diff, compare, difference, file
license: MIT-0
tags:
  - tools
---

# JSON Diff

Compare two JSON files and show the differences in a clear format.

## Features

- Compare JSON files of any complexity
- Detect nested object differences
- Identify array length changes
- Show old vs new values for changed fields
- Pure Python, no external dependencies

## Input

Two JSON files passed as arguments.

## Output

List of all differences found, with paths and old/new values.

## Usage

```
python3 scripts/json_diff.py --file1 data1.json --file2 data2.json
```

## Example

Input file1.json:
```json
{"name": "Alice", "age": 30, "city": "Beijing"}
```

Input file2.json:
```json
{"name": "Alice", "age": 31, "city": "Shanghai"}
```

Output:
```
differences:
- age: 30 -> 31
- city: Beijing -> Shanghai
count: 2
```

## Exit Codes

- 0: Comparison completed (with or without differences)
- 1: File read error

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
