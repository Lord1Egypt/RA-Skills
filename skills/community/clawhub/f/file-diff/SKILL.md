---
name: file-diff
description: Compare two files and display their differences in a human-readable markdown format. Use when asked to "compare files", "show diff", "compare differences", "diff two files", or any request to analyze file differences. Triggers on phrases like "比较文件"、"比较异同"、"diff"、"show me the differences".
---

# File Diff

Compare two files and display differences in a clean, readable markdown format.

## Usage

### Quick Compare (Two file paths)

```bash
diff <source_file> <target_file>
```

### Unified Diff Format (Recommended)

```bash
diff -u <source_file> <target_file>
```

## Output Format

The diff output is formatted as:

```markdown
**File A**: `/path/to/file1`
**File B**: `/path/to/file2`

## Differences

### 1. [Section/Line description]
```diff
- removed line
+ added line
```
```

## Workflow

1. Identify the two files to compare
2. Run `diff -u` command
3. Parse the unified diff output
4. Format into readable markdown with:
   - File paths as headers
   - Line numbers from diff output
   - `-` prefix for removals (red)
   - `+` prefix for additions (green)
   - Context lines for clarity

## Example

Input:
```bash
diff -u /tmp/original.txt /tmp/modified.txt
```

Output format:
```
**File A**: `/tmp/original.txt`
**File B**: `/tmp/modified.txt`

## Differences

### Line 5
```diff
- old content
+ new content
```
```

## Notes

- Always use `-u` flag for unified format (more readable)
- Include both file paths in the output
- Preserve all changes including additions, deletions, and modifications
