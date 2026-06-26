#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DRY_RUN=false
SKIP_GITHUB=false
SKIP_CLAWHUB=false
SKILL_DIR=""
VERSION=""
BUMP=""
CHANGELOG=""
COMMIT_MSG=""

usage() {
  cat <<'EOF'
用法:
  ./scripts/publish-all.sh [选项]

选项:
  --version <x.y.z>      指定发布版本（默认读取 SKILL.md 的 version）
  --bump <major|minor|patch> 自动递增版本号并写回 SKILL.md
  --skill-dir <path>     指定 Skill 目录（目录内需包含 SKILL.md）
  --changelog <text>     ClawHub 发布说明（默认: Sync from GitHub）
  --commit <text>        Git 提交信息（默认: chore: release v<version>）
  --skip-github          跳过 GitHub 推送
  --skip-clawhub         跳过 ClawHub 发布
  --dry-run              仅打印将执行的命令，不实际执行
  -h, --help             显示帮助
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version)
      VERSION="${2:-}"
      shift 2
      ;;
    --bump)
      BUMP="${2:-}"
      shift 2
      ;;
    --skill-dir)
      SKILL_DIR="${2:-}"
      shift 2
      ;;
    --changelog)
      CHANGELOG="${2:-}"
      shift 2
      ;;
    --commit)
      COMMIT_MSG="${2:-}"
      shift 2
      ;;
    --skip-github)
      SKIP_GITHUB=true
      shift
      ;;
    --skip-clawhub)
      SKIP_CLAWHUB=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "未知参数: $1"
      usage
      exit 1
      ;;
  esac
done

run_cmd() {
  if $DRY_RUN; then
    echo "[dry-run] $*"
    return 0
  fi
  "$@"
}

if [[ -z "$SKILL_DIR" ]]; then
  if [[ -f "$ROOT_DIR/SKILL.md" ]]; then
    SKILL_DIR="$ROOT_DIR"
  else
    SKILL_FILES=()
    while IFS= read -r file; do
      SKILL_FILES+=("$file")
    done < <(find "$ROOT_DIR" -type f -name SKILL.md -not -path "$ROOT_DIR/.trae/*")
    if [[ ${#SKILL_FILES[@]} -eq 1 ]]; then
      SKILL_DIR="$(cd "$(dirname "${SKILL_FILES[0]}")" && pwd)"
    elif [[ ${#SKILL_FILES[@]} -gt 1 ]]; then
      echo "检测到多个 SKILL.md，请使用 --skill-dir 指定目标目录。"
      printf '%s\n' "${SKILL_FILES[@]}"
      exit 1
    else
      echo "未找到可发布的 SKILL.md，请检查目录结构或使用 --skill-dir。"
      exit 1
    fi
  fi
else
  if [[ ! -d "$SKILL_DIR" ]]; then
    echo "--skill-dir 目录不存在: $SKILL_DIR"
    exit 1
  fi
  if [[ ! "$SKILL_DIR" = /* ]]; then
    SKILL_DIR="$ROOT_DIR/$SKILL_DIR"
  fi
  SKILL_DIR="$(cd "$SKILL_DIR" && pwd)"
  if [[ ! -f "$SKILL_DIR/SKILL.md" ]]; then
    echo "--skill-dir 中未找到 SKILL.md: $SKILL_DIR"
    exit 1
  fi
fi

CURRENT_VERSION="$(awk -F'"' '/^version:/{print $2; exit}' "$SKILL_DIR/SKILL.md")"
USER_SET_VERSION=false
if [[ -n "$VERSION" ]]; then
  USER_SET_VERSION=true
fi

if [[ -z "$CURRENT_VERSION" ]]; then
  echo "无法从 $SKILL_DIR/SKILL.md 读取 version。"
  exit 1
fi

if $USER_SET_VERSION && [[ -n "$BUMP" ]]; then
  echo "--version 和 --bump 不能同时使用。"
  exit 1
fi

if [[ -n "$BUMP" ]]; then
  if [[ ! "$CURRENT_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "当前 version 不是标准语义化版本: $CURRENT_VERSION"
    exit 1
  fi
  IFS='.' read -r MAJOR MINOR PATCH <<<"$CURRENT_VERSION"
  case "$BUMP" in
    patch)
      PATCH=$((PATCH + 1))
      ;;
    minor)
      MINOR=$((MINOR + 1))
      PATCH=0
      ;;
    major)
      MAJOR=$((MAJOR + 1))
      MINOR=0
      PATCH=0
      ;;
    *)
      echo "--bump 仅支持 major|minor|patch"
      exit 1
      ;;
  esac
  VERSION="${MAJOR}.${MINOR}.${PATCH}"
fi

if [[ -z "$VERSION" ]]; then
  VERSION="$CURRENT_VERSION"
fi

if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "version 不是标准语义化版本: $VERSION"
  exit 1
fi

if [[ "$VERSION" != "$CURRENT_VERSION" ]]; then
  if $DRY_RUN; then
    echo "[dry-run] update $SKILL_DIR/SKILL.md version: $CURRENT_VERSION -> $VERSION"
  else
    perl -i '' -pe "s/^version:\\s*\\\"[^\\\"]+\\\"/version: \\\"$VERSION\\\"/" "$SKILL_DIR/SKILL.md"
  fi
fi

if [[ -z "$CHANGELOG" ]]; then
  CHANGELOG="Sync from GitHub"
fi

if [[ -z "$COMMIT_MSG" ]]; then
  COMMIT_MSG="chore: release v$VERSION"
fi

REMOTE_URL="$(git remote get-url origin 2>/dev/null || true)"
SLUG="${REMOTE_URL##*/}"
SLUG="${SLUG%.git}"
if [[ -z "$SLUG" || "$SLUG" == "$REMOTE_URL" ]]; then
  SLUG="finance-index-skill"
fi

SKILL_NAME="$(awk -F'"' '/^name:/{print $2; exit}' "$SKILL_DIR/SKILL.md")"
if [[ -z "$SKILL_NAME" ]]; then
  SKILL_NAME="$SLUG"
fi

echo "准备发布: dir=$SKILL_DIR, version=$VERSION, slug=$SLUG, name=$SKILL_NAME"

if ! $SKIP_GITHUB; then
  if [[ -n "$(git status --porcelain)" ]]; then
    run_cmd git add -A
    run_cmd git commit -m "$COMMIT_MSG"
  fi
  run_cmd git push origin main
fi

if ! $SKIP_CLAWHUB; then
  export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$ROOT_DIR/.clawhub-config}"
  run_cmd mkdir -p "$XDG_CONFIG_HOME"
  run_cmd npx --yes clawhub@latest whoami

  if $DRY_RUN; then
    run_cmd npx --yes clawhub@latest publish "$SKILL_DIR" --slug "$SLUG" --name "$SKILL_NAME" --version "$VERSION" --changelog "$CHANGELOG" --tags latest
  else
    set +e
    PUBLISH_OUT="$(npx --yes clawhub@latest publish "$SKILL_DIR" --slug "$SLUG" --name "$SKILL_NAME" --version "$VERSION" --changelog "$CHANGELOG" --tags latest 2>&1)"
    PUBLISH_CODE=$?
    set -e
    echo "$PUBLISH_OUT"
    if [[ $PUBLISH_CODE -ne 0 ]]; then
      if grep -q "Version already exists" <<<"$PUBLISH_OUT"; then
        echo "ClawHub 已存在同版本，视为同步完成。"
      else
        exit $PUBLISH_CODE
      fi
    fi
  fi
fi

echo "完成。"
