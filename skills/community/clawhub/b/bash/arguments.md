# Arguments — Flags, getopts, Usage, Subcommands

Argument handling is where scripts leak: a missing quote here silently drops an empty argument, a missing default silently processes the wrong path. Parse once, validate immediately, then never touch `$@` again.

## The Positional Basics

- `$#` count · `$1`…`$9`, `${10}` beyond nine · `"$@"` all arguments as separate words · `"$*"` all joined with the first char of IFS
- `shift` consumes `$1`; `shift 2` consumes two and FAILS (status 1) if there are fewer — under `set -e` that ends the script, so guard: `shift 2 || die "missing value"`
- `set -- a b c` replaces the positional list; `set -- "${defaults[@]}" "$@"` is how you prepend defaults
- `$0` is how the script was invoked, not where it lives — for the script's own directory use `${BASH_SOURCE[0]}` (`files.md`)
- Forwarding: `cmd "$@"` passes arguments through unchanged, including empty ones; `cmd $*` destroys both properties

## getopts (short options, POSIX, built in)

```bash
usage() { printf 'usage: %s [-v] [-o FILE] [-n COUNT] TARGET...\n' "${0##*/}"; }
verbose=0 out=- count=1
while getopts ':vo:n:h' opt; do
  case $opt in
    v) verbose=1 ;;
    o) out=$OPTARG ;;
    n) count=$OPTARG ;;
    h) usage; exit 0 ;;
    :) printf 'option -%s needs a value\n' "$OPTARG" >&2; usage >&2; exit 2 ;;
    \?) printf 'unknown option -%s\n' "$OPTARG" >&2; usage >&2; exit 2 ;;
  esac
done
shift $((OPTIND - 1))          # mandatory: leaves only the operands in "$@"
(( $# >= 1 )) || { usage >&2; exit 2; }
```

- The leading `:` in the optstring turns on SILENT error mode — without it getopts prints its own message and you lose control of the wording and of the `:` branch
- Forgetting `shift $((OPTIND - 1))` is the classic bug: the flags stay in `"$@"` and get processed as filenames
- `OPTIND` is global; reset it (`local OPTIND=1`) before parsing inside a function, or the second call parses nothing
- getopts handles `-vo file`, `-o file`, and `-ofile`; it does NOT handle long options, and it stops at the first non-option argument, so options must precede operands

## Long Options Without getopt(1)

`getopt(1)` supports `--long` but the BSD version shipped on macOS does not (SKILL.md Where Experts Disagree). Hand-rolled loop, portable and explicit:

```bash
while (( $# )); do
  case $1 in
    -v|--verbose)  verbose=1 ;;
    -o|--output)   out=${2:?--output needs a value}; shift ;;
    --output=*)    out=${1#*=} ;;
    --dry-run)     dry=1 ;;
    --no-color)    color=0 ;;
    -h|--help)     usage; exit 0 ;;
    --)            shift; break ;;          # everything after is an operand
    -*)            printf 'unknown option: %s\n' "$1" >&2; exit 2 ;;
    *)             operands+=("$1") ;;      # allow flags after operands
  esac
  shift
done
set -- "${operands[@]+"${operands[@]}"}" "$@"
```

- Support both `--output FILE` and `--output=FILE`: users type whichever their last tool used
- Handle `--` explicitly, or a filename starting with `-` can never be passed
- Negatable pairs (`--color`/`--no-color`) beat a `--color=true` value whose truthiness every tool spells differently

## Validate At The Boundary

- Every value coming from a flag is a string until proven otherwise: `[[ $count =~ ^[0-9]+$ ]] || die "…"` before it reaches `(( ))` (SKILL.md Core Rule 8)
- Check mutually exclusive combinations once, after parsing: `(( quiet && verbose ))` is an argument error (exit 2), not a runtime surprise 40 lines later
- Resolve defaults from config and environment in a documented precedence — flag > environment variable > config file > built-in default — and print the effective values under `--verbose`
- Fail on unknown options rather than ignoring them: a typo'd `--dyr-run` that is silently dropped runs the destructive version

## Usage And Exit Codes

- `--help` prints to STDOUT and exits 0; a usage error prints to STDERR and exits 2. Getting this backwards breaks `./script --help | less` and every CI check
- The usage line is the contract: `usage: script [-v] [-o FILE] TARGET...` — brackets optional, `...` repeatable, uppercase placeholders
- No arguments at all: print usage and exit 2 for tools that require operands; print help and exit 0 only for tools whose no-arg behavior is genuinely "show help"
- Keep `usage()` next to the parser so the two cannot drift; a `--help` that lists a flag the parser rejects is worse than no help

## Subcommands

```bash
cmd=${1:-}; shift || true
case $cmd in
  deploy)  cmd_deploy "$@" ;;
  status)  cmd_status "$@" ;;
  ''|-h|--help) usage ;;
  *) printf 'unknown command: %s\n' "$cmd" >&2; usage >&2; exit 2 ;;
esac
```

- Global flags before the subcommand, subcommand flags after — parse them in two passes, exactly as `git` does; a single flat parser makes `deploy --force` ambiguous with a global `--force`
- One function per subcommand named `cmd_<name>`, each with its own `usage_<name>`; dispatch stays a table someone can read
- Keep the dispatch `case` and the help text generated from the same list when the tool grows past a handful of subcommands

## Reading Operands

- `-` conventionally means stdin: `[[ $file == - ]] && file=/dev/stdin`
- No operands and stdin is not a terminal → read stdin (the filter convention): `[[ -t 0 ]] || set -- -`
- Expanding a user-supplied glob is the caller's shell's job, not yours — accept the already-expanded list in `"$@"` and iterate `for f in "$@"`, never re-glob the string
