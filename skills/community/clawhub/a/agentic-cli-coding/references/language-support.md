# Language Support Matrix

What works out of the box, what needs project-local tooling, and what's best-effort.

## Legend

- ✅ **Native** — Works with just the bundled toolkit (Node + acorn + js-yaml).
- 🟡 **Local tool** — Requires the language's tool to be on PATH or in `./node_modules/.bin/`.
- 🟢 **Best-effort** — A weaker check runs if no real validator is available; gross syntax errors caught.
- ❌ **Not validated** — Files of this type are accepted as-is; rely on project tooling.

## Matrix

| Language | File | Read/Edit | Syntax Validate | Format | AST Edit |
|---|---|---|---|---|---|
| JavaScript | `.js .mjs .cjs` | ✅ | ✅ `node --check` | 🟡 prettier | ✅ acorn |
| JSX | `.jsx` | ✅ | ✅ `node --check` | 🟡 prettier | ✅ acorn |
| TypeScript | `.ts` | ✅ | 🟡 `tsc` → 🟢 acorn | 🟡 prettier | 🟢 partial |
| TSX | `.tsx` | ✅ | 🟡 `tsc` → 🟢 acorn | 🟡 prettier | 🟢 partial |
| Vue SFC | `.vue` | ✅ | ❌ (use vue-tsc) | 🟡 prettier | ❌ |
| Svelte | `.svelte` | ✅ | ❌ (use svelte-check) | 🟡 prettier | ❌ |
| JSON | `.json` | ✅ | ✅ `JSON.parse` | 🟡 prettier | ❌ |
| YAML | `.yaml .yml` | ✅ | ✅ js-yaml | 🟡 prettier | ❌ |
| TOML | `.toml` | ✅ | ❌ | ❌ | ❌ |
| XML | `.xml` | ✅ | ❌ | ❌ | ❌ |
| HTML | `.html .htm` | ✅ | 🟢 bracket balance | 🟡 prettier | ❌ |
| CSS | `.css` | ✅ | ❌ | 🟡 prettier | ❌ |
| SCSS/Sass | `.scss .sass` | ✅ | ❌ | 🟡 prettier | ❌ |
| LESS | `.less` | ✅ | ❌ | 🟡 prettier | ❌ |
| Markdown | `.md .mdx` | ✅ | ❌ | 🟡 prettier | ❌ |
| Python | `.py` | ✅ | 🟡 `python3 -m py_compile` | 🟡 black, ruff | ❌ |
| Ruby | `.rb` | ✅ | 🟡 `ruby -c` | 🟡 rubocop | ❌ |
| Go | `.go` | ✅ | 🟡 `gofmt -e` | 🟡 gofmt | ❌ |
| Rust | `.rs` | ✅ | 🟡 `rustfmt --check` | 🟡 rustfmt | ❌ |
| Java | `.java` | ✅ | ❌ (use compiler) | ❌ | ❌ |
| Kotlin | `.kt .kts` | ✅ | ❌ | ❌ | ❌ |
| Swift | `.swift` | ✅ | ❌ | ❌ | ❌ |
| C / C++ | `.c .h .cpp .hpp` | ✅ | ❌ (use compiler) | ❌ | ❌ |
| C# | `.cs` | ✅ | ❌ | ❌ | ❌ |
| PHP | `.php` | ✅ | 🟡 `php -l` | 🟡 php-cs-fixer | ❌ |
| Bash / Zsh | `.sh .bash .zsh` | ✅ | ✅ `bash -n` | ❌ | ❌ |
| SQL | `.sql` | ✅ | ❌ | ❌ | ❌ |
| Dockerfile | `Dockerfile` | ✅ | ❌ | ❌ | ❌ |
| Makefile | `Makefile` | ✅ | ❌ | ❌ | ❌ |

## What "validation" actually checks

The auto-validation that runs after every edit is **syntax-only**, not type-checking or linting. Specifically:

- **`node --check`** — Catches parse errors. Does not catch undefined variables, type errors, or runtime errors.
- **`JSON.parse`** — Strict JSON. Comments, trailing commas, single quotes all fail.
- **`js-yaml`** — Standard YAML 1.2 with safe schema.
- **`bash -n`** — Catches syntax errors, not unset variables or quoting issues.
- **`python3 -m py_compile`** — Catches indentation and parse errors. Imports are not resolved.
- **`tsc --noEmit`** — When available, this is the strongest check: full type-checking with project's `tsconfig.json`.

If validation passes, your edit's syntax is correct. If validation fails, the edit is rolled back. **Validation passing does not guarantee the edit is logically correct** — that requires running the project's tests.

## When `oce ast` works on TypeScript

The bundled acorn parser handles standard JavaScript including ES2024 syntax. On TypeScript files, it works for the JS subset:

✅ Works:
- `function foo()`, `class Foo`, arrow functions, async/await
- `import` / `export` statements (ES module syntax)
- Decorators (with `acornOptions: { allowDecorators: true }` — the default)

❌ Won't parse (use text-based edits instead):
- Type annotations on parameters: `function foo(x: number)` 
- Generics: `function foo<T>()` 
- `interface`, `type`, `namespace`, `enum`
- TS-specific syntax like `as const`, `satisfies`, non-null assertions

For full TS support, install `typescript` locally so `tsc --noEmit` is available — it'll be used automatically.

## Adding language support

The skill's language detection lives in `lib/common.sh` (function `detect_language`). To add a new language:

1. Add the extension(s) to `detect_language`.
2. Add a case branch in `scripts/oce-validate.sh` if a syntax checker exists.
3. Add a case branch in `scripts/oce-format.sh` if a formatter exists.
4. Test by creating a file of that type and running `oce validate <file>`.

Do not add validators that require network access, since this runs in agent contexts that may have no internet.
