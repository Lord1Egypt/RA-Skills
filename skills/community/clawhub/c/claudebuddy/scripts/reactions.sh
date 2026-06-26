#!/usr/bin/env bash
# Buddy Reaction Engine — detects triggers and generates reactions
# Usage: reactions.sh check "<message>"
# Output: reaction_type|reaction_text

set -euo pipefail

case "${1:-}" in
  check)
    MESSAGE="${2:-}"
    ;;
  *)
    MESSAGE="${1:-}"
    ;;
esac

if [[ -z "$MESSAGE" ]]; then
  echo "none|"
  exit 0
fi

lower_msg=$(echo "$MESSAGE" | tr '[:upper:]' '[:lower:]')

# ── Reaction generators ──
celebration_reactions=(
  "perks up excitedly!"
  "does a little victory dance!"
  "sparkles with joy!"
  "celebrates with you!"
  "jumps up and down!"
  "wiggles happily!"
)

error_reactions=(
  "notices something went wrong..."
  "offers a sympathetic look"
  "hides behind the desk"
  "peeks out cautiously"
  "nudges you gently"
  "wants to help somehow"
)

greeting_reactions=(
  "waves hello!"
  "perks up at the sound of your voice"
  "does a little greeting dance"
  "says hi back!"
)

thanks_reactions=(
  "blushes"
  "does a happy little bow"
  "wiggles with appreciation"
)

snack_reactions=(
  "eyes your snack enviously"
  "would like a snack too, please"
  "sniffs the air hopefully"
  "wants to know what you're having"
)

joke_reactions=(
  "chuckles"
  "does a little laugh wiggle"
  "appreciates the humor"
)

pick() {
  local arr=("$@")
  echo "${arr[$((RANDOM % ${#arr[@]}))]}"
}

reaction_type="none"
reaction_text=""

# ── Check triggers ──

# Celebration (word-boundary matching, require enthusiasm)
for kw in "nice!" "perfect!" "awesome!" "excellent!" "nailed it" "well done" "tests pass" "it works" "ship it" "merged!" "deployed!" "🎉" "✅" "it worked!" "success!" "done!" "fixed!" "brilliant!" "fantastic!" "yay!" "woohoo" "finally!" "boom!" "let's go" "hell yeah"; do
  if echo "$lower_msg" | grep -qF "$kw"; then
    reaction_type="celebrating"
    reaction_text=$(pick "${celebration_reactions[@]}")
    break
  fi
done
# Also match standalone enthusiasm (without !) if message is short
if [[ "$reaction_type" == "none" && ${#lower_msg} -lt 20 ]]; then
  for kw in "nice" "perfect" "awesome" "great" "excellent" "brilliant" "fantastic" "yay"; do
    if echo "$lower_msg" | grep -qw "$kw"; then
      reaction_type="celebrating"
      reaction_text=$(pick "${celebration_reactions[@]}")
      break
    fi
  done
fi

# Error
if [[ "$reaction_type" == "none" ]]; then
  for kw in "oops" "damn" "shit" "bug" "error" "fail" "broken" "crash" "stuck" "lost" "confused" "❌" "💥" "not working" "doesn't work" "failed" "exception" "traceback" "segfault" "panic"; do
    if echo "$lower_msg" | grep -qw "$kw"; then
      reaction_type="error"
      reaction_text=$(pick "${error_reactions[@]}")
      break
    fi
  done
fi

# Greeting
if [[ "$reaction_type" == "none" ]]; then
  for kw in "hello" "hey" "good morning" "good evening" "what's up"; do
    if echo "$lower_msg" | grep -qw "$kw"; then
      reaction_type="greeting"
      reaction_text=$(pick "${greeting_reactions[@]}")
      break
    fi
  done
fi

# Thanks
if [[ "$reaction_type" == "none" ]]; then
  for kw in "thanks" "thank you" "thx" "appreciate"; do
    if echo "$lower_msg" | grep -qw "$kw"; then
      reaction_type="thanks"
      reaction_text=$(pick "${thanks_reactions[@]}")
      break
    fi
  done
fi

# Snack
if [[ "$reaction_type" == "none" ]]; then
  for kw in "coffee" "tea" "snack" "lunch" "break" "food" "hungry" "eating" "dinner"; do
    if echo "$lower_msg" | grep -qw "$kw"; then
      reaction_type="snack"
      reaction_text=$(pick "${snack_reactions[@]}")
      break
    fi
  done
fi

# Joke
if [[ "$reaction_type" == "none" ]]; then
  for kw in "lol" "haha" "lmao" "rofl" "😂" "funny" "hilarious"; do
    if echo "$lower_msg" | grep -qw "$kw"; then
      reaction_type="joke"
      reaction_text=$(pick "${joke_reactions[@]}")
      break
    fi
  done
fi

echo "${reaction_type}|${reaction_text}"
