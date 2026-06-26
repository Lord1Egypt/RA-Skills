#!/usr/bin/env bash
# memes - Agent meme library manager with multi-platform send
set -euo pipefail

MEMES_DIR="${MEMES_DIR:-$HOME/.openclaw/workspace/memes}"
# Load config file if present (sets defaults for MEMES_DEFAULT_*, OPENCLAW_CHANNEL, etc.)
MEMES_CONFIG="${MEMES_CONFIG:-$HOME/.config/memes/config}"
[[ -f "$MEMES_CONFIG" ]] && source "$MEMES_CONFIG"
# Also check legacy location
[[ -f "$HOME/.memesrc" ]] && source "$HOME/.memesrc"
# Auto-detect channel + target from OpenClaw runtime context file
# Format: "platform:target" e.g. "telegram:12345" or "discord:98765" or just "telegram"
OPENCLAW_CHANNEL_FILE="${OPENCLAW_CHANNEL_FILE:-/tmp/openclaw-current-channel}"
if [[ -z "${OPENCLAW_CHANNEL:-}" && -f "$OPENCLAW_CHANNEL_FILE" ]]; then
  # Only use file if it's less than 5 minutes old (300 seconds)
  _file_age=$(( $(date +%s) - $(stat -c %Y "$OPENCLAW_CHANNEL_FILE" 2>/dev/null || echo 0) ))
  if [[ $_file_age -lt 300 ]]; then
    _ctx=$(cat "$OPENCLAW_CHANNEL_FILE")
    if [[ "$_ctx" == *:* ]]; then
      OPENCLAW_CHANNEL="${_ctx%%:*}"
      MEMES_CURRENT_TARGET="${_ctx#*:}"
    else
      OPENCLAW_CHANNEL="$_ctx"
    fi
  fi
fi
# Auto-detect scripts dir: same directory as this script, or override with MEMES_SCRIPTS
SCRIPTS_DIR="${MEMES_SCRIPTS:-$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")/.." 2>/dev/null && pwd)/scripts}"
[[ ! -d "$SCRIPTS_DIR" ]] && SCRIPTS_DIR="$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")"

usage() {
  cat <<EOF
Usage: memes <command> [args]

Commands:
  pick <category>         Randomly pick a meme, print its path
  list <category>         List all memes in a category
  random                  Pick from any category at random
  send <category> [caption] [--to target] [--channel platform] [--account name]
  categories              List all categories with counts

Platforms with fast send: discord, feishu, telegram
Other platforms fall back to: openclaw message send

Examples:
  memes send happy "好开心！" --to <channel_id>         # → Discord
  memes send facepalm --to channel:1491636222853124176  # → Discord #work
  memes send feishu cute-animals "看！" --to user:xxx   # → Feishu
  memes send telegram wow --to 12345678                 # → Telegram
EOF
  exit 1
}

cmd_categories() {
  [[ ! -d "$MEMES_DIR" ]] && { echo "Error: Meme library not found at $MEMES_DIR" >&2; exit 1; }
  for dir in "$MEMES_DIR"/*/; do
    [[ -d "$dir" ]] || continue
    name=$(basename "$dir"); [[ "$name" == .* ]] && continue
    count=$(find "$dir" -maxdepth 1 -type f \( -name '*.gif' -o -name '*.jpg' -o -name '*.png' -o -name '*.webp' \) 2>/dev/null | wc -l)
    printf "%-20s %d\n" "$name" "$count"
  done | sort
}

cmd_pick() {
  local category="${1:-}"
  [[ -z "$category" ]] && { echo "Usage: memes pick <category>" >&2; exit 1; }
  # Alias mapping (Chinese/common names → folder names)
  declare -A ALIASES=(
    [哇]=wow [惊讶]=wow [surprised]=wow
    [开心]=happy [高兴]=happy [庆祝]=happy [celebrate]=happy
    [无语]=facepalm [晕]=facepalm [服了]=facepalm
    [加油]=encourage [鼓励]=encourage
    [可爱]=cute-animals [萌]=cute-animals [猫]=cute-animals
    [难过]=sad [伤心]=sad
    [累]=tired [困]=tired
    [爱]=love [喜欢]=love
    [谢谢]=thanks [感谢]=thanks
    [想]=thinking [思考]=thinking [嗯]=thinking
    [慌]=panic [急]=panic
    [早]=greeting-morning [早安]=greeting-morning
    [晚安]=greeting-night [晚]=greeting-night
    [你好]=greeting-hello [hi]=greeting-hello [hello]=greeting-hello
    [再见]=greeting-bye [拜]=greeting-bye [bye]=greeting-bye
    [赞]=approve [好]=approve
    [debug]=debug-mood [bug]=debug-mood
    [迷惑]=confused [懵]=confused
    [摊手]=shrug [无奈]=shrug [没办法]=shrug [随便]=shrug
    [干活]=working [忙]=working [在搞]=working [coding]=working
  )
  category="${ALIASES[$category]:-$category}"
  local dir="$MEMES_DIR/$category"
  [[ ! -d "$dir" ]] && { echo "Error: Category '$category' not found. Run 'memes categories' for list." >&2; exit 1; }
  local files=()
  while IFS= read -r f; do files+=("$f"); done < <(find "$dir" -maxdepth 1 -type f \( -name '*.gif' -o -name '*.jpg' -o -name '*.png' -o -name '*.webp' \) 2>/dev/null)
  [[ ${#files[@]} -eq 0 ]] && { echo "Error: No memes in '$category'" >&2; exit 1; }
  local picked="${files[$((RANDOM % ${#files[@]}))]}"
  # Detect git LFS pointer (not real image)
  if [[ $(stat -c%s "$picked" 2>/dev/null || stat -f%z "$picked" 2>/dev/null) -lt 1024 ]] && grep -q 'oid sha256' "$picked" 2>/dev/null; then
    echo "Error: '$picked' is a git LFS pointer, not a real image." >&2
    echo "Run: cd \"$MEMES_DIR\" && git lfs pull" >&2
    exit 1
  fi
  echo "$picked"
}

cmd_list() {
  local category="${1:-}"
  [[ -z "$category" ]] && { echo "Usage: memes list <category>" >&2; exit 1; }
  local dir="$MEMES_DIR/$category"
  [[ ! -d "$dir" ]] && { echo "Error: Category '$category' not found." >&2; exit 1; }
  find "$dir" -maxdepth 1 -type f \( -name '*.gif' -o -name '*.jpg' -o -name '*.png' -o -name '*.webp' \) 2>/dev/null | sort
}

cmd_random() {
  local cats=()
  for dir in "$MEMES_DIR"/*/; do
    [[ -d "$dir" ]] || continue
    local name=$(basename "$dir"); [[ "$name" == .* ]] && continue
    cats+=("$name")
  done
  [[ ${#cats[@]} -eq 0 ]] && { echo "Error: No categories found" >&2; exit 1; }
  local cat="${cats[$((RANDOM % ${#cats[@]}))]}"
  cmd_pick "$cat"
}

cmd_send() {
  local category="" caption="" to="" channel="${OPENCLAW_CHANNEL:-discord}" account=""
  # Detect platform as first arg (overrides env default)
  [[ "${1:-}" =~ ^(discord|feishu|telegram|whatsapp|slack|line|qq|wechat)$ ]] && { channel="$1"; shift; }
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --category|-c)  category="$2"; shift 2 ;;
      --caption|-m)   caption="$2"; shift 2 ;;
      --to|-t)        to="$2"; shift 2 ;;
      --channel)      channel="$2"; shift 2 ;;
      --account|-a)   account="$2"; shift 2 ;;
      *)              if [[ -z "$category" ]]; then category="$1"; else caption="${caption:+$caption }$1"; fi; shift ;;
    esac
  done
  [[ -z "$category" ]] && { echo "Usage: memes send <category> [caption] [--to target] [--channel platform]" >&2; exit 1; }

  local meme_path; meme_path=$(cmd_pick "$category")

  # Timeout for send commands (prevents SIGKILL from parent exec timeout)
  local SEND_TIMEOUT="${MEMES_SEND_TIMEOUT:-30}"

  # Try platform-specific fast script first, fall back to openclaw CLI
  case "$channel" in
    discord)
      local script="$SCRIPTS_DIR/discord-send-image.sh"
      local target="${to#channel:}"
      if [[ -z "$target" ]]; then
        target="${MEMES_CURRENT_TARGET:-${MEMES_DEFAULT_CHANNEL:-}}"
        [[ -z "$target" ]] && { echo "Error: --to <channel_id> required (or set MEMES_DEFAULT_CHANNEL)" >&2; exit 1; }
      fi
      if [[ -x "$script" ]]; then
        timeout "$SEND_TIMEOUT" bash "$script" "$target" "$meme_path" "$caption"
      else
        _send_openclaw "$meme_path" "$caption" "$to" "$channel" "$account"
      fi
      ;;
    feishu)
      local script="$SCRIPTS_DIR/feishu-send-image.mjs"
      local target="${to:-${MEMES_CURRENT_TARGET:-${MEMES_DEFAULT_FEISHU:-}}}"
      [[ -z "$target" ]] && { echo "Error: --to <target> required (or set MEMES_DEFAULT_FEISHU)" >&2; exit 1; }
      if [[ -f "$script" ]]; then
        timeout "$SEND_TIMEOUT" node "$script" "$target" "$meme_path" ${caption:+"$caption"}
      else
        _send_openclaw "$meme_path" "$caption" "$to" "feishu" "$account"
      fi
      ;;
    line)
      local script="$SCRIPTS_DIR/line-send-image.sh"
      local target="${to:-${MEMES_CURRENT_TARGET:-${MEMES_DEFAULT_LINE:-}}}"
      [[ -z "$target" ]] && { echo "Error: --to <user_or_group_id> required (or set MEMES_DEFAULT_LINE)" >&2; exit 1; }
      if [[ -x "$script" ]]; then
        timeout "$SEND_TIMEOUT" bash "$script" "$target" "$meme_path" "$caption"
      else
        _send_openclaw "$meme_path" "$caption" "$to" "line" "$account"
      fi
      ;;
    telegram)
      local script="$SCRIPTS_DIR/telegram-send-image.sh"
      local target="${to:-${MEMES_CURRENT_TARGET:-${MEMES_DEFAULT_TELEGRAM:-}}}"
      [[ -z "$target" ]] && { echo "Error: --to <chat_id> required (or set MEMES_DEFAULT_TELEGRAM)" >&2; exit 1; }
      if [[ -x "$script" ]]; then
        timeout "$SEND_TIMEOUT" bash "$script" "$target" "$meme_path" "$caption"
      else
        _send_openclaw "$meme_path" "$caption" "$to" "telegram" "$account"
      fi
      ;;
    *)
      local script="$SCRIPTS_DIR/${channel}-send-image.sh"
      if [[ -x "$script" ]]; then
        timeout "$SEND_TIMEOUT" bash "$script" "${to:-}" "$meme_path" "$caption"
      else
        _send_openclaw "$meme_path" "$caption" "$to" "$channel" "$account"
      fi
      ;;
  esac

  echo "$meme_path"
}

_send_openclaw() {
  local meme_path="$1" caption="$2" to="$3" channel="$4" account="$5"
  local send_timeout="${MEMES_SEND_TIMEOUT:-30}"
  local cmd="cd $HOME/repo/openclaw && node scripts/run-node.mjs message send"
  cmd+=" --channel $channel"
  [[ -n "$account" ]] && cmd+=" --account $account"
  [[ -n "$to" ]] && cmd+=" --target \"$to\""
  cmd+=" --media \"$meme_path\""
  [[ -n "$caption" ]] && cmd+=" --message \"$caption\""
  timeout "$send_timeout" bash -c "$cmd" 2>&1
}

[[ $# -lt 1 ]] && usage
case "$1" in
  pick)       shift; cmd_pick "$@" ;;
  list)       shift; cmd_list "$@" ;;
  random)     cmd_random ;;
  send)       shift; cmd_send "$@" ;;
  categories) cmd_categories ;;
  -h|--help)  usage ;;
  *)          echo "Unknown command: $1" >&2; usage ;;
esac
