---
name: code-explainer-tool
description: Explain any code snippet or file in plain English. Paste code → get a clear explanation of what it does, how it works, and key concepts. Use when the user shares code and wants to understand it, learn from it, or review it.
---

# Code Explainer

Transform code into plain-English explanations. Perfect for learning, reviewing, or understanding unfamiliar code.

## Usage

```
explain this code
what does this do?
explain: [paste code]
```

## How it works

1. Analyzes code structure and syntax
2. Identifies key operations and patterns
3. Explains in plain English with technical accuracy
4. Highlights important concepts and potential issues

## Supported Languages

All major languages supported:
- Python, JavaScript, TypeScript
- Go, Rust, Java, C/C++, C#
- Ruby, PHP, Swift, Kotlin
- SQL, Shell/Bash, YAML, JSON
- And more...

## Output Format

- **Summary**: What the code does
- **Breakdown**: Step-by-step explanation
- **Key Concepts**: Important patterns/techniques used
- **Notes**: Warnings, best practices, or improvements

## Script

```python
python scripts/explain_code.py <path/to/file>
```

Or pipe code:

```
cat myfile.py | python scripts/explain_code.py -
```