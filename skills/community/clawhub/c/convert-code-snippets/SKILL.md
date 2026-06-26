---
name: convert-code-snippets
description: >
  Use when (1) user provides a code snippet and asks to convert it from one programming language to another (e.g., Python to JavaScript, Java to Kotlin). (2) user asks to transform code between representations (e.g., JSON schema to TypeScript types, Markdown table to CSV). (3) user provides code in one style/convention and wants it converted to another (e.g., CommonJS to ESM, callback to async/await).
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

## Core Position

This skill converts **code snippets and data structures** between programming languages, formats, and conventions. It handles syntactic transformation (language-to-language), representational transformation (JSON to TypeScript types), and stylistic transformation (older patterns to newer ones). It does NOT just copy-paste — it applies semantic equivalence, meaning the output code must be functionally equivalent to the input.

Key responsibilities:
- Detect the source and target languages from file extensions or explicit annotation
- Apply language-specific syntax rules (indentation, semicolons, keyword differences, standard library equivalents)
- Handle language idioms — not just syntax replacement, but idiomatic transformation
- Preserve comments and docstrings where possible, or mark them as needing manual review
- Validate that the output is syntactically correct in the target language

## Modes

### `/convert-code-snippets --language`
**Language-to-language conversion.** Converts code from source language to target language. Requires `--from` and `--to` flags:
```
--from python --to javascript
--from java --to kotlin
--from go --to rust
--from typescript --to python
```
Supported languages: Python, JavaScript, TypeScript, Java, Kotlin, Go, Rust, C++, C#, Swift, Ruby, PHP.

### `/convert-code-snippets --schema`
**Schema to code conversion.** Converts a data schema (JSON Schema, OpenAPI, SQL schema) into typed code:
- `JSON Schema` → TypeScript interfaces, Python dataclasses, Java classes, Go structs
- `OpenAPI spec` → client code (TypeScript, Python), server stubs
- `SQL CREATE TABLE` → ORM models (SQLAlchemy, TypeORM, Prisma)

### `/convert-code-snippets --style`
**Code style transformation.** Converts code between conventions:
- `callback-to-async` — converts callback-based code to async/await
- `class-to-function` — converts class-based OOP to functional style
- `commonjs-to-esm` — converts `require()` to `import`/`export`
- `python2-to-python3` — converts Python 2 print statements, unicode handling
- `jsx-to-tsx` — converts JavaScript JSX to TypeScript TSX

### `/convert-code-snippets --format`
**Data format conversion.** Converts between structured data formats:
- `json-to-yaml`, `yaml-to-json`, `toml-to-json`
- `csv-to-json`, `json-to-csv`, `tsv-to-csv`
- `xml-to-json`, `json-to-xml`

## Execution Steps

1. **Detect source and target language/format**


**From file extension:**
```
.py  → Python     .js  → JavaScript   .java → Java
.ts  → TypeScript .kt  → Kotlin       .go   → Go
.rs  → Rust       .cpp → C++          .cs   → C#
.swift → Swift   .rb  → Ruby         .php  → PHP
.tsx → TypeScript .jsx → JavaScript   .json → JSON
.yaml → YAML      .yml → YAML        .toml → TOML
.csv → CSV        .xml → XML          .sql  → SQL
```

**From content (if extension ambiguous):**
- Python: `def `, `import `, `print(` → Python
- JavaScript: `function `, `const `, `let `, `=>` → JavaScript
- Java: `public class `, `System.out.` → Java
- TypeScript: `: string`, `: number`, `interface ` → TypeScript

If source or target is ambiguous, ask the user: "Cannot determine target language — please specify `--from python --to javascript` explicitly."

2. **Parse and analyze source code**


Read the source code as UTF-8 text. Use a parser if available for the source language:
- Python: `ast` module to parse into AST
- JavaScript/TypeScript: `esprima` or `babel parser`
- Java: use a simple regex-based approach if full parser unavailable

For languages without parser support, use structural pattern matching:
- Identify functions/methods: pattern `def name(` or `function name(`
- Identify classes: pattern `class Name` or `class Name extends`
- Identify imports: pattern `import ` or `from ` or `require(`
- Identify type annotations: pattern `: Type` or `-> Type`

Extract: function signatures, class definitions, imports, type annotations, comments.

3. **Map language constructs**


Build a transformation map for the specific language pair. Common mappings:

**Python → JavaScript:**
```
def fn(x, y)          →  function fn(x, y) {
print(x)              →  console.log(x)
None                  →  null
True / False          →  true / false
x if cond else y      →  cond ? x : y
with open(f) as f:    →  (async () => { const fs = require('fs'); ... })()
def __init__(self):   →  constructor() {
self.x                →  this.x
f"string {x}"         →  `string ${x}`
[x for x in lst]      →  lst.map(x => x)
```
**Python → TypeScript:** (above + type annotations)
```
int, float, str       →  number, number, string
List[int]             →  number[]
Dict[str, int]        →  Record<string, number>
Optional[int]         →  number | null
def fn() -> int       →  function fn(): number
```

**Java → Kotlin:**
```
System.out.println()  →  println()
public class          →  class (public is default)
String                →  String (kotlin.String)
final                 →  val
void method()         →  fun method(): Unit
if (x == null)        →  if (x == null)
```

**Callback → Async/Await:**
```
// Before (callback style)
apiCall(arg, function(err, result) {
  if (err) return handleError(err);
  process(result);
});

// After (async/await)
try {
  const result = await apiCall(arg);
  process(result);
} catch (err) {
  handleError(err);
}
```

**CommonJS → ESM:**
```
const fs = require('fs');                  →  import fs from 'fs';
const {a, b} = require('./module');        →  import {a, b} from './module.js';
module.exports = {fn};                     →  export const fn = ...;
module.exports.fn = fn;                    →  export function fn() {...}
```

4. **Apply formatting rules**


**Indentation:**
- Detect current indentation (tabs, 2-space, 4-space) from first indented line
- Preserve or convert based on `--indent` flag (default: 2 spaces for most languages)

**Semicolons:**
- JavaScript/TypeScript: add `;` at end of statement (unless already present or line ends with `{`/`}`)
- Python: remove `;` if present

**Quotes:**
- Prefer single quotes in Python, backticks in JavaScript template literals
- Convert double-quoted strings with no special chars to single quotes in Python

**Imports/exports:**
- Group imports: stdlib, third-party, local (separated by blank lines)
- Sort alphabetically within groups
- Remove unused imports

5. **Validate output**


For parsed languages, attempt to parse the output:
- Python: `ast.parse(output)` — if it fails, report the error with line number
- JavaScript: run `eslint --no-eslintrc --parser-options {ecmaVersion: 2020} filename.js` if available

If no parser available, do structural validation:
- Balanced braces `{...}`, brackets `[...]`, parentheses `(...)`
- No unclosed strings (detect by scanning for string delimiters)
- Keywords in correct case (`function` not `Function`, `const` not `CONST`)

If validation fails, report: "Converted code is invalid [target language]: error at line {N}: {detail}. Reverting to source format."

6. **Report transformation summary**


Return:
```json
{
  "source_language": "python",
  "target_language": "javascript",
  "lines_converted": 142,
  "functions_mapped": 8,
  "classes_mapped": 3,
  "imports_mapped": 12,
  "comments_preserved": 7,
  "warnings": [
    {"line": 42, "issue": "Python dict comprehension has no direct JS equivalent — converted to .map() but verify correctness"},
    {"line": 87, "issue": "Decorator @property cannot be represented in ES5 — needs manual conversion"}
  ],
  "approximate_functional_equivalence": "85%"
}
```

## Mandatory Rules

### Do not

- Do not perform literal search-replace without understanding semantics (e.g., Python `is` vs JavaScript `===`)
- Do not convert language-specific standard library calls without substituting the equivalent (e.g., `System.out.println()` must become `console.log()`, not just stay as-is)
- Do not drop type annotations in `--schema` mode — TypeScript/Java/Kotlin output must have types
- Do not silently skip functions or classes — every top-level definition must appear in output (even if as stub requiring manual completion)
- Do not convert code that uses a library/framework not available in the target ecosystem without warning
- Do not preserve inline comments that reference source-language-specific constructs (e.g., `# self` in Python → `// self` in JavaScript — remove or update)

### Do

- Report `approximate_functional_equivalence` percentage and list specific areas needing manual review
- Map standard library functions (e.g., Python `len()` → JS `.length`, Python `str()` → JS `String()`)
- Preserve comments when they document behavior, not implementation details
- In `--style` mode, add a comment `// Auto-converted from [source style] — verify correctness` at the top
- Detect and flag language-specific features that cannot be directly converted (decorators, metaclasses, generators, async generators)
- Use the target language's idiomatic patterns, not just syntactic translation

## Quality Bar

| Criterion | Minimum | Ideal |
|-----------|---------|-------|
| Syntax validity | Output parses without error in target language | Output passes linter with no warnings |
| Semantic equivalence | Approximate functional equivalence >= 70% | >= 90% with manual review only for complex features |
| Standard library mapping | All detected stdlib calls mapped to target equivalent | Verified by running converted code against test cases |
| Type preservation | Type annotations preserved where possible | Full type inference in target language |
| Comment preservation | Comments that document behavior preserved | Comments translated, not just copied |
| Edge case handling | Handles null, empty input gracefully | All edge cases have explicit handling with test cases |

A good output is syntactically valid in the target language, semantically equivalent to the source (with known gaps documented), and formatted according to the target language's conventions.

## Good vs. Bad Examples

| Scenario | Bad | Good |
|---------|-----|------|
| Python `is` to JS | Replaces `is` with `===` literally | Maps `is` to `===` for primitives but warns about object identity difference |
| `len(list)` in Python | Writes `len(list)` in JS (not valid) | Converts to `list.length` |
| `def fn(a, b=None)` | Converts to `function fn(a, b=null)` (loses default intent) | Adds `if (b === undefined) b = null` or uses default parameter `b = null` |
| Python f-string | Converts `f"{x}"` to `"${x}"` (wrong in non-template context) | Detects f-string, converts to template literal `` `${x}` `` |
| Java `for` loop | Converts `for (int i=0; i<n; i++)` to `for i in range(n):` (Pythonic but not equivalent) | Preserves index-based loop or maps to `for i in range(n)` with note |
| Missing import | Silently drops `import os` | Maps to `const os = require('os')` (Node) or reports "os module has no direct JS equivalent" |
| Callback to async | Converts only one level of callbacks | Recursively converts nested callbacks to async/await, flattening the chain |
| Unknown construct | Skips the function entirely | Includes function signature as comment: `// function unknownFeature() — needs manual implementation` |