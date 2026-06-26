#!/usr/bin/env bash
# aegis/scripts/setup-guardrails.sh — Auto-configure language-specific hard guardrails
# Usage: bash setup-guardrails.sh /path/to/project [--ci github|gitlab]
#
# Detects project stack and sets up:
# 1. Pre-commit hook (lint + type-check + format + contract validation)
# 2. CI pipeline config (GitHub Actions or GitLab CI)
# 3. Linter/formatter configs if not present

set -euo pipefail

PROJECT_PATH="${1:?Usage: setup-guardrails.sh <project-path> [--ci github|gitlab]}"
CI_PLATFORM="github"  # default
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Parse --ci flag
shift
while [[ $# -gt 0 ]]; do
  case $1 in
    --ci) CI_PLATFORM="$2"; shift 2 ;;
    *) shift ;;
  esac
done

echo "🛡️  Setting up Aegis hard guardrails in: $PROJECT_PATH"
echo ""

# --- Detect stack ---
STACK_JSON=$(bash "$SCRIPT_DIR/detect-stack.sh" "$PROJECT_PATH")
echo "📋 Detected stack:"
echo "$STACK_JSON" | head -10
echo ""

# Helper: check if language is in detected stack
has_lang() {
  echo "$STACK_JSON" | grep -q "\"$1\""
}

has_framework() {
  echo "$STACK_JSON" | grep -q "\"$1\""
}

# ============================================================
# PRE-COMMIT HOOK
# ============================================================
HOOK_DIR="$PROJECT_PATH/.git/hooks"
HOOK_FILE="$HOOK_DIR/pre-commit"

# Also create a portable copy in project root
HOOK_SCRIPT="$PROJECT_PATH/.aegis/pre-commit.sh"
mkdir -p "$PROJECT_PATH/.aegis"

HOOK_CONTENT="#!/usr/bin/env bash
# Aegis Pre-Commit Hook — auto-generated, language-adaptive
# Blocks commits that fail hard checks. Bypass with: git commit --no-verify
set -e

echo '🛡️  Aegis pre-commit checks...'
ERRORS=0
"

# --- TypeScript / JavaScript ---
if has_lang "typescript" || has_lang "javascript"; then
  # Detect package runner
  PKG_RUN="npx"
  if echo "$STACK_JSON" | grep -q '"pnpm"'; then PKG_RUN="pnpm exec"; fi
  if echo "$STACK_JSON" | grep -q '"bun"'; then PKG_RUN="bunx"; fi

  HOOK_CONTENT+="
# --- TypeScript / JavaScript ---
echo '  [JS/TS] Lint...'
$PKG_RUN eslint --max-warnings 0 . 2>/dev/null || { echo '❌ ESLint failed'; ERRORS=\$((ERRORS+1)); }
"

  if has_lang "typescript"; then
    HOOK_CONTENT+="
echo '  [TS] Type check...'
$PKG_RUN tsc --noEmit 2>/dev/null || { echo '❌ TypeScript type check failed'; ERRORS=\$((ERRORS+1)); }
"
  fi

  HOOK_CONTENT+="
echo '  [JS/TS] Format check...'
$PKG_RUN prettier --check . 2>/dev/null || { echo '❌ Prettier format check failed (run: $PKG_RUN prettier --write .)'; ERRORS=\$((ERRORS+1)); }
"

  # Write ESLint config if missing
  if [ ! -f "$PROJECT_PATH/.eslintrc.json" ] && [ ! -f "$PROJECT_PATH/.eslintrc.js" ] && [ ! -f "$PROJECT_PATH/eslint.config.js" ] && [ ! -f "$PROJECT_PATH/eslint.config.mjs" ]; then
    cat > "$PROJECT_PATH/eslint.config.mjs" << 'ESLINT_EOF'
import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    rules: {
      "no-unused-vars": "warn",
      "no-console": "warn",
      "prefer-const": "error",
      "no-var": "error",
    },
  },
  {
    ignores: ["node_modules/", "dist/", "build/", ".next/", "contracts/shared-types.ts"],
  },
];
ESLINT_EOF
    echo "  ✅ Created eslint.config.mjs"
  fi

  # Write Prettier config if missing
  if [ ! -f "$PROJECT_PATH/.prettierrc" ] && [ ! -f "$PROJECT_PATH/.prettierrc.json" ] && [ ! -f "$PROJECT_PATH/prettier.config.js" ]; then
    cat > "$PROJECT_PATH/.prettierrc" << 'PRETTIER_EOF'
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2
}
PRETTIER_EOF
    echo "  ✅ Created .prettierrc"
  fi
fi

# --- Go ---
if has_lang "go"; then
  HOOK_CONTENT+="
# --- Go ---
echo '  [Go] Vet...'
go vet ./... 2>/dev/null || { echo '❌ go vet failed'; ERRORS=\$((ERRORS+1)); }

echo '  [Go] Format check...'
GOFMT_OUTPUT=\$(gofmt -l . 2>/dev/null || true)
if [ -n \"\$GOFMT_OUTPUT\" ]; then
  echo '❌ gofmt: unformatted files:' \$GOFMT_OUTPUT
  ERRORS=\$((ERRORS+1))
fi
"

  # Check for golangci-lint
  HOOK_CONTENT+="
if command -v golangci-lint &>/dev/null; then
  echo '  [Go] Lint...'
  golangci-lint run ./... 2>/dev/null || { echo '❌ golangci-lint failed'; ERRORS=\$((ERRORS+1)); }
fi
"

  # Write golangci-lint config if missing
  if [ ! -f "$PROJECT_PATH/.golangci.yml" ] && [ ! -f "$PROJECT_PATH/.golangci.yaml" ]; then
    cat > "$PROJECT_PATH/.golangci.yml" << 'GOLINT_EOF'
run:
  timeout: 5m

linters:
  enable:
    - errcheck
    - govet
    - staticcheck
    - unused
    - gosimple
    - ineffassign
    - misspell
    - gofmt
    - goimports
    - revive

linters-settings:
  revive:
    rules:
      - name: exported
        severity: warning
      - name: var-naming
        severity: warning

issues:
  exclude-dirs:
    - vendor
    - node_modules
GOLINT_EOF
    echo "  ✅ Created .golangci.yml"
  fi
fi

# --- Python ---
if has_lang "python"; then
  HOOK_CONTENT+="
# --- Python ---
echo '  [Python] Lint...'
if command -v ruff &>/dev/null; then
  ruff check . 2>/dev/null || { echo '❌ ruff check failed'; ERRORS=\$((ERRORS+1)); }
  echo '  [Python] Format check...'
  ruff format --check . 2>/dev/null || { echo '❌ ruff format failed (run: ruff format .)'; ERRORS=\$((ERRORS+1)); }
elif command -v flake8 &>/dev/null; then
  flake8 . 2>/dev/null || { echo '❌ flake8 failed'; ERRORS=\$((ERRORS+1)); }
fi

if command -v mypy &>/dev/null; then
  echo '  [Python] Type check...'
  mypy . 2>/dev/null || { echo '⚠️  mypy type check has issues (non-blocking)'; }
fi
"

  # Write ruff config if missing
  if [ ! -f "$PROJECT_PATH/ruff.toml" ] && [ ! -f "$PROJECT_PATH/pyproject.toml" ] || ! grep -q "\[tool.ruff\]" "$PROJECT_PATH/pyproject.toml" 2>/dev/null; then
    if [ ! -f "$PROJECT_PATH/ruff.toml" ]; then
      cat > "$PROJECT_PATH/ruff.toml" << 'RUFF_EOF'
line-length = 100
target-version = "py311"

[lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM"]
ignore = ["E501"]  # line length handled by formatter

[format]
quote-style = "double"
RUFF_EOF
      echo "  ✅ Created ruff.toml"
    fi
  fi
fi

# --- Rust ---
if has_lang "rust"; then
  HOOK_CONTENT+="
# --- Rust ---
echo '  [Rust] Check...'
cargo check 2>/dev/null || { echo '❌ cargo check failed'; ERRORS=\$((ERRORS+1)); }

echo '  [Rust] Lint...'
cargo clippy -- -D warnings 2>/dev/null || { echo '❌ clippy failed'; ERRORS=\$((ERRORS+1)); }

echo '  [Rust] Format check...'
cargo fmt --check 2>/dev/null || { echo '❌ cargo fmt failed (run: cargo fmt)'; ERRORS=\$((ERRORS+1)); }
"
fi

# --- Contract validation (always, if contracts/ exists) ---
HOOK_CONTENT+="
# --- Aegis Contract Validation ---
if [ -d contracts/ ]; then
  echo '  [Aegis] Contract validation...'
  # Use project-local .aegis/ copy (portable) or fallback to validate inline
  VALIDATE_SCRIPT=\"\$(git rev-parse --show-toplevel 2>/dev/null)/.aegis/validate-contract.sh\"
  if [ -f \"\$VALIDATE_SCRIPT\" ]; then
    bash \"\$VALIDATE_SCRIPT\" \"\$(git rev-parse --show-toplevel)\" 2>/dev/null || { echo '❌ Contract validation failed'; ERRORS=\$((ERRORS+1)); }
  else
    echo '  ⚠️  .aegis/validate-contract.sh not found — run init-project.sh to install'
  fi
fi
"

# --- Final gate ---
HOOK_CONTENT+="
if [ \$ERRORS -gt 0 ]; then
  echo ''
  echo \"🛡️  Aegis blocked commit: \$ERRORS check(s) failed.\"
  echo '   Fix issues or bypass with: git commit --no-verify'
  exit 1
fi
echo '🛡️  All checks passed.'
"

# Write hook
echo "$HOOK_CONTENT" > "$HOOK_SCRIPT"
chmod +x "$HOOK_SCRIPT"
echo "  ✅ Created .aegis/pre-commit.sh"

# Install git hook if .git exists
if [ -d "$PROJECT_PATH/.git" ]; then
  mkdir -p "$HOOK_DIR"
  cp "$HOOK_SCRIPT" "$HOOK_FILE"
  chmod +x "$HOOK_FILE"
  echo "  ✅ Installed .git/hooks/pre-commit"
fi

# ============================================================
# CI PIPELINE
# ============================================================

if [ "$CI_PLATFORM" = "github" ]; then
  CI_DIR="$PROJECT_PATH/.github/workflows"
  CI_FILE="$CI_DIR/aegis-checks.yml"
  mkdir -p "$CI_DIR"

  cat > "$CI_FILE" << 'CI_HEADER'
name: "🛡️ Aegis Quality Gates"

on:
  push:
    branches: [main, develop, "feature/**"]
  pull_request:
    branches: [main, develop]

CI_HEADER

  # Add jobs based on detected languages
  echo "jobs:" >> "$CI_FILE"

  # --- TypeScript/JavaScript job ---
  if has_lang "typescript" || has_lang "javascript"; then
    PKG_MGR="npm"
    if echo "$STACK_JSON" | grep -q '"pnpm"'; then PKG_MGR="pnpm"; fi

    cat >> "$CI_FILE" << JSTS_EOF
  lint-typecheck-js:
    name: "JS/TS Lint + Type Check"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
JSTS_EOF

    if [ "$PKG_MGR" = "pnpm" ]; then
      cat >> "$CI_FILE" << 'PNPM_EOF'
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - run: pnpm install --frozen-lockfile
      - run: pnpm exec eslint --max-warnings 0 .
      - run: pnpm exec prettier --check .
PNPM_EOF
    else
      cat >> "$CI_FILE" << 'NPM_EOF'
      - run: npm ci
      - run: npx eslint --max-warnings 0 .
      - run: npx prettier --check .
NPM_EOF
    fi

    if has_lang "typescript"; then
      if [ "$PKG_MGR" = "pnpm" ]; then
        echo "      - run: pnpm exec tsc --noEmit" >> "$CI_FILE"
      else
        echo "      - run: npx tsc --noEmit" >> "$CI_FILE"
      fi
    fi
    echo "" >> "$CI_FILE"
  fi

  # --- Go job ---
  if has_lang "go"; then
    cat >> "$CI_FILE" << 'GO_EOF'
  lint-typecheck-go:
    name: "Go Lint + Vet"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: "1.22"
      - run: go vet ./...
      - run: test -z "$(gofmt -l .)"
      - uses: golangci/golangci-lint-action@v6
        with:
          version: latest
      - run: go test ./... -count=1

GO_EOF
  fi

  # --- Python job ---
  if has_lang "python"; then
    cat >> "$CI_FILE" << 'PY_EOF'
  lint-typecheck-python:
    name: "Python Lint + Format"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff
      - run: ruff check .
      - run: ruff format --check .

PY_EOF
  fi

  # --- Rust job ---
  if has_lang "rust"; then
    cat >> "$CI_FILE" << 'RUST_EOF'
  lint-typecheck-rust:
    name: "Rust Check + Clippy + Fmt"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      - run: cargo check
      - run: cargo clippy -- -D warnings
      - run: cargo fmt --check
      - run: cargo test

RUST_EOF
  fi

  # --- Contract validation job (always) ---
  cat >> "$CI_FILE" << 'CONTRACT_EOF'
  aegis-contract-validation:
    name: "🛡️ Aegis Contract Validation"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate contracts
        run: |
          if [ -d contracts/ ]; then
            echo "Validating Aegis contracts..."
            # Basic YAML syntax check
            for f in contracts/*.yaml contracts/*.yml; do
              [ -f "$f" ] || continue
              node -e "
                const fs = require('fs');
                const c = fs.readFileSync('$f','utf8');
                if (c.match(/^\t/m)) { console.error('Tab indent in $f'); process.exit(1); }
              " || exit 1
              echo "  ✅ $f syntax OK"
            done
            # JSON schema check
            for f in contracts/*.json; do
              [ -f "$f" ] || continue
              node -e "JSON.parse(require('fs').readFileSync('$f','utf8'))" || exit 1
              echo "  ✅ $f valid JSON"
            done
            # Check shared-types not redefined locally
            if [ -f contracts/shared-types.ts ] && [ -d src/ ]; then
              TYPES=$(grep -oP '(?<=export (interface|type) )\w+' contracts/shared-types.ts || true)
              for t in $TYPES; do
                if grep -rn "^\(export \)\?\(interface\|type\) $t\b" src/ | grep -v import | grep -v node_modules; then
                  echo "❌ Type '$t' from shared-types.ts is redefined in src/"
                  exit 1
                fi
              done
              echo "  ✅ No shared-type redefinitions"
            fi
            echo "🛡️ Contract validation passed"
          else
            echo "No contracts/ directory — skipping"
          fi
CONTRACT_EOF

  echo "  ✅ Created .github/workflows/aegis-checks.yml"

elif [ "$CI_PLATFORM" = "gitlab" ]; then
  CI_FILE="$PROJECT_PATH/.gitlab-ci-aegis.yml"

  cat > "$CI_FILE" << 'GL_HEADER'
# Aegis Quality Gates — include in main .gitlab-ci.yml
# include:
#   - local: '.gitlab-ci-aegis.yml'

stages:
  - aegis-lint
  - aegis-test

GL_HEADER

  if has_lang "go"; then
    cat >> "$CI_FILE" << 'GL_GO'
aegis-go-lint:
  stage: aegis-lint
  image: golang:1.22
  script:
    - go vet ./...
    - test -z "$(gofmt -l .)"
    - go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
    - golangci-lint run ./...

aegis-go-test:
  stage: aegis-test
  image: golang:1.22
  script:
    - go test ./... -count=1 -v

GL_GO
  fi

  if has_lang "typescript" || has_lang "javascript"; then
    # Detect package manager for GitLab CI
    GL_PKG_INSTALL="npm ci"
    GL_PKG_RUN="npx"
    if echo "$STACK_JSON" | grep -q '"pnpm"'; then
      GL_PKG_INSTALL="corepack enable && pnpm install --frozen-lockfile"
      GL_PKG_RUN="pnpm exec"
    elif echo "$STACK_JSON" | grep -q '"yarn"'; then
      GL_PKG_INSTALL="corepack enable && yarn install --immutable"
      GL_PKG_RUN="yarn"
    fi

    cat >> "$CI_FILE" << GL_JS_EOF
aegis-js-lint:
  stage: aegis-lint
  image: node:20
  script:
    - $GL_PKG_INSTALL
    - $GL_PKG_RUN eslint --max-warnings 0 .
    - $GL_PKG_RUN prettier --check .
GL_JS_EOF

    if has_lang "typescript"; then
      echo "    - $GL_PKG_RUN tsc --noEmit" >> "$CI_FILE"
    fi
    echo "" >> "$CI_FILE"
  fi

  if has_lang "python"; then
    cat >> "$CI_FILE" << 'GL_PY'
aegis-python-lint:
  stage: aegis-lint
  image: python:3.12
  script:
    - pip install ruff
    - ruff check .
    - ruff format --check .

GL_PY
  fi

  cat >> "$CI_FILE" << 'GL_CONTRACT'
aegis-contract-validation:
  stage: aegis-lint
  image: node:20
  script:
    - |
      if [ -d contracts/ ]; then
        for f in contracts/*.yaml contracts/*.yml; do
          [ -f "$f" ] || continue
          node -e "const fs=require('fs'); const c=fs.readFileSync('$f','utf8'); if(c.match(/^\t/m)){process.exit(1)}"
          echo "✅ $f OK"
        done
        for f in contracts/*.json; do
          [ -f "$f" ] || continue
          node -e "JSON.parse(require('fs').readFileSync('$f','utf8'))"
          echo "✅ $f OK"
        done
        echo "🛡️ Contracts validated"
      fi
  rules:
    - exists:
        - contracts/**/*

GL_CONTRACT

  echo "  ✅ Created .gitlab-ci-aegis.yml"
fi

echo ""
echo "🛡️  Guardrails setup complete!"
echo ""
echo "Installed:"
echo "  - Pre-commit hook (.aegis/pre-commit.sh + .git/hooks/pre-commit)"
echo "  - CI pipeline ($CI_PLATFORM)"
echo "  - Language-specific linter/formatter configs"
echo ""
echo "To bypass pre-commit (emergency only): git commit --no-verify"
