#!/usr/bin/env bash
# Buddy Sprite Renderer — renders ASCII companion sprites
set -euo pipefail

eye_char() {
  case "$1" in
    default)  printf '•' ;;
    happy)    printf '^' ;;
    sparkle)  printf '✦' ;;
    heart)    printf '♥' ;;
    star)     printf '★' ;;
    glow)     printf '◎' ;;
    *)        printf '•' ;;
  esac
}

render_sprite() {
  local species="${1:-cat}" eye="${2:-default}" hat="${3:-none}" mood="${4:-idle}"
  local frame=$((RANDOM % 3)) e
  e=$(eye_char "$eye")

  if [[ "$hat" != "none" ]]; then
    case "$hat" in
      crown)     printf '   \\^^^/    \n' ;;
      tophat)    printf '   [___]    \n' ;;
      propeller) printf '    -+-     \n' ;;
      halo)      printf '   (   )    \n' ;;
      wizard)    printf '    /^\\     \n' ;;
      beanie)    printf '   (___)    \n' ;;
      tinyduck)  printf '    ,>      \n' ;;
    esac
  fi

  case "$species" in
    duck)
      case $frame in
        0) printf '    __     \n  <( %s )___\n   (  ._>  \n    ----   \n' "$e" ;;
        1) printf '    __     \n  <( %s )___\n   (  ._>  \n    ----~  \n' "$e" ;;
        2) printf '    __     \n  <( %s )___\n   (  .__> \n    ----   \n' "$e" ;;
      esac ;;
    goose)
      case $frame in
        0) printf '     ( %s> \n      ||    \n    _(__)_ \n    ^^^^   \n' "$e" ;;
        1) printf '    ( %s>  \n      ||    \n    _(__)_ \n    ^^^^   \n' "$e" ;;
        2) printf '     ( %s>>\n      ||    \n    _(__)_ \n    ^^^^   \n' "$e" ;;
      esac ;;
    blob)
      case $frame in
        0) printf '  .----.   \n ( %s  %s ) \n (      )  \n  --------  \n' "$e" "$e" ;;
        1) printf ' .------.  \n(  %s  %s  )\n(        ) \n --------  \n' "$e" "$e" ;;
        2) printf '   .--.    \n  (%s  %s)  \n  (    )   \n   ----    \n' "$e" "$e" ;;
      esac ;;
    cat)
      case $frame in
        0) printf '  /\\_/\\    \n ( %s  %s ) \n (  ω  )   \n (__) (__) \n' "$e" "$e" ;;
        1) printf '  /\\_/\\    \n ( %s  %s ) \n (  ω  )   \n (__) (__)\n' "$e" "$e" ;;
        2) printf '  /\\-/\\    \n ( %s  %s ) \n (  ω  )   \n (__) (__) \n' "$e" "$e" ;;
      esac ;;
    dragon)
      case $frame in
        0) printf ' /^\\  /^\\  \n<  %s  %s  >\n(   ~~   ) \n---vvvv---\n' "$e" "$e" ;;
        1) printf ' /^\\  /^\\  \n<  %s  %s  >\n(        ) \n---vvvv---\n' "$e" "$e" ;;
        2) printf ' /^\\  /^\\  \n<  %s  %s  >\n(   ~~   ) \n---vvvv---\n' "$e" "$e" ;;
      esac ;;
    octopus)
      case $frame in
        0) printf '  .----.   \n ( %s  %s ) \n (______)  \n /\\/\\/\\/\\/ \n' "$e" "$e" ;;
        1) printf '  .----.   \n ( %s  %s ) \n (______)  \n \\/\\/\\/\\/\\\n' "$e" "$e" ;;
        2) printf '  .----.   \n ( %s  %s ) \n (______)  \n /\\/\\/\\/\\/ \n' "$e" "$e" ;;
      esac ;;
    owl)
      case $frame in
        0) printf '  /\\  /\\   \n ((%s)(%s))\n (  ><  )  \n  --------  \n' "$e" "$e" ;;
        1) printf '  /\\  /\\   \n ((%s)(%s))\n (  ><  )  \n  .----.   \n' "$e" "$e" ;;
        2) printf '  /\\  /\\   \n ((%s)(-) )\n (  ><  )  \n  --------  \n' "$e" ;;
      esac ;;
    penguin)
      case $frame in
        0) printf ' .---.     \n (%s>%s)    \n/(   )\\   \n -----    \n' "$e" "$e" ;;
        1) printf ' .---.     \n (%s>%s)    \n|(   )|   \n -----    \n' "$e" "$e" ;;
        2) printf ' .---.     \n (%s>%s)    \n/(   )\\   \n -----    \n' "$e" "$e" ;;
      esac ;;
    turtle)
      case $frame in
        0) printf '  _,--._   \n ( %s  %s ) \n/[______]\\ \n..      ..\n' "$e" "$e" ;;
        1) printf '  _,--._   \n ( %s  %s ) \n/[______]\\ \n  ..  ..  \n' "$e" "$e" ;;
        2) printf '  _,--._   \n ( %s  %s ) \n/[======]\\ \n..      ..\n' "$e" "$e" ;;
      esac ;;
    snail)
      case $frame in
        0) printf '    .--.   \n  ( %s )  \n  \\_----  \n ~~~~~~~~ \n' "$e" ;;
        1) printf '   .--.    \n  | %s  )  \n  \\_----  \n ~~~~~~~~ \n' "$e" ;;
        2) printf '    .--.   \n  ( %s  )  \n  \\_----  \n  ~~~~~~  \n' "$e" ;;
      esac ;;
    ghost)
      case $frame in
        0) printf '  .----.   \n / %s  %s \\ \n |      |  \n ~~~~~~~~~ \n' "$e" "$e" ;;
        1) printf '  .----.   \n / %s  %s \\ \n |      |  \n ~~~~~~~~~ \n' "$e" "$e" ;;
        2) printf '  .----.   \n / %s  %s \\ \n |      |  \n ~~~~~~~~~ \n' "$e" "$e" ;;
      esac ;;
    axolotl)
      case $frame in
        0) printf '(________)\n(%s .. %s)\n ( .--. )  \n (_/  \\_) \n' "$e" "$e" ;;
        1) printf '(________)\n(%s .. %s)\n ( .--. )  \n (_/  \\_) \n' "$e" "$e" ;;
        2) printf '(________)\n(%s .. %s)\n (  --  )  \n ~_/  \\_~\n' "$e" "$e" ;;
      esac ;;
    capybara)
      case $frame in
        0) printf ' n______n \n( %s    %s)\n(   oo   )\n -------- \n' "$e" "$e" ;;
        1) printf ' n______n \n( %s    %s)\n(   Oo   )\n -------- \n' "$e" "$e" ;;
        2) printf ' u______n \n( %s    %s)\n(   oo   )\n -------- \n' "$e" "$e" ;;
      esac ;;
    cactus)
      case $frame in
        0) printf '   ____   \n  |%s  %s|  \n |_|    |_|\n   |    |  \n' "$e" "$e" ;;
        1) printf '   ____   \n  |%s  %s|  \n |_|    |_|\n   |    |  \n' "$e" "$e" ;;
        2) printf '   ____   \n  |%s  %s|  \n |_|    |_|\n   |    |  \n' "$e" "$e" ;;
      esac ;;
    robot)
      case $frame in
        0) printf '  .[||].  \n [ %s  %s ]\n [ ==== ] \n -------- \n' "$e" "$e" ;;
        1) printf '  .[||].  \n [ %s  %s ]\n [ -==- ] \n -------- \n' "$e" "$e" ;;
        2) printf '  .[||].  \n [ %s  %s ]\n [ ==== ] \n -------- \n' "$e" "$e" ;;
      esac ;;
    rabbit)
      case $frame in
        0) printf '  (\\__/)  \n ( %s  %s ) \n=(  ..  )=\n (__) (__) \n' "$e" "$e" ;;
        1) printf '  (|__/)  \n ( %s  %s ) \n=(  ..  )=\n (__) (__) \n' "$e" "$e" ;;
        2) printf '  (\\__/)  \n ( %s  %s ) \n=( .  . )=\n (__) (__) \n' "$e" "$e" ;;
      esac ;;
    mushroom)
      case $frame in
        0) printf '.-o-OO-o-.\n(__________)\n  |%s  %s|  \n  |____|   \n' "$e" "$e" ;;
        1) printf '.-O-oo-O-.\n(__________)\n  |%s  %s|  \n  |____|   \n' "$e" "$e" ;;
        2) printf '.-o-OO-o-.\n(__________)\n  |%s  %s|  \n  |____|   \n' "$e" "$e" ;;
      esac ;;
    chonk)
      case $frame in
        0) printf ' /\\    /\\  \n( %s    %s)\n(   ..   )\n -------- \n' "$e" "$e" ;;
        1) printf ' /\\    /|  \n( %s    %s)\n(   ..   )\n -------- \n' "$e" "$e" ;;
        2) printf ' /\\    /\\  \n( %s    %s)\n(   ..   )\n --------~\n' "$e" "$e" ;;
      esac ;;
    *)
      printf '  /\\_/\\    \n ( %s  %s ) \n (  ω  )   \n (__) (__) \n' "$e" "$e" ;;
  esac
}

render_egg() {
  local frame=$((RANDOM % 3))
  case $frame in
    0) printf '    .---.\n   (     )\n   (  ?  )\n   (     )\n    ----- \n' ;;
    1) printf '    .---.\n   (     )\n  ~(  ?  )~\n   (     )\n    ----- \n' ;;
    2) printf '    .---.\n (       )\n  (  ?  ) \n (       )\n    ----- \n' ;;
  esac
}

case "${1:-render}" in
  render)
    if [[ $# -lt 2 ]]; then
      state_file="$HOME/.openclaw/workspace/buddy-state.json"
      if [[ -f "$state_file" ]] && command -v jq &>/dev/null; then
        species=$(jq -r '.species // "cat"' "$state_file")
        eye=$(jq -r '.eye // "default"' "$state_file")
        hat=$(jq -r '.hat // "none"' "$state_file")
        mood=$(jq -r '.mood // "idle"' "$state_file")
        stage=$(jq -r '.stage // "egg"' "$state_file")
      else
        species="cat" eye="default" hat="none" mood="idle" stage="baby"
      fi
    else
      species="${2:-cat}" eye="${3:-default}" hat="${4:-none}" mood="${5:-idle}"
      stage="baby"
    fi
    if [[ "$stage" == "egg" ]]; then
      render_egg
    else
      render_sprite "$species" "$eye" "$hat" "$mood"
    fi
    ;;
  preview)
    species="${2:-cat}"
    printf '=== %s ===\n\nDefault (idle):\n' "$species"
    render_sprite "$species" default none idle
    printf '\nHappy (celebrating):\n'
    render_sprite "$species" happy none celebrating
    printf '\nSparkle (success):\n'
    render_sprite "$species" sparkle crown success
    ;;
  egg)
    render_egg
    ;;
  species)
    printf 'duck goose blob cat dragon octopus owl penguin turtle snail ghost axolotl capybara cactus robot rabbit mushroom chonk\n'
    ;;
  *)
    echo "Usage: sprites.sh render [species] [eye] [hat] [mood]"
    echo "       sprites.sh preview <species>"
    echo "       sprites.sh egg"
    echo "       sprites.sh species"
    exit 1
    ;;
esac
