#!/usr/bin/env bash
# Post-migration fixes, run INSIDE nextcloud/data/USER/files:
#   1. convert .heic/.HEIC/.heif images to .jpg (heif-convert);
#      originals removed only after a verified non-empty output
#   2. give extensionless files an extension from `file` MIME detection
# Modes:
#   (default)       dry-run: print the plan, change nothing
#   --apply         execute everything (office/text/zip only with --auto-office)
#   --interactive   ask per file: y=do it, n=skip, a=all remaining, q=quit;
#                   unknown types: type an extension by hand (needs a terminal)
# Collisions get -1/-2 suffixes, never overwrites.
# Run as the Nextcloud system user (YunoHost: nextcloud, bare Debian: www-data).
set -euo pipefail

APPLY=0 AUTO_OFFICE=0 INTERACTIVE=0 AUTO_ALL=0 STOP=0
for a in "$@"; do
  case $a in
    --apply) APPLY=1 ;;
    --auto-office) AUTO_OFFICE=1 ;;
    -i|--interactive) INTERACTIVE=1 ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "unknown option: $a" >&2; exit 2 ;;
  esac
done
if [ "$INTERACTIVE" -eq 1 ]; then
  if ! { : > /dev/tty; } 2>/dev/null; then
    echo "--interactive needs a terminal (tty); use dry-run or --apply instead" >&2
    exit 2
  fi
fi

case "$PWD" in
  /|"$HOME") echo "refusing to run in $PWD - cd into nextcloud/data/USER/files first" >&2; exit 2 ;;
esac
[[ "$PWD" == */files ]] || echo "WARNING: $PWD does not look like a USER/files dir - double-check." >&2
command -v file >/dev/null 2>&1 || { echo "'file' is not installed" >&2; exit 1; }

DIR_OWNER=""
if [ "$(id -u)" -eq 0 ]; then
  DIR_OWNER=$(stat -c '%u:%g' .)
  echo "WARNING: running as root; new files chowned to $DIR_OWNER (dir owner). Prefer sudo -u <nextcloud-user>." >&2
fi
own() { if [ -n "$DIR_OWNER" ]; then chown "$DIR_OWNER" "$1"; fi; }

n_heic=0 n_ext=0 n_skip=0
failures=()
manual=()

unique_target() { # $1 desired path -> first free path (name-1.ext, name-2.ext...)
  local t=$1 stem ext n=1
  if [ ! -e "$t" ]; then printf '%s\n' "$t"; return; fi
  stem=${t%.*}; ext=${t##*.}
  while [ -e "$stem-$n.$ext" ]; do n=$((n+1)); done
  printf '%s\n' "$stem-$n.$ext"
}

ext_for_mime() {
  case $1 in
    image/jpeg) echo jpg ;;
    image/png) echo png ;;
    image/gif) echo gif ;;
    image/webp) echo webp ;;
    image/tiff) echo tif ;;
    image/bmp) echo bmp ;;
    image/x-icon|image/vnd.microsoft.icon) echo ico ;;
    application/pdf) echo pdf ;;
    image/heic|image/heif|image/heic-sequence|image/heif-sequence) echo HEIC ;;
    audio/mpeg) echo mp3 ;;
    audio/flac) echo flac ;;
    audio/x-wav|audio/vnd.wave) echo wav ;;
    video/mp4) echo mp4 ;;
    video/quicktime) echo mov ;;
    application/msword) echo doc ;;
    application/vnd.ms-excel) echo xls ;;
    application/vnd.ms-powerpoint) echo ppt ;;
    application/vnd.openxmlformats-officedocument.wordprocessingml.document) echo docx ;;
    application/vnd.openxmlformats-officedocument.spreadsheetml.sheet) echo xlsx ;;
    application/vnd.openxmlformats-officedocument.presentationml.presentation) echo pptx ;;
    application/vnd.oasis.opendocument.text) echo odt ;;
    application/vnd.oasis.opendocument.spreadsheet) echo ods ;;
    application/vnd.oasis.opendocument.presentation) echo odp ;;
    text/plain) echo txt ;;
    application/zip) echo zip ;;
    *) echo "" ;;
  esac
}
is_office() { case $1 in doc|xls|ppt|docx|xlsx|pptx|odt|ods|odp|txt|zip) return 0 ;; *) return 1 ;; esac; }

DECISION=plan
decide() { # $1 = description of the planned action -> DECISION=apply|plan|skip
  if [ "$STOP" -eq 1 ]; then DECISION=skip; return; fi
  if [ "$INTERACTIVE" -eq 1 ] && [ "$AUTO_ALL" -eq 0 ]; then
    local ans
    printf '%s\n  [y]es / [n]o / [a]ll remaining / [q]uit ? ' "$1" > /dev/tty
    IFS= read -r ans < /dev/tty || ans=q
    case $ans in
      y|Y|o|O) DECISION=apply ;;
      a|A) AUTO_ALL=1; DECISION=apply ;;
      q|Q) STOP=1; DECISION=skip ;;
      *) DECISION=skip ;;
    esac
  elif [ "$APPLY" -eq 1 ] || [ "$AUTO_ALL" -eq 1 ]; then
    DECISION=apply
  else
    DECISION=plan
  fi
}

heic_convert() { # $1 = source file (named *.heic/heif or extensionless HEIC)
  local src=$1 dir base out
  dir=$(dirname -- "$src"); base=$(basename -- "$src")
  case $base in *.*) base=${base%.*} ;; esac
  out=$(unique_target "$dir/$base.jpg")
  decide "HEIC->JPG  $src  ->  $out"
  case $DECISION in
    plan) echo "[dry] HEIC->JPG  $src  ->  $out"; n_heic=$((n_heic+1)); return 0 ;;
    skip) n_skip=$((n_skip+1)); return 0 ;;
  esac
  if ! command -v heif-convert >/dev/null 2>&1; then
    echo "[FAIL] heif-convert missing (apt install libheif-examples): $src"
    failures+=("$src"); return 0
  fi
  if heif-convert "$src" "$out" >/dev/null 2>&1 && [ -s "$out" ]; then
    own "$out"
    rm -- "$src"
    echo "[ok]  HEIC->JPG  $src  ->  $out"
    n_heic=$((n_heic+1))
  else
    rm -f -- "$out"
    echo "[FAIL] HEIC conversion: $src"
    failures+=("$src")
  fi
}

# ---- Phase 1: named HEIC/HEIF files ----
mapfile -d '' HEIC_FILES < <(find . -type f \( -iname '*.heic' -o -iname '*.heif' \) -print0)
if [ "${#HEIC_FILES[@]}" -gt 0 ] && ! command -v heif-convert >/dev/null 2>&1; then
  if [ "$APPLY" -eq 1 ] || [ "$INTERACTIVE" -eq 1 ]; then
    echo "heif-convert missing: apt install libheif-examples" >&2; exit 1
  fi
  echo "NOTE: heif-convert not installed (apt install libheif-examples); dry-run plan only." >&2
fi
for f in ${HEIC_FILES[@]+"${HEIC_FILES[@]}"}; do heic_convert "$f"; done

# ---- Phase 2: extensionless files ----
while IFS= read -r -d '' f; do
  if [ "$STOP" -eq 1 ]; then break; fi
  mime=$(file -b --mime-type -- "$f")
  ext=$(ext_for_mime "$mime")
  if [ "$ext" = "HEIC" ]; then heic_convert "$f"; continue; fi
  if [ -z "$ext" ] && [ "$INTERACTIVE" -eq 1 ] && [ "$AUTO_ALL" -eq 0 ]; then
    # didactic: show what `file` sees, let the user pick an extension
    printf 'unknown type: %s\n  %s\n  extension to add (letters/digits, empty=skip): ' "$f" "$(file -b -- "$f" | cut -c1-100)" > /dev/tty
    IFS= read -r ans < /dev/tty || ans=''
    if [[ "$ans" =~ ^[A-Za-z0-9]{1,8}$ ]]; then ext=$ans; fi
  fi
  if [ -z "$ext" ]; then
    manual+=("$f  [$mime]  $(file -b -- "$f" | cut -c1-100)")
    continue
  fi
  if is_office "$ext" && [ "$AUTO_OFFICE" -eq 0 ] && [ "$INTERACTIVE" -eq 0 ]; then
    manual+=("$f  [$mime]  office/text type: re-run with --auto-office or rename by hand")
    continue
  fi
  target=$(unique_target "$f.$ext")
  decide "+ext  $f  ->  $target  [$mime]"
  case $DECISION in
    plan) echo "[dry] +ext  $f  ->  $target" ;;
    skip) n_skip=$((n_skip+1)); continue ;;
    apply) mv -- "$f" "$target"; echo "[ok]  +ext  $f  ->  $target" ;;
  esac
  n_ext=$((n_ext+1))
done < <(find . -type f ! -name '*.*' -print0)

# ---- Report ----
MODE=DRY-RUN
if [ "$INTERACTIVE" -eq 1 ]; then MODE=INTERACTIVE; elif [ "$APPLY" -eq 1 ]; then MODE=APPLY; fi
REPORT=$(mktemp "${TMPDIR:-/tmp}/nc_fix_report.XXXXXX.txt")
{
  echo "== Nextcloud fix report $(date -Is) =="
  echo "dir: $PWD   mode: $MODE"
  echo "HEIC converted: $n_heic   extensions added: $n_ext   skipped: $n_skip   failures: ${#failures[@]}"
  if [ "${#failures[@]}" -gt 0 ]; then printf 'FAILED: %s\n' "${failures[@]}"; fi
  echo
  echo "-- Manual review (${#manual[@]}) --"
  if [ "${#manual[@]}" -gt 0 ]; then printf '%s\n' "${manual[@]}"; else echo "(none)"; fi
} | tee "$REPORT"

if [ "$APPLY" -eq 1 ] || [ "$INTERACTIVE" -eq 1 ]; then
  echo
  echo "NEXT: rescan as the Nextcloud user:"
  echo "  YunoHost: yunohost app shell nextcloud  ->  php occ files:scan --all"
  echo "  bare:     sudo -u www-data php /path/to/nextcloud/occ files:scan --all"
fi
[ "${#failures[@]}" -eq 0 ]
