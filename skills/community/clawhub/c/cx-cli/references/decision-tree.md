# cx Decision Tree

Quick decision guide for when and how to use cx.

```
START: Need to understand code?
│
├─ YES → Is it a supported language? (Rust/TS/Python/Go/C/C++/Java/Ruby/Lua/Zig/Bash/Solidity/Elixir)
│   │
│   ├─ NO → Use `read` tool directly
│   │
│   └─ YES → What's your goal?
│       │
│       ├─ Understand file structure → `cx overview <file>`
│       │   └─ Need specific symbol? → `cx definition --name <X>`
│       │
│       ├─ Find symbol across project → `cx symbols [--kind K] [--name GLOB]`
│       │   └─ Found it? → `cx definition --name <X> --from <file>`
│       │
│       ├─ Before editing/refactoring → `cx references --name <X>`
│       │   └─ See impact? → Proceed with edit
│       │
│       └─ After context compression → `cx overview <file>` to re-orient
│
└─ NO → Do you need full file context? (imports, comments, non-code)
    │
    ├─ YES → Use `read` tool
    │
    └─ NO → Are you editing the file?
        │
        ├─ YES → Use `read` + `edit` tools
        │
        └─ NO → Use `grep` or `web_search` for text patterns
```

## Quick Lookup Table

| Your Situation | First Command | Next Step |
|----------------|---------------|-----------|
| "What's in this file?" | `cx overview file.py` | `cx definition --name <X>` |
| "Where is X defined?" | `cx symbols --name "*X*"` | `cx definition --name X --from <file>` |
| "Who calls X?" | `cx references --name X` | Read each call site if needed |
| "How does this module work?" | `cx symbols --file module.py` | `cx definition` for key functions |
| "Is this function used?" | `cx references --name func` | Check each reference |
| "What's the entry point?" | `cx symbols --name "main"` | `cx definition --name main` |

## Error Recovery Flow

```
cx command fails
│
├─ "unsupported file type" → File is .md/.yaml/.json → Use `read`
│
├─ "database locked" → Wait 2-3s → Retry → `cx cache clean` if persistent
│
├─ "file not in index" → File outside git root? → Move inside or use `read`
│
├─ "symbol not found" → Try glob: `cx symbols --name "*partial*"`
│
└─ "missing grammar" → `cx lang add <language>`
```
