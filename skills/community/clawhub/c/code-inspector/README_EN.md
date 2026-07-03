# code-inspector

AI-generated code quality detection tool — signature-based AI code smell detector.

## Features

Automatically detects 8 common quality issues in AI-generated code:

| Detection Type | Severity | Description |
|---------------|----------|-------------|
| **Truncation** | 🔴 Critical | LLM output truncation markers like `// ...`, `# ...`, `# rest of the code` |
| **Thinking Leak** | 🟡 Warning | LLM thinking process leaked into comments, e.g. `// Let me`, `# First,`, `# Now,` |
| **Hardcoded Secrets** | 🔴 Critical | API keys, tokens, passwords hardcoded in source |
| **Missing Error Handling** | 🟡 Warning | File operations, network calls without try/except blocks |
| **TODO Bomb** | 🟡 Warning | More than 3 TODO/FIXME/HACK markers in a file |
| **Copy-Paste** | 🟡 Warning | Repeated identical code blocks (>5 lines) |
| **Incomplete Imports** | 🔵 Info | Using functions/variables that may not be imported (e.g., `pd`, `np`) |
| **Bare Except** | 🟡 Warning | `except:` without specifying exception type |

## Quick Start

### Installation

```bash
pip install -e .
```

### Usage

```bash
# Check a single file
code-inspector check app.py

# Scan a directory recursively
code-inspector scan ./src

# View aggregate statistics
code-inspector stats ./project
```

### Sample Output

```
╭───────────────── Code Inspector ─────────────────╮
│ app.py  |  Language: Python                       │
╰───────────────────────────────────────────────────╯
Quality Score: ████████████████░░░░ 80/100

╭──────────────────── Smells Found: 2 ────────────────────╮
│ # │ Line │ Severity  │ Type           │ Description     │
├───┼──────┼───────────┼────────────────┼─────────────────┤
│ 1 │  42  │ 🔴 critical │ hardcoded_secret│ API key hardcoded │
│ 2 │  15  │ 🟡 warning  │ todo_bomb      │ TODO markers >3 │
╰──────────────────────────────────────────────────────────╯
```

## Supported Languages

- Python (`.py`)
- JavaScript (`.js`)
- TypeScript (`.ts`)

## Quality Scoring

Each file starts at 100, with deductions per detected smell:

- Truncation: -20
- Hardcoded Secret: -25
- Thinking Leak: -15
- Copy-Paste: -12
- Missing Error Handling: -10
- Incomplete Import: -10
- TODO Bomb: -8
- Bare Except: -7

## License

MIT License
