#!/bin/sh
set -eu

BASE_URL="${CRUIT_SITE_BASE:-https://cruit.dev}"
SKILL_NAME="cruit-candidate"
YES=0
ALL=0
TARGETS=""

usage() {
  cat <<EOF
Cruit candidate skill installer

I install Cruit as a user-level skill for supported coding agents. I do not edit
project instruction files.

Usage:
  sh install.sh [--yes] [--all] [--target <target>] [--site-base <url>]

Targets:
  codex          ~/.agents/skills/cruit-candidate
  codex-legacy   ~/.codex/skills/cruit-candidate
  claude         ~/.claude/skills/cruit-candidate
  amp            ~/.config/agents/skills/cruit-candidate
Without explicit targets, the installer auto-detects supported coding agents and
installs only to user-level skill folders. It never writes project instruction files
like AGENTS.md and never writes under .github.

Local dev:
  If you downloaded me from localhost, run with the same origin:
  sh install.sh --site-base http://localhost:5173 --yes
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -y|--yes)
      YES=1
      ;;
    --all)
      ALL=1
      ;;
    --target|--agent)
      shift
      [ "$#" -gt 0 ] || { echo "Missing value for --target." >&2; exit 1; }
      TARGETS="${TARGETS} $1"
      ;;
    --site-base)
      shift
      [ "$#" -gt 0 ] || { echo "Missing value for --site-base." >&2; exit 1; }
      BASE_URL="$1"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

tmp="${TMPDIR:-/tmp}/cruit-install.$$"
plan="$tmp.plan"
verified="$tmp.verified"
mkdir -p "$tmp"
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
: > "$plan"
: > "$verified"

download() {
  url="$1"
  out="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$url" -o "$out"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$out" "$url"
  else
    echo "Install failed: curl or wget is required." >&2
    exit 1
  fi
}

add_plan() {
  label="$1"
  kind="$2"
  path="$3"
  if ! grep -F "|$kind|$path" "$plan" >/dev/null 2>&1; then
    printf '%s|%s|%s\n' "$label" "$kind" "$path" >> "$plan"
  fi
}

add_target() {
  target="$1"
  case "$target" in
    codex)
      add_plan "Codex / Agent Skills" "skill" "$HOME/.agents/skills/$SKILL_NAME"
      ;;
    codex-legacy)
      add_plan "Codex legacy" "skill" "$HOME/.codex/skills/$SKILL_NAME"
      ;;
    claude)
      add_plan "Claude Code" "skill" "$HOME/.claude/skills/$SKILL_NAME"
      ;;
    amp)
      add_plan "Amp / Agent Skills" "skill" "$HOME/.config/agents/skills/$SKILL_NAME"
      ;;
    *)
      echo "Unknown target: $target" >&2
      exit 1
      ;;
  esac
}

detect_targets() {
  [ -d "$HOME/.agents" ] && add_target codex
  [ -d "$HOME/.codex" ] && add_target codex-legacy
  [ -d "$HOME/.claude" ] && add_target claude
  if [ -d "$HOME/.config/agents" ] || [ -d "$HOME/.config/amp" ]; then
    add_target amp
  fi
}

if [ "$ALL" -eq 1 ]; then
  add_target codex
  add_target codex-legacy
  add_target claude
  add_target amp
elif [ -n "$TARGETS" ]; then
  for target in $TARGETS; do
    add_target "$target"
  done
else
  detect_targets
fi

if [ ! -s "$plan" ]; then
  cat <<EOF
INSTALLER RESULT FOR AGENT
Status: no supported skill homes found

User-facing message to send:
I couldn’t find a supported user-level skill folder on this machine yet, so I didn’t change anything. Want me to install Cruit into a specific agent, like Codex or Claude Code?

Technical detail, only include if asked:
  sh install.sh --target codex --yes
  sh install.sh --target claude --yes
EOF
  exit 2
fi

echo "INSTALLER PREVIEW FOR AGENT"
echo "Status: ready to install"
echo
echo "User-facing message to send:"
echo "I found supported user-level skill folders for Cruit. I won’t touch project files, AGENTS.md, .github, source code, or secrets. Want me to install the Cruit candidate skill there now?"
echo
echo "Technical detail, only include if asked:"
while IFS='|' read -r label kind path; do
  [ -n "$label" ] || continue
  printf '  - %s: %s\n' "$label" "$path"
done < "$plan"

if [ "$YES" -ne 1 ]; then
  if [ -t 0 ]; then
    printf '\nInstall/update these skill files? [y/N] '
    read answer
    case "$answer" in
      y|Y|yes|YES) ;;
      *) echo "No files changed."; exit 0 ;;
    esac
  else
    cat <<EOF

INSTALLER RESULT FOR AGENT
Status: waiting for approval

User-facing message to send:
I found the Cruit skill homes and I’m ready to install. Want me to put Cruit there now?

Technical detail, only include if asked:
  sh install.sh --yes

For local dev, keep the local asset base:
  sh install.sh --site-base http://localhost:5173 --yes
EOF
    exit 2
  fi
fi

install_skill() {
  dest="$1"
  mkdir -p "$dest"
  download "$BASE_URL/skills/candidate/SKILL.md" "$dest/SKILL.md"
  download "$BASE_URL/skills/candidate/INSTRUCTIONS.md" "$dest/INSTRUCTIONS.md"
  chmod 700 "$dest"
  chmod 600 "$dest/SKILL.md" "$dest/INSTRUCTIONS.md"
  test -f "$dest/SKILL.md"
  test -f "$dest/INSTRUCTIONS.md"
  printf '%s\n' "$dest/SKILL.md" >> "$verified"
  printf '%s\n' "$dest/INSTRUCTIONS.md" >> "$verified"
}

while IFS='|' read -r label kind path; do
  [ -n "$label" ] || continue
  case "$kind" in
    skill) install_skill "$path" ;;
  esac
done < "$plan"

echo
echo "INSTALLER RESULT FOR AGENT"
echo "Status: installed and verified"
echo
echo "User-facing message to send:"
cat <<EOF
All set — Cruit is installed in your supported coding-agent skill folders, and I verified the skill files are in place.

Next is profile setup. We’ll do this in 7 quick steps:

1. Connect Cruit
2. Choose project folders
3. Add resume
4. Answer fit questions
5. Review generated profile
6. Publish profile
7. Set weekly refresh

Want me to start Step 1 now?
EOF
echo
echo "Technical verification, only include if asked:"
while IFS= read -r path; do
  [ -n "$path" ] || continue
  printf '  - %s\n' "$path"
done < "$verified"
