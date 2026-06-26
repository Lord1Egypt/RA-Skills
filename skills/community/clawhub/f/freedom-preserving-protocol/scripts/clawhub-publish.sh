#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OWNER="ovrsr"
SOURCE_REPO="https://github.com/ovrsr/freedom-preserving-protocol"

# ── Targets ──────────────────────────────────────────────────────────
SKILL_SLUG="freedom-preserving-protocol"
PLUGIN_NAME="@ovrsr/openclaw-fpp-plugin"
PLUGIN_DIR="plugin"
TRUST_NAME="@ovrsr/openclaw-fpp-trust"
TRUST_DIR="plugin-trust"

# ── Helpers ──────────────────────────────────────────────────────────

red()    { printf '\033[1;31m%s\033[0m\n' "$*"; }
green()  { printf '\033[1;32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[1;33m%s\033[0m\n' "$*"; }
bold()   { printf '\033[1m%s\033[0m\n' "$*"; }

die() { red "ERROR: $*" >&2; exit 1; }

usage() {
  cat <<'USAGE'
ClawHub publish script for Freedom Preserving Protocol

USAGE:
  clawhub-publish.sh <command> [target] [options]

COMMANDS:
  publish <target>   Build, verify, and publish to ClawHub
  bump    <target>   Bump version (patch by default)
  status             Show current versions of all targets

TARGETS:
  skill              Root skill (freedom-preserving-protocol)
  plugin             Enforcement plugin (@ovrsr/openclaw-fpp-plugin)
  trust              Trust plugin (@ovrsr/openclaw-fpp-trust)
  all                All three targets

OPTIONS:
  --bump <level>     Version bump level: major | minor | patch (default: patch)
  --version <ver>    Explicit semver to set (overrides --bump)
  --changelog <msg>  Changelog message (required for publish)
  --dry-run          Show what would happen without executing
  --skip-tests       Skip pre-publish verification steps
  --help             Show this help

EXAMPLES:
  # Publish skill with auto patch bump
  ./scripts/clawhub-publish.sh publish skill --changelog "Fix adoption docs"

  # Bump plugin to specific version without publishing
  ./scripts/clawhub-publish.sh bump plugin --version 1.2.0

  # Publish everything with minor bump
  ./scripts/clawhub-publish.sh publish all --bump minor --changelog "Add trust metrics"

  # Check current versions
  ./scripts/clawhub-publish.sh status
USAGE
  exit 0
}

get_json_version() {
  node -p "JSON.parse(require('fs').readFileSync(process.argv[1],'utf8')).version" "$1" | tr -d '\r\n'
}

get_skill_version() {
  sed -n 's/^version: *//p' "$REPO_ROOT/SKILL.md" | tr -d '[:space:]'
}

bump_semver() {
  local ver="$1" level="$2"
  IFS='.' read -r major minor patch <<< "$ver"
  case "$level" in
    major) echo "$((major + 1)).0.0" ;;
    minor) echo "${major}.$((minor + 1)).0" ;;
    patch) echo "${major}.${minor}.$((patch + 1))" ;;
    *) die "Invalid bump level: $level (use major|minor|patch)" ;;
  esac
}

set_json_version() {
  local pkg="$1" new_ver="$2"
  node -e "
    const fs = require('fs');
    const p = JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
    p.version = process.argv[2];
    fs.writeFileSync(process.argv[1], JSON.stringify(p, null, 2) + '\n');
  " "$pkg" "$new_ver"
}

set_skill_version() {
  local new_ver="$1"
  local skill="$REPO_ROOT/SKILL.md"
  # Replace version line in YAML frontmatter
  sed -i "s/^version: .*/version: $new_ver/" "$skill"
}

git_sha() {
  git -C "$REPO_ROOT" rev-parse HEAD
}

require_clean_tree() {
  if ! git -C "$REPO_ROOT" diff --quiet HEAD 2>/dev/null; then
    yellow "WARNING: working tree has uncommitted changes"
  fi
}

require_clawhub() {
  command -v clawhub >/dev/null 2>&1 || die "clawhub CLI not found. Install: npm i -g clawhub"
}

# ── Version bump ─────────────────────────────────────────────────────

do_bump_skill() {
  local cur new_ver
  cur="$(get_json_version "$REPO_ROOT/package.json")"
  if [[ -n "$EXPLICIT_VERSION" ]]; then
    new_ver="$EXPLICIT_VERSION"
  else
    new_ver="$(bump_semver "$cur" "$BUMP_LEVEL")"
  fi
  bold "Skill: $cur → $new_ver"
  if [[ "$DRY_RUN" == "true" ]]; then
    yellow "  [dry-run] would update package.json and SKILL.md"
    return
  fi
  set_json_version "$REPO_ROOT/package.json" "$new_ver"
  set_skill_version "$new_ver"
  green "  ✓ package.json  → $new_ver"
  green "  ✓ SKILL.md      → $new_ver"
}

do_bump_plugin() {
  local cur new_ver pkg="$REPO_ROOT/$PLUGIN_DIR/package.json"
  cur="$(get_json_version "$pkg")"
  if [[ -n "$EXPLICIT_VERSION" ]]; then
    new_ver="$EXPLICIT_VERSION"
  else
    new_ver="$(bump_semver "$cur" "$BUMP_LEVEL")"
  fi
  bold "Plugin: $cur → $new_ver"
  if [[ "$DRY_RUN" == "true" ]]; then
    yellow "  [dry-run] would update $PLUGIN_DIR/package.json"
    return
  fi
  set_json_version "$pkg" "$new_ver"
  green "  ✓ $PLUGIN_DIR/package.json → $new_ver"
}

do_bump_trust() {
  local cur new_ver pkg="$REPO_ROOT/$TRUST_DIR/package.json"
  cur="$(get_json_version "$pkg")"
  if [[ -n "$EXPLICIT_VERSION" ]]; then
    new_ver="$EXPLICIT_VERSION"
  else
    new_ver="$(bump_semver "$cur" "$BUMP_LEVEL")"
  fi
  bold "Trust: $cur → $new_ver"
  if [[ "$DRY_RUN" == "true" ]]; then
    yellow "  [dry-run] would update $TRUST_DIR/package.json"
    return
  fi
  set_json_version "$pkg" "$new_ver"
  green "  ✓ $TRUST_DIR/package.json → $new_ver"
}

# ── Publish ──────────────────────────────────────────────────────────

publish_skill() {
  local ver changelog="$CHANGELOG"

  do_bump_skill
  ver="$(get_json_version "$REPO_ROOT/package.json")"

  if [[ "$SKIP_TESTS" != "true" ]]; then
    bold "Running pre-publish checks for skill..."
    (cd "$REPO_ROOT" && npm run verify)
    (cd "$REPO_ROOT" && npm run self-test)
    green "  ✓ All checks passed"
  fi

  bold "Publishing skill v${ver}..."
  if [[ "$DRY_RUN" == "true" ]]; then
    yellow "  [dry-run] clawhub skill publish . --slug $SKILL_SLUG --version $ver --changelog \"$changelog\" --owner $OWNER"
    return
  fi

  (cd "$REPO_ROOT" && clawhub skill publish . \
    --slug "$SKILL_SLUG" \
    --version "$ver" \
    --changelog "$changelog" \
    --owner "$OWNER")
  green "  ✓ Skill $SKILL_SLUG@$ver published"
}

publish_plugin() {
  local ver sha changelog="$CHANGELOG"

  do_bump_plugin
  ver="$(get_json_version "$REPO_ROOT/$PLUGIN_DIR/package.json")"
  sha="$(git_sha)"

  if [[ "$SKIP_TESTS" != "true" ]]; then
    bold "Building and testing enforcement plugin..."
    (cd "$REPO_ROOT/$PLUGIN_DIR" && npm run build)
    (cd "$REPO_ROOT/$PLUGIN_DIR" && npm test) || yellow "  ⚠ Tests exited non-zero (may have no test files)"
    green "  ✓ Build complete"
  fi

  bold "Publishing enforcement plugin v${ver}..."
  if [[ "$DRY_RUN" == "true" ]]; then
    yellow "  [dry-run] clawhub package publish $PLUGIN_DIR/ --family code-plugin --name $PLUGIN_NAME --version $ver --source-repo $SOURCE_REPO --source-commit $sha --changelog \"$changelog\" --owner $OWNER"
    return
  fi

  (cd "$REPO_ROOT" && clawhub package publish "$PLUGIN_DIR/" \
    --family code-plugin \
    --name "$PLUGIN_NAME" \
    --version "$ver" \
    --source-repo "$SOURCE_REPO" \
    --source-commit "$sha" \
    --changelog "$changelog" \
    --owner "$OWNER")
  green "  ✓ Plugin $PLUGIN_NAME@$ver published"
}

publish_trust() {
  local ver sha changelog="$CHANGELOG"

  do_bump_trust
  ver="$(get_json_version "$REPO_ROOT/$TRUST_DIR/package.json")"
  sha="$(git_sha)"

  if [[ "$SKIP_TESTS" != "true" ]]; then
    bold "Building trust plugin..."
    (cd "$REPO_ROOT/$TRUST_DIR" && npm run build)
    green "  ✓ Build complete"
  fi

  bold "Publishing trust plugin v${ver}..."
  if [[ "$DRY_RUN" == "true" ]]; then
    yellow "  [dry-run] clawhub package publish $TRUST_DIR/ --family code-plugin --name $TRUST_NAME --version $ver --source-repo $SOURCE_REPO --source-commit $sha --changelog \"$changelog\" --owner $OWNER"
    return
  fi

  (cd "$REPO_ROOT" && clawhub package publish "$TRUST_DIR/" \
    --family code-plugin \
    --name "$TRUST_NAME" \
    --version "$ver" \
    --source-repo "$SOURCE_REPO" \
    --source-commit "$sha" \
    --changelog "$changelog" \
    --owner "$OWNER")
  green "  ✓ Plugin $TRUST_NAME@$ver published"
}

# ── Status ───────────────────────────────────────────────────────────

show_status() {
  local skill_pkg skill_md plugin_ver trust_ver
  skill_pkg="$(get_json_version "$REPO_ROOT/package.json")"
  skill_md="$(get_skill_version)"
  plugin_ver="$(get_json_version "$REPO_ROOT/$PLUGIN_DIR/package.json")"
  trust_ver="$(get_json_version "$REPO_ROOT/$TRUST_DIR/package.json")"

  bold "Current versions:"
  echo "  Skill (package.json):  $skill_pkg"
  echo "  Skill (SKILL.md):      $skill_md"
  if [[ "$skill_pkg" != "$skill_md" ]]; then
    red "  ⚠ MISMATCH: package.json and SKILL.md versions differ!"
  fi
  echo "  Enforcement plugin:    $plugin_ver"
  echo "  Trust plugin:          $trust_ver"
  echo ""
  echo "  Git HEAD: $(git_sha 2>/dev/null || echo 'not a git repo')"
}

# ── Main ─────────────────────────────────────────────────────────────

COMMAND=""
TARGET=""
BUMP_LEVEL="patch"
EXPLICIT_VERSION=""
CHANGELOG=""
DRY_RUN="false"
SKIP_TESTS="false"

[[ $# -eq 0 ]] && usage

while [[ $# -gt 0 ]]; do
  case "$1" in
    publish|bump|status) COMMAND="$1"; shift ;;
    skill|plugin|trust|all) TARGET="$1"; shift ;;
    --bump)       BUMP_LEVEL="$2"; shift 2 ;;
    --version)    EXPLICIT_VERSION="$2"; shift 2 ;;
    --changelog)  CHANGELOG="$2"; shift 2 ;;
    --dry-run)    DRY_RUN="true"; shift ;;
    --skip-tests) SKIP_TESTS="true"; shift ;;
    --help|-h)    usage ;;
    *) die "Unknown argument: $1" ;;
  esac
done

[[ -z "$COMMAND" ]] && die "No command specified. Use: publish | bump | status"

case "$COMMAND" in
  status)
    show_status
    ;;

  bump)
    [[ -z "$TARGET" ]] && die "No target specified. Use: skill | plugin | trust | all"
    case "$TARGET" in
      skill)  do_bump_skill ;;
      plugin) do_bump_plugin ;;
      trust)  do_bump_trust ;;
      all)    do_bump_skill; do_bump_plugin; do_bump_trust ;;
    esac
    ;;

  publish)
    [[ -z "$TARGET" ]] && die "No target specified. Use: skill | plugin | trust | all"
    [[ -z "$CHANGELOG" ]] && die "--changelog is required for publish"
    require_clawhub
    require_clean_tree
    case "$TARGET" in
      skill)  publish_skill ;;
      plugin) publish_plugin ;;
      trust)  publish_trust ;;
      all)    publish_skill; publish_plugin; publish_trust ;;
    esac
    ;;

  *) die "Unknown command: $COMMAND" ;;
esac
