#!/usr/bin/env bash
# =============================================================================
# audit-script-engineering.sh
# Machine-verified consistency checks for software engineering projects.
# Run before Step 10 (Audit) in the build-protocol-engineering workflow.
#
# Usage:
#   chmod +x audit-script-engineering.sh
#   ./audit-script-engineering.sh [project-root]
#
# Exit code:
#   0 = all checks passed (or only warnings)
#   1 = one or more 🔴 BLOCKER found — deploy is blocked
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${1:-.}"
ERRORS=0
WARNINGS=0

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log_ok()      { echo -e "${GREEN}  ✅ $1${NC}"; }
log_warn()    { echo -e "${YELLOW}  ⚠️  WARN: $1${NC}"; ((WARNINGS+=1)); }
log_error()   { echo -e "${RED}  🔴 BLOCKER: $1${NC}"; ((ERRORS+=1)); }
section()     { echo; echo "=== $1 ==="; }

cd "$PROJECT_ROOT"

# =============================================================================
# LAYER 1 — NAMING CONSISTENCY
# =============================================================================

section "Layer 1: Naming Consistency"

# --- 1a. Env var names: .env.example ↔ config/*.ts ↔ docker-compose.yml ↔ k8s configmap ---

if [ -f ".env.example" ]; then
  ENV_KEYS=$(grep -E "^[A-Z_]+=?" .env.example | sed 's/=.*//' | sort)

  # Check config/*.ts (look for process.env.VARNAME)
  if ls config/*.ts 2>/dev/null | head -1 > /dev/null; then
    CONFIG_KEYS=$(grep -roh 'process\.env\.[A-Z_]*' config/*.ts 2>/dev/null \
      | sed 's/process\.env\.//' | sort -u)
    MISSING_IN_CONFIG=$(comm -23 <(echo "$ENV_KEYS") <(echo "$CONFIG_KEYS"))
    if [ -n "$MISSING_IN_CONFIG" ]; then
      log_warn "Env vars in .env.example not referenced in config/*.ts:\n$MISSING_IN_CONFIG"
    else
      log_ok ".env.example vars all referenced in config/*.ts"
    fi
  else
    log_warn "No config/*.ts found — skipping .env.example ↔ config check"
  fi

  # Check docker-compose.yml
  if [ -f "docker-compose.yml" ]; then
    COMPOSE_KEYS=$(grep -oh '\${[A-Z_]*}' docker-compose.yml 2>/dev/null \
      | tr -d '${}' | sort -u)
    MISSING_IN_COMPOSE=$(comm -23 <(echo "$ENV_KEYS") <(echo "$COMPOSE_KEYS") 2>/dev/null || true)
    if [ -n "$MISSING_IN_COMPOSE" ]; then
      log_warn "Some env vars from .env.example not in docker-compose.yml — may be intentional"
    else
      log_ok "docker-compose.yml references match .env.example"
    fi
  fi

else
  log_warn "No .env.example found — skipping env var consistency check"
fi

# --- 1b. k8s ConfigMap env vars ---
if ls k8s/*.yaml k8s/*.yml 2>/dev/null | head -1 > /dev/null; then
  K8S_KEYS=$(grep -roh 'name: [A-Z_]*' k8s/ 2>/dev/null | sed 's/name: //' | sort -u)
  if [ -f ".env.example" ]; then
    MISSING_K8S=$(comm -23 <(echo "$ENV_KEYS") <(echo "$K8S_KEYS") 2>/dev/null || true)
    if [ -n "$MISSING_K8S" ]; then
      log_warn "Env vars in .env.example missing from k8s manifests:\n$MISSING_K8S"
    else
      log_ok "k8s ConfigMap env vars match .env.example"
    fi
  fi
fi


# =============================================================================
# LAYER 2 — BUSINESS CONSISTENCY
# =============================================================================

section "Layer 2: Business Consistency"

# --- 2a. API paths: backend routes ↔ frontend fetch calls ---

if [ -d "src" ]; then
  # Extract backend route definitions (common patterns: Express, Hono, Fastify)
  BACKEND_ROUTES=$(grep -roh "\"\/[a-z/:-]*\"" src/ 2>/dev/null \
    | grep -v node_modules \
    | grep -v ".test." \
    | tr -d '"' | sort -u || true)

  # Extract frontend fetch/axios calls
  FRONTEND_CALLS=$(grep -roh "fetch(\`[^'\"]*\`\|['\"][\/][a-z/:-]*['\"]" src/ 2>/dev/null \
    | grep -v node_modules \
    | sed "s/fetch(//; s/['\"\`]//g" \
    | tr ',' '\n' | grep "^/" | sort -u || true)

  UNMATCHED_ROUTES=$(comm -23 \
    <(echo "$BACKEND_ROUTES" | sort) \
    <(echo "$FRONTEND_CALLS" | sort) 2>/dev/null || true)

  if [ -n "$UNMATCHED_ROUTES" ]; then
    log_warn "Backend routes with no matching frontend call (may be intentional for external APIs):\n$UNMATCHED_ROUTES"
  else
    log_ok "Backend routes and frontend fetch calls appear consistent"
  fi
else
  log_warn "No src/ directory found — skipping API path check"
fi


# --- 2b. Design doc API paths vs backend routes ---
if ls docs/D*.md 2>/dev/null | head -1 > /dev/null; then
  DOC_PATHS=$(grep -roh '[A-Z]*\s*/[a-z/:-]*' docs/D*.md 2>/dev/null \
    | grep -E "^(GET|POST|PUT|PATCH|DELETE)\s+" \
    | awk '{print $2}' | sort -u || true)
  log_ok "Design docs present — manual cross-check of API paths recommended"
else
  log_warn "No docs/D*.md found — design doc ↔ implementation API path check skipped"
fi


# =============================================================================
# LAYER 3 — DATA CONSISTENCY
# =============================================================================

section "Layer 3: Data Consistency"

# --- 3a. DB column names: init.sql ↔ query layer ↔ TypeScript interfaces ---

SQL_FILES=$(find . -name "*.sql" -not -path "*/node_modules/*" 2>/dev/null || true)
if [ -n "$SQL_FILES" ]; then
  # Extract column names from CREATE TABLE statements
  SQL_COLUMNS=$(echo "$SQL_FILES" | xargs grep -oh '[a-z_]* [A-Z]' 2>/dev/null \
    | sed 's/ [A-Z]//' | grep -v "^$" | sort -u || true)

  # Check TypeScript interfaces for matching field names
  TS_FIELDS=$(find src -name "*.ts" -not -path "*/node_modules/*" 2>/dev/null \
    | xargs grep -oh '^\s*[a-z_]*[?]*:' 2>/dev/null \
    | tr -d ': ?' | grep -v "^$" | sort -u || true)

  # Report columns in SQL not found in any TS interface (warning only — aliases are valid)
  MISSING_TS=$(comm -23 <(echo "$SQL_COLUMNS") <(echo "$TS_FIELDS") 2>/dev/null || true)
  if [ -n "$MISSING_TS" ]; then
    log_warn "SQL columns with no matching TS field (aliases or unused columns?):\n$(echo "$MISSING_TS" | head -20)"
  else
    log_ok "SQL columns appear to have matching TypeScript fields"
  fi
else
  log_warn "No .sql files found — skipping DB ↔ TypeScript column check"
fi


# --- 3b. Migration file ordering ---
MIGRATION_FILES=$(find . \( -name "*.sql" -o -name "*.ts" \) \
  -path "*/migrations/*" -not -path "*/node_modules/*" 2>/dev/null \
  | sort || true)

if [ -n "$MIGRATION_FILES" ]; then
  PREV_NUM=0
  MIGRATION_ERROR=0
  while IFS= read -r f; do
    BASENAME=$(basename "$f")
    # Extract leading number (handles 001_foo.sql, 20240101_bar.ts, etc.)
    NUM=$(echo "$BASENAME" | grep -oh '^[0-9]*' || true)
    if [ -n "$NUM" ]; then
      NUM_INT=$((10#$NUM))
      if [ "$NUM_INT" -lt "$PREV_NUM" ]; then
        log_error "Migration order broken: $BASENAME comes after a higher-numbered file"
        MIGRATION_ERROR=1
      fi
      PREV_NUM=$NUM_INT
    fi
  done <<< "$MIGRATION_FILES"
  if [ "$MIGRATION_ERROR" -eq 0 ]; then
    log_ok "Migration file numbering is sequential"
  fi
else
  log_warn "No migration files found in migrations/ — skipping migration order check"
fi


# =============================================================================
# SECURITY CHECKS
# =============================================================================

section "Security: Secrets in Code"

# --- Hardcoded secrets ---
SECRET_PATTERNS=(
  "AKIA[0-9A-Z]{16}"          # AWS Access Key ID
  "sk-[a-zA-Z0-9]{32,}"       # OpenAI / Anthropic API key prefix
  "ghp_[a-zA-Z0-9]{36}"       # GitHub personal access token
  "ghs_[a-zA-Z0-9]{36}"       # GitHub Actions token
  "xox[baprs]-[0-9A-Za-z]"    # Slack token
  "-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----"  # Private keys
  "password\s*=\s*['\"][^'\"]{4,}['\"]"  # Hardcoded password assignments
)

SECRETS_FOUND=0
for pattern in "${SECRET_PATTERNS[@]}"; do
  MATCHES=$(grep -rn --include="*.ts" --include="*.js" --include="*.py" --include="*.go" \
    -E "$pattern" . 2>/dev/null \
    | grep -v node_modules \
    | grep -v ".test." \
    | grep -v ".env.example" \
    | grep -v "# example" \
    | grep -v "// example" \
    | head -5 || true)
  if [ -n "$MATCHES" ]; then
    log_error "Potential secret found (pattern: $pattern):\n$MATCHES"
    SECRETS_FOUND=1
  fi
done
if [ "$SECRETS_FOUND" -eq 0 ]; then
  log_ok "No hardcoded secrets detected"
fi


# =============================================================================
# CODE HYGIENE
# =============================================================================

section "Code Hygiene"

# --- TODO / FIXME markers ---
if [ -d "src" ]; then
  TODO_COUNT=$(grep -rn "TODO\|FIXME" src/ 2>/dev/null \
    | grep -v node_modules | wc -l | tr -d ' ' || echo "0")
  if [ "$TODO_COUNT" -gt 0 ]; then
    log_warn "$TODO_COUNT TODO/FIXME markers remain in src/ — each should have a tracking issue"
    grep -rn "TODO\|FIXME" src/ 2>/dev/null | grep -v node_modules | head -10 || true
  else
    log_ok "No TODO/FIXME markers in src/"
  fi
fi

# --- console.log / debug artifacts ---
if [ -d "src" ]; then
  DEBUG_COUNT=$(grep -rn "console\.log\|console\.debug\|debugger;" src/ 2>/dev/null \
    | grep -v node_modules \
    | grep -v ".test." \
    | grep -v "logger\." \
    | wc -l | tr -d ' ' || echo "0")
  if [ "$DEBUG_COUNT" -gt 5 ]; then
    log_warn "$DEBUG_COUNT console.log/debug statements in src/ — review before shipping"
  else
    log_ok "console.log count acceptable ($DEBUG_COUNT)"
  fi
fi

# --- Broken imports (Node/TS) ---
if command -v npx &>/dev/null && [ -f "tsconfig.json" ]; then
  TS_ERRORS=$(npx tsc --noEmit 2>&1 | grep -c "error TS" || echo "0")
  if [ "$TS_ERRORS" -gt 0 ]; then
    log_error "TypeScript reports $TS_ERRORS compilation error(s) — run 'npx tsc --noEmit' to see details"
  else
    log_ok "TypeScript compilation: no errors"
  fi
else
  log_warn "No tsconfig.json or npx not available — skipping TypeScript compilation check"
fi


# =============================================================================
# SUMMARY
# =============================================================================

echo
echo "======================================="
echo "  AUDIT SUMMARY"
echo "======================================="
if [ "$ERRORS" -gt 0 ]; then
  echo -e "${RED}  🔴 BLOCKERS: $ERRORS — DEPLOY IS BLOCKED${NC}"
fi
if [ "$WARNINGS" -gt 0 ]; then
  echo -e "${YELLOW}  ⚠️  WARNINGS: $WARNINGS — review before deploy${NC}"
fi
if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
  echo -e "${GREEN}  ✅ All checks passed — cleared for Audit step${NC}"
elif [ "$ERRORS" -eq 0 ]; then
  echo -e "${GREEN}  ✅ No blockers. Review warnings above.${NC}"
fi
echo "======================================="

exit "$ERRORS"
