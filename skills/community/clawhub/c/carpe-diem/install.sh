#!/usr/bin/env bash
#
# Carpe Diem — 一键安装脚本
# One-click install script
#
# 用法:
#   # 从项目根目录直接运行
#   bash install.sh --platform openclaw
#   bash install.sh --platform openclaw --target ~/.openclaw/skills/carpe-diem
#   bash install.sh --platform claude-code --dry-run
#
#   # 从 GitHub 安装时，先克隆并审查脚本，再在源码根目录执行
#   git clone --depth 1 https://github.com/wanghaonan3333-web/carpe-diem.git
#   cd carpe-diem && less install.sh
#   bash install.sh --platform codex
#
# Options:
#   --platform <name>   Target platform: codex, claude-code, cursor, openclaw (默认 auto-detect)
#   --target <path>     Install directory (platform default if omitted)
#   --dry-run           Generate and show install plan without applying
#   --skip-verify       Skip verification step after apply
#   --help, -h          Show this help message

set -euo pipefail

SCRIPT_NAME="$(basename "$0")"

# ── Color helpers (disabled if not terminal) ──────────────────────────────
if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  CYAN='\033[0;36m'
  NC='\033[0m' # No Color
else
  RED=''; GREEN=''; YELLOW=''; CYAN=''; NC=''
fi

info()  { printf "${GREEN}✓${NC} %s\n" "$*"; }
warn()  { printf "${YELLOW}⚠${NC} %s\n" "$*"; }
error() { printf "${RED}✗${NC} %s\n" "$*" >&2; }
step()  { printf "\n${CYAN}==>${NC} %s\n" "$*"; }

# ── Help ──────────────────────────────────────────────────────────────────
show_help() {
  cat <<EOF
Carpe Diem — One-click install

用法:
  # 从项目根目录直接运行
  bash install.sh --platform openclaw
  bash install.sh --platform openclaw --target ~/.openclaw/skills/carpe-diem
  bash install.sh --platform claude-code --dry-run

  # 从 GitHub 安装时，先克隆并审查脚本，再在源码根目录执行
  git clone --depth 1 https://github.com/wanghaonan3333-web/carpe-diem.git
  cd carpe-diem
  less install.sh
  bash install.sh --platform codex

Options:
  --platform <name>   Target platform: codex, claude-code, cursor, openclaw
  --target <path>     Install directory (platform default if omitted)
  --dry-run           Generate and show install plan without applying
  --skip-verify       Skip verification step after apply
  --help, -h          Show this help message
EOF
  exit 0
}

# ── Parse arguments ───────────────────────────────────────────────────────
PLATFORM=""
TARGET=""
DRY_RUN=false
SKIP_VERIFY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform)
      PLATFORM="$2"
      shift 2
      ;;
    --target)
      TARGET="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --skip-verify)
      SKIP_VERIFY=true
      shift
      ;;
    --help|-h)
      show_help
      ;;
    *)
      error "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# ── Pre-flight checks ────────────────────────────────────────────────────
step "Pre-flight checks"

# Python 3.10+
PYTHON=""
if command -v python3 &>/dev/null; then
  PYTHON="python3"
elif command -v python &>/dev/null; then
  PYTHON="python"
else
  error "Python not found. Carpe Diem requires Python 3.10+."
  exit 1
fi

PYTHON_VERSION=$("$PYTHON" --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]; }; then
  error "Carpe Diem requires Python 3.10+. Found: $PYTHON_VERSION"
  exit 1
fi
info "Python $PYTHON_VERSION — OK"

# ── Detect project root ───────────────────────────────────────────────────
# 安装脚本只使用用户已经下载并可审查的本地源码，不自动拉取或执行远程内容。
PROJECT_DIR=""
step "Detecting Carpe Diem source"
if [ -f "scripts/carpe_diem.py" ]; then
  PROJECT_DIR="$(pwd)"
  info "Found Carpe Diem project root: $PROJECT_DIR"
elif [ -f "$(dirname "$0")/scripts/carpe_diem.py" ]; then
  PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
  info "Found Carpe Diem project root: $PROJECT_DIR"
else
  error "Run this installer from a reviewed Carpe Diem source directory."
  error "Expected scripts/carpe_diem.py beside install.sh; no remote code was downloaded."
  exit 1
fi

cd "$PROJECT_DIR"

# ── Detect platform ──────────────────────────────────────────────────────
step "Detecting platform"

if [ -n "$PLATFORM" ]; then
  # Validate platform name
  case "$PLATFORM" in
    codex|claude-code|cursor|openclaw)
      info "Using specified platform: $PLATFORM"
      ;;
    *)
      error "Unsupported platform: $PLATFORM. Valid options: codex, claude-code, cursor, openclaw"
      exit 1
      ;;
  esac
else
  info "Auto-detecting installed platforms..."
  DETECT_OUTPUT=$("$PYTHON" scripts/carpe_diem.py install detect --json 2>/dev/null || echo '{"platforms":[]}')
  # Find the first platform whose CLI binary is actually on PATH
  PLATFORM=$(echo "$DETECT_OUTPUT" | "$PYTHON" -c "
import json, sys
data = json.load(sys.stdin)
for p in data.get('platforms', []):
    if p.get('command_path'):
        print(p['platform'])
        sys.exit(0)
print('')
" 2>/dev/null || true)

  if [ -z "$PLATFORM" ]; then
    # No CLI detected; list available platforms and suggest the first one
    PLATFORM="codex"
    warn "No supported platform CLI detected on PATH."
    warn "Defaulting to 'codex'. You can override with: --platform claude-code|cursor|openclaw"
    warn "Or install the target CLI first, then re-run without --platform for auto-detection."
  else
    info "Auto-detected platform: $PLATFORM"
  fi
fi

# ── Generate install plan ────────────────────────────────────────────────
step "Generating install plan"

PLAN_FILE="/tmp/carpe-diem-install-$$.json"
PLAN_ARGS=("--platform" "$PLATFORM" "--json")

if [ -n "$TARGET" ]; then
  PLAN_ARGS+=("--target" "$TARGET")
fi

"$PYTHON" scripts/carpe_diem.py install plan "${PLAN_ARGS[@]}" > "$PLAN_FILE" 2>/dev/null

if [ ! -s "$PLAN_FILE" ]; then
  error "Install plan generation failed."
  exit 1
fi

# Show plan summary
PLATFORM_DISPLAY=$("$PYTHON" -c "
import json
with open('$PLAN_FILE') as f:
    d = json.load(f)
print(f'  Platform: {d.get(\"platform\", \"?\")}')
print(f'  Target:   {d.get(\"target\", \"?\")}')
print(f'  Version:  {d.get(\"version\", \"?\")}')
print(f'  Files:    {len(d.get(\"files\", []))}')
" 2>/dev/null || echo "  (plan summary unavailable)")

echo "$PLATFORM_DISPLAY"

# ── Dry-run: show plan and exit ──────────────────────────────────────────
if $DRY_RUN; then
  step "Dry-run mode — install plan (not applied)"
  "$PYTHON" -m json.tool "$PLAN_FILE" 2>/dev/null || cat "$PLAN_FILE"
  info "Dry-run complete. Remove $PLAN_FILE manually if desired."
  exit 0
fi

# ── Apply plan ───────────────────────────────────────────────────────────
step "Applying install plan"

"$PYTHON" scripts/carpe_diem.py install apply --plan "$PLAN_FILE" --yes 2>&1

APPLY_EXIT=$?
if [ "$APPLY_EXIT" -ne 0 ]; then
  error "Install apply failed (exit code $APPLY_EXIT)."
  error "Check the plan at $PLAN_FILE for details."
  exit 1
fi
info "Install applied successfully"

# ── Verify ────────────────────────────────────────────────────────────────
if $SKIP_VERIFY; then
  warn "Verification skipped (--skip-verify)"
else
  step "Verifying installation"

  # Extract target directory from plan
  TARGET_DIR=$("$PYTHON" -c "
import json
with open('$PLAN_FILE') as f:
    d = json.load(f)
print(d.get('target', ''))
" 2>/dev/null || true)

  if [ -n "$TARGET_DIR" ]; then
    "$PYTHON" scripts/carpe_diem.py install verify --target "$TARGET_DIR" 2>&1
    VERIFY_EXIT=$?
    if [ "$VERIFY_EXIT" -eq 0 ]; then
      info "Verification passed — all files match their receipt"
    else
      warn "Verification reported issues (exit code $VERIFY_EXIT)."
      warn "You can re-run: python3 scripts/carpe_diem.py install verify --target $TARGET_DIR"
    fi
  else
    warn "Could not extract target directory from plan, skipping verification."
  fi
fi

# ── Done ──────────────────────────────────────────────────────────────────
step "Installation complete"

echo ""
echo "  Carpe Diem has been installed to your $PLATFORM skill directory."
echo ""
echo "  Next step: open a new $PLATFORM session and say:"
echo ""

case "$PLATFORM" in
  codex)
    echo "    \"我想做一个项目，但没有头绪。\""
    echo "    \"I want to build a project, but I have no direction.\""
    ;;
  claude-code)
    echo "    \"帮我找到一个值得做的开源项目。\""
    echo "    \"Help me find an open-source project worth building.\""
    ;;
  cursor)
    echo "    \"我有 Coding Agent，但不知道做什么。\""
    echo "    \"I have a Coding Agent but do not know what to build.\""
    ;;
  openclaw)
    echo "    \"我想开始一个项目，但还没有方向。\""
    echo "    \"I want to start a project, but I have no direction yet.\""
    ;;
esac

echo ""
info "If the Skill is not auto-discovered, explicitly ask your Agent to read:"
echo "    $TARGET_DIR/SKILL.md"
echo ""
