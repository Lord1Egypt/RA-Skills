#!/usr/bin/env bash
# oce.sh — Dispatcher for the agentic_cli_coding skill.
# Routes subcommands to oce-*.sh scripts living next to it in scripts/.
#
# Invocation:
#   bash <skill>/scripts/oce.sh <command> [args]
#
# Or with the bin/ wrapper installed (via scripts/install.sh):
#   oce <command> [args]

set -euo pipefail

# Resolve our own location (follow symlinks)
_self="${BASH_SOURCE[0]:-$0}"
while [ -h "$_self" ]; do
  _dir="$(cd -P "$(dirname "$_self")" && pwd)"
  _self="$(readlink "$_self")"
  [[ "$_self" != /* ]] && _self="$_dir/$_self"
done
OCE_SCRIPTS="$(cd -P "$(dirname "$_self")" && pwd)"
OCE_HOME="$(cd -P "$OCE_SCRIPTS/.." && pwd)"
export OCE_HOME OCE_SCRIPTS

usage() {
  cat <<'EOF'
oce — Code editing for agentic coders

USAGE
  bash scripts/oce.sh <command> [options] [args]

DISCOVERY
  tree [--depth N] [path]                Project structure (skips noise dirs)
  find <pattern> [--type LANG] [path]    Multi-mode search with smart excludes
  grep-context <pattern> <file>          Grep with surrounding lines
  ast symbols <file>                     List functions/classes (JS/TS)

READING
  read <file>                            Whole file with line numbers
  read <file> --lines A:B                Specific range
  read <file> --around PATTERN [-c N]    N lines around first match

EDITING
  replace <file> --old STR --new STR     Exact string replacement (default: 1)
  insert  <file> --before-match P        Insert before first match
  insert  <file> --after-match P         Insert after first match
  insert  <file> --line N                Insert at specific line
  delete  <file> --lines A:B             Delete a range
  delete  <file> --match PATTERN         Delete every matching line
  patch apply <patchfile>                Apply unified diff (with rollback)
  patch create <file> < new              Generate diff against current file
  write   <file>                         Replace file contents from stdin

STRUCTURED EDITS (JS/TS)
  ast rename <file> --from N --to N      Rename identifier (scope-aware)
  ast extract <file> <symbol>            Print a function/class
  ast replace-symbol <file> <symbol>     Replace a function/class from stdin

VALIDATION & FORMAT
  validate <file>                        Auto-detect language & syntax-check
  format   <file> [--check]              Run language formatter (if available)
  diff     <file>                        Diff against last backup

SAFETY
  backup list [<file>]                   List backups
  backup restore <file> [--at N]         Restore Nth backup back (0 = newest)
  backup diff <file> [N]                 Diff vs Nth backup
  backup clean [DAYS]                    Remove backups older than DAYS (default 30)

TRANSACTIONS (multi-file atomic)
  transaction begin                      Print a fresh TXN_ID
  transaction status <txn>               Show files in transaction
  transaction validate <txn>             Validate every file in transaction
  transaction commit <txn>               Validate + finalize
  transaction rollback <txn>             Restore every file from snapshot
  transaction list                       Recent transactions

GLOBAL FLAGS
  --json                                 Machine-readable output
  --dry-run                              Show what would happen, change nothing
  --no-color                             Disable ANSI colors
  --txn <id>                             Run command inside an existing transaction

EXAMPLES
  bash scripts/oce.sh tree --depth 2
  bash scripts/oce.sh find "TODO" --type ts
  bash scripts/oce.sh replace config.js --old "old" --new "new"

See SKILL.md for the methodology and references/ for deeper docs.
EOF
}

if [ $# -eq 0 ]; then usage; exit 0; fi

CMD="$1"; shift
case "$CMD" in
  -h|--help|help)     usage ;;
  version|--version)  echo "oce 1.0.0" ;;
  read)               exec bash "$OCE_SCRIPTS/oce-read.sh" "$@" ;;
  write)              exec bash "$OCE_SCRIPTS/oce-write.sh" "$@" ;;
  replace)            exec bash "$OCE_SCRIPTS/oce-replace.sh" "$@" ;;
  insert)             exec bash "$OCE_SCRIPTS/oce-insert.sh" "$@" ;;
  delete)             exec bash "$OCE_SCRIPTS/oce-delete.sh" "$@" ;;
  patch)              exec bash "$OCE_SCRIPTS/oce-patch.sh" "$@" ;;
  find)               exec bash "$OCE_SCRIPTS/oce-find.sh" "$@" ;;
  grep-context)       exec bash "$OCE_SCRIPTS/oce-grep-context.sh" "$@" ;;
  tree)               exec bash "$OCE_SCRIPTS/oce-tree.sh" "$@" ;;
  validate)           exec bash "$OCE_SCRIPTS/oce-validate.sh" "$@" ;;
  format)             exec bash "$OCE_SCRIPTS/oce-format.sh" "$@" ;;
  diff)               exec bash "$OCE_SCRIPTS/oce-diff.sh" "$@" ;;
  backup)             exec bash "$OCE_SCRIPTS/oce-backup.sh" "$@" ;;
  transaction|txn)    exec bash "$OCE_SCRIPTS/oce-transaction.sh" "$@" ;;
  ast)                exec bash "$OCE_SCRIPTS/oce-ast.sh" "$@" ;;
  doctor)             exec bash "$OCE_SCRIPTS/oce-doctor.sh" "$@" ;;
  *)                  printf 'Unknown command: %s\n\n' "$CMD" >&2; usage >&2; exit 64 ;;
esac
