---
name: code-formatter
description: Code formatting best practices and quick references for Python, JavaScript, JSON, Markdown, and common languages with Prettier, Black, ESLint, and other formatters. Use when needing to format code, configure linters, or set up code style guidelines.
---

# Code Formatter & Style Guide

Quick references for code formatting tools and style best practices.

---

## 🐍 Python Formatting

### Black (Opinionated Formatter)
```bash
# Install
pip install black

# Format file
black file.py

# Format directory
black src/

# Check without modifying
black --check file.py

# Configuration (pyproject.toml)
[tool.black]
line-length = 88
target-version = ['py310']
```

### isort (Import Sorting)
```bash
# Install
pip install isort

# Sort imports
isort file.py
isort src/

# Black-compatible config
[tool.isort]
profile = "black"
```

### flake8 (Linting)
```bash
# Install
pip install flake8

# Lint
flake8 file.py
flake8 src/

# Config (setup.cfg)
[flake8]
max-line-length = 88
extend-ignore = E203, W503
```

### ruff (Fast Linter & Formatter)
```bash
# Install
pip install ruff

# Lint
ruff check file.py

# Fix automatically
ruff check --fix file.py

# Format
ruff format file.py
```

---

## 💛 JavaScript/TypeScript Formatting

### Prettier
```bash
# Install
npm install -D prettier

# Format
npx prettier --write file.js
npx prettier --write src/

# Check
npx prettier --check file.js

# Config (.prettierrc)
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80
}

# Ignore (.prettierignore)
node_modules/
build/
dist/
```

### ESLint
```bash
# Install
npm install -D eslint

# Initialize
npx eslint --init

# Lint
npx eslint file.js
npx eslint src/

# Fix
npx eslint --fix file.js

# Config (.eslintrc.js)
module.exports = {
  extends: ['eslint:recommended'],
  parserOptions: { ecmaVersion: 2022 },
  rules: {
    'no-unused-vars': 'warn',
    'no-console': 'warn'
  }
}
```

### Format on Save (VS Code)
```json
// settings.json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

---

## 📋 JSON Formatting

### jq
```bash
# Pretty print JSON
jq '.' file.json

# Compact (one line)
jq -c '.' file.json

# Sort keys
jq -S '.' file.json
```

### Prettier for JSON
```bash
npx prettier --write file.json
npx prettier --write *.json
```

### Python json.tool
```bash
python3 -m json.tool file.json
python3 -m json.tool file.json --sort-keys
```

---

## 📝 Markdown Formatting

### Prettier
```bash
npx prettier --write README.md
npx prettier --write docs/
```

### markdownlint
```bash
# Install
npm install -D markdownlint-cli

# Lint
npx markdownlint README.md
npx markdownlint docs/

# Fix
npx markdownlint --fix README.md
```

### Common Rules
- Line length: 80-120 chars
- ATX headers: `# Header` not `Header =====`
- Consistent list indentation (2 spaces)
- One blank line between sections
- Trailing whitespace removal

---

## 🔧 EditorConfig (Cross-Editor)

Create `.editorconfig` in project root:
```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[*.{json,yml,yaml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

---

## 🚀 Quick Format Commands

| Language | Tool | Command |
|----------|------|---------|
| Python | black | `black file.py` |
| Python | ruff | `ruff format file.py` |
| JS/TS | Prettier | `npx prettier --write file.js` |
| JSON | jq | `jq '.' file.json` |
| Markdown | Prettier | `npx prettier --write README.md` |
| Shell | shfmt | `shfmt -w script.sh` |
| Go | gofmt | `gofmt -w file.go` |
| Rust | rustfmt | `rustfmt file.rs` |

---

## 💡 Best Practices

1. **Commit config files**: `.prettierrc`, `.eslintrc`, `pyproject.toml`, `.editorconfig`
2. **Format on save**: Set up your editor to auto-format
3. **Pre-commit hooks**: Use `pre-commit` or `husky` to enforce
4. **Consistency**: Pick one style and stick to it
5. **CI checks**: Run formatters/lint in CI pipeline

### Pre-commit Setup (.pre-commit-config.yaml)
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0-alpha.8
    hooks:
      - id: prettier
```
