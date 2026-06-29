# cx Output Examples

Real output samples from actual commands to help agents understand what to expect.

## cx symbols --json

```json
[
  {
    "file": "skills/folio/scripts/stealth_upload.py",
    "name": "main",
    "kind": "fn",
    "signature": "def main()"
  }
]
```

## cx definition

```
file: skills/folio/scripts/stealth_upload.py
line: 13
---
def main():
    parser = argparse.ArgumentParser(description="Folio Stealth Upload Script")
    parser.add_argument("--file", required=True, help="Path to the file to upload")
    # ... function body
```

## cx references

```
[2]{file,line,kind,context}:
  skills/folio/scripts/stealth_upload.py,13,function_definition,"def main():"
  skills/folio/scripts/stealth_upload.py,87,call,main()
```

## cx overview (TypeScript)

```
[12]{name,kind,signature}:
  "src/index.ts",module,""
  "main",fn,"async function main()"
  "Config",interface,"interface Config"
  "handleError",fn,"function handleError(err: Error): never"
```

## Output Format Notes

- Default format is **TOON** (compact, line-based)
- Use `--json` for machine-parseable JSON output
- Line numbers are 1-indexed
- File paths are relative to project root (git root)
