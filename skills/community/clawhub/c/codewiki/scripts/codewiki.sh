#!/usr/bin/env bash
#
# codewiki.sh — Clone a GitHub repository and generate a wiki from it using
#               the `codewiki` CLI. Designed to be invoked either directly by
#               a human or programmatically by an external AI Agent.
#
# Usage:
#   ./codewiki.sh -r <repo> [-o <output>] [-i "<instructions>"] \
#                 [--render <mkdocs|vitepress|both>] [--serve [PORT]]
#
# Exit codes:
#   0  Success — wiki generated under <output>/<repo>/wiki
#   1  Usage error (missing/invalid arguments)
#   2  Dependency missing (bash, git, or codewiki)
#   3  Clone/pull failure
#   4  codewiki generation failure
#   5  Render failure (render_docs.sh non-zero exit)
#
# --------------------------------------------------------------------------- #

# -----------------------------------------------------------------------------
# Strict-mode shell options so the script fails fast and predictably.
# -e  : exit immediately if any command exits with non-zero status.
# -u  : treat unset variables as an error when substituted.
# -o pipefail : propagate the failure of any command inside a pipeline.
# -----------------------------------------------------------------------------
set -euo pipefail

# -----------------------------------------------------------------------------
# Globals. We keep them in one place so they're easy to audit. Default values
# are intentionally minimal — every override must come from a CLI flag.
# -----------------------------------------------------------------------------
REPOSITORY=""          # Parsed value of -r/--repository. Required.
OUTPUT_DIR="."         # Parsed value of -o/--output. Defaults to CWD.
INSTRUCTIONS=""        # Parsed value of -i/--instructions. Optional.
HAVE_INSTRUCTIONS=0    # 1 if -i was passed; keeps quoting logic explicit.
RENDER_STACK=""        # Parsed value of --render. Empty = skip rendering.
HAVE_RENDER=0          # 1 if --render was passed; distinguishes "" from absent.
SERVE=0                # 1 if --serve was passed (only valid with --render).
SERVE_PORT=""          # Optional port value parsed after --serve.

# -----------------------------------------------------------------------------
# Script metadata, used by --help and --version-style introspection.
# -----------------------------------------------------------------------------
SCRIPT_NAME="codewiki.sh"
SCRIPT_VERSION="1.1.0"

# -----------------------------------------------------------------------------
# print_help()
# Prints a clean, agent-readable help banner. The formatting is intentionally
# predictable: a brief synopsis, then a flag table, then examples. Agents can
# scrape this with simple regex.
# -----------------------------------------------------------------------------
print_help() {
  cat <<'HELP'
codewiki.sh — Clone a repo and generate a wiki with the `codewiki` CLI.

SYNOPSIS
  codewiki.sh -r <repository> [-o <output_dir>] [-i "<instructions>"]
              [--render <mkdocs|vitepress|both>] [--serve [PORT]]
  codewiki.sh -h | --help

DESCRIPTION
  Clones (or pulls) the target Git repository into an output directory, then
  invokes `codewiki generate` to produce a wiki under <output>/<repo>/wiki.

  Repository (-r) accepts two forms:
    1. "<group>/<repository>"           -> expanded to
       https://github.com/<group>/<repository>.git
    2. "https://..." or "git@..."       -> used verbatim as the clone URL.

  When --render is supplied, the sibling `render_docs.sh` is invoked after the
  wiki is generated, turning the Markdown into a static MkDocs and/or VitePress
  site. Rendered sites land under <output>/<repo>/mkdocs and/or
  <output>/<repo>/vitepress.

OPTIONS
  -r, --repository <repo>     (Required) Repo shorthand or full clone URL.
  -o, --output <dir>           (Optional) Destination directory. Created with
                              `mkdir -p` if missing. Defaults to ".".
  -i, --instructions <text>   (Optional) Free-form instructions passed
                              verbatim to `codewiki generate --instructions`.
      --render <stack>        (Optional) Render the generated wiki with the
                              sibling render_docs.sh. <stack> must be one of
                              `mkdocs`, `vitepress`, or `both`. Omit to skip
                              rendering entirely.
      --serve [PORT]          (Optional) After rendering, start a static HTTP
                              server on the built site(s). Requires --render.
                              PORT defaults to 8000; when <stack>=both,
                              MkDocs is served on PORT and VitePress on PORT+1.
                              The server runs in the foreground; Ctrl-C stops.
  -h, --help                  Show this help and exit.

EXAMPLES
  # Shorthand repo, default output dir:
  codewiki.sh -r anthropics/claude-code

  # Full URL, custom output, with instructions:
  codewiki.sh -r https://github.com/foo/bar.git \
              -o ./work/bar \
              -i "Focus on the auth module; skip vendored code."

  # Generate + render both stacks, then serve on port 3000:
  codewiki.sh -r foo/bar --render both --serve 3000

EXIT CODES
  0  Success          1  Usage error
  2  Missing dep      3  Clone/pull failure
  4  Generation failure    5  Render failure
HELP
}

# -----------------------------------------------------------------------------
# die <exit_code> <message>
# Print an error to stderr and exit with the given code. Centralized so every
# failure path looks identical and is easy for an agent to parse.
# -----------------------------------------------------------------------------
die() {
  local code="$1"
  shift
  printf '\033[31m[error]\033[0m %s\n' "$*" >&2
  exit "$code"
}

# -----------------------------------------------------------------------------
# log <message>
# Informational stdout line, prefixed so agents can separate it from the
# codewiki tool's own output.
# -----------------------------------------------------------------------------
log() {
  printf '\033[36m[codewiki.sh]\033[0m %s\n' "$*"
}

# -----------------------------------------------------------------------------
# check_dependencies()
# Fail fast if the runtime environment is missing required tools. This is the
# "strict" mode: every dependency is verified before any side-effecting
# command runs.
#   - git       : needed to clone/pull.
#   - codewiki  : the actual wiki generator. We assume it is on $PATH.
# Returns 0 if all present; exits with code 2 and a message otherwise.
# -----------------------------------------------------------------------------
check_dependencies() {
  local missing=()

  # Bash is implicit (we're running in it), so we skip a self-check.
  command -v git      >/dev/null 2>&1 || missing+=( "git" )
  command -v codewiki >/dev/null 2>&1 || missing+=( "codewiki" )

  if (( ${#missing[@]} > 0 )); then
    printf '\033[31m[error]\033[0m Missing required dependencies: %s\n' \
        "${missing[*]}" >&2
    printf '  - git:      install from https://git-scm.com/\n' >&2
    printf '  - codewiki: install per your project instructions\n' >&2
    exit 2
  fi
}

# -----------------------------------------------------------------------------
# normalize_repository <raw>
# Translate the user-supplied -r value into a normalized full clone URL and
# echo it to stdout. Two accepted shapes:
#   1. "<group>/<repository>"  — e.g. "anthropics/claude-code".
#      Expanded to https://github.com/<group>/<repository>.git
#   2. Anything starting with "https://" or "git@" — passed through as-is.
# Exits with code 1 if neither shape matches.
# -----------------------------------------------------------------------------
normalize_repository() {
  local raw="$1"

  # Case 2: already a full URL — accept https:// or git@...: forms verbatim.
  if [[ "$raw" == https://* || "$raw" == git@* ]]; then
    printf '%s' "$raw"
    return 0
  fi

  # Case 1: shorthand "group/repo". Validate the shape loosely:
  #   - must contain exactly one '/'
  #   - neither side may be empty
  #   - no whitespace
  if [[ "$raw" == */* && "$raw" != */*/* && "$raw" != /* && "$raw" != */ \
        && "$raw" != *" "* ]]; then
    printf 'https://github.com/%s.git' "$raw"
    return 0
  fi

  # Reject anything else with a useful diagnostic.
  die 1 "Invalid repository '$raw'. Use '<group>/<repo>' or a full https:// / git@ URL."
}

# -----------------------------------------------------------------------------
# derive_repo_dirname <clone_url>
# Compute the on-disk directory name for a clone from a URL. Handles both
# HTTPS and SSH URL forms and strips a trailing ".git" if present.
#   "https://github.com/g/r.git"   -> "r"
#   "git@github.com:g/r.git"       -> "r"
# Echoes the derived name to stdout.
# -----------------------------------------------------------------------------
derive_repo_dirname() {
  local url="$1"
  local name

  # Drop everything up to the final '/' (HTTPS) or ':' (SSH) so we're left
  # with "<repo>[.git]". We strip the longest prefix matching either
  # character class.
  name="${url##*/}"

  # Strip an optional trailing ".git".
  name="${name%.git}"

  # Defensive: if the URL had no path component, fall back to a safe name.
  printf '%s' "${name:-repo}"
}

# -----------------------------------------------------------------------------
# clone_or_pull <clone_url> <dest>
# Ensure the repository is checked out at <dest>.
#   - If <dest> is a git repo, run `git pull` to refresh it.
#   - Otherwise, `git clone --depth 1` into <dest> (shallow, default branch).
# Exits with code 3 on any failure.
# -----------------------------------------------------------------------------
clone_or_pull() {
  local url="$1"
  local dest="$2"

  # `.git` presence is the canonical "is this a working clone?" check.
  if [[ -d "$dest/.git" ]]; then
    log "Existing clone found at '$dest'; pulling latest."
    # -C runs git as if cwd were $dest; we avoid `cd` for predictable state.
    if ! git -C "$dest" pull --ff-only; then
      die 3 "git pull failed in '$dest'. Resolve conflicts or remove the directory."
    fi
  else
    # --depth 1  : shallow clone, default branch only. Fast and small.
    # We do NOT pass --no-single-branch: codewiki needs the working tree,
    # not history, so the default branch tip is sufficient.
    log "Cloning (shallow) '$url' into '$dest'."
    if ! git clone --depth 1 "$url" "$dest"; then
      die 3 "git clone failed for '$url'."
    fi
  fi
}

# -----------------------------------------------------------------------------
# run_codewiki <repo_dir> <instructions> <have_instructions>
# Invoke `codewiki generate` inside the cloned repo. We build the argument
# list as a Bash array so any whitespace, quotes, or shell metacharacters in
# the instructions are preserved verbatim — no eval, no re-quoting.
#   - Always emits --output ./wiki (relative to the repo dir).
#   - Adds --instructions "<text>" only when provided.
# Exits with code 4 if codewiki returns non-zero.
# -----------------------------------------------------------------------------
run_codewiki() {
  local repo_dir="$1"
  local instr="$2"
  local have="$3"

  # Build argv safely. Arrays keep each token as a single argv element,
  # sidestepping word-splitting entirely.
  local args=( "generate" "--output" "./wiki" )
  if (( have )); then
    args+=( "--instructions" "$instr" )
  fi

  log "Running: codewiki ${args[*]@Q}  (cwd: $repo_dir)"
  # Run from inside the repo so ./wiki lands where we want it.
  if ! ( cd "$repo_dir" && codewiki "${args[@]}" ); then
    die 4 "codewiki generation failed."
  fi

  log "Wiki written to: $repo_dir/wiki"
}

# -----------------------------------------------------------------------------
# render_docs <wiki_dir> <repo_dir> <stack> <serve> <serve_port>
# Invoke the sibling `render_docs.sh` to turn the generated Markdown wiki
# into a static MkDocs and/or VitePress site. Rendered outputs are co-located
# with the wiki under <repo_dir>/mkdocs and <repo_dir>/vitepress so the whole
# pipeline stays self-contained.
#
#   --src         : the wiki directory produced by run_codewiki.
#   --stack       : passed through verbatim from --render (already validated).
#   --mkdocs-out  : <repo_dir>/mkdocs
#   --vitepress-out: <repo_dir>/vitepress
#   --serve [PORT]: forwarded only when --serve was supplied.
#
# Exits with code 5 if render_docs.sh is missing/non-executable or returns
# non-zero. The --serve case blocks in the foreground until Ctrl-C; that
# happens inside render_docs.sh, so we just propagate its exit status.
# -----------------------------------------------------------------------------
render_docs() {
  local wiki_dir="$1"
  local repo_dir="$2"
  local stack="$3"
  local serve="$4"
  local serve_port="$5"

  # Resolve the sibling render_docs.sh relative to this script so the wrapper
  # works no matter where it's invoked from.
  local script_path
  script_path="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/render_docs.sh"
  if [[ ! -x "$script_path" ]]; then
    die 5 "render_docs.sh not found or not executable at: $script_path"
  fi

  # Build argv as an array to preserve verbatim quoting of every value.
  local args=(
    "--src"      "$wiki_dir"
    "--stack"    "$stack"
    "--mkdocs-out"    "$repo_dir/mkdocs"
    "--vitepress-out" "$repo_dir/vitepress"
  )
  if (( serve )); then
    args+=( "--serve" )
    # Optional port: only append when explicitly provided as a number.
    if [[ -n "$serve_port" ]]; then
      args+=( "$serve_port" )
    fi
  fi

  log "Running: $script_path ${args[*]@Q}"
  if ! "$script_path" "${args[@]}"; then
    die 5 "render_docs.sh failed."
  fi
}

# -----------------------------------------------------------------------------
# parse_args "$@"
# Consume CLI arguments into the global REPOSITORY / OUTPUT_DIR /
# INSTRUCTIONS / HAVE_INSTRUCTIONS slots. Supports both short (-r) and long
# (--repository) forms, and --help / -h. Calls die(1) on any malformed input,
# including the "naked command" case where no args are passed at all.
# -----------------------------------------------------------------------------
parse_args() {
  # GNU-style option parsing via getopts is awkward with long flags, so we
  # hand-roll the loop. This is more readable for an agent auditing the code.
  while (( $# > 0 )); do
    case "$1" in
      -r|--repository)
        # Require a value; guard against a trailing flag or end-of-args.
        if [[ -z "${2:-}" || "$2" == -* ]]; then
          die 1 "Option '$1' requires a value."
        fi
        REPOSITORY="$2"
        shift 2
        ;;
      -o|--output)
        if [[ -z "${2:-}" || "$2" == -* ]]; then
          die 1 "Option '$1' requires a value."
        fi
        OUTPUT_DIR="$2"
        shift 2
        ;;
      -i|--instructions)
        if [[ -z "${2:-}" ]]; then
          # Note: we allow a literal empty string if the caller quotes it.
          # If the next token is another flag, treat instructions as missing.
          die 1 "Option '$1' requires a value."
        fi
        INSTRUCTIONS="$2"
        HAVE_INSTRUCTIONS=1
        shift 2
        ;;
      --render)
        # --render takes a required value: mkdocs | vitepress | both.
        if [[ -z "${2:-}" || "$2" == -* ]]; then
          die 1 "Option '$1' requires a value (mkdocs, vitepress, or both)."
        fi
        case "$2" in
          mkdocs|vitepress|both) ;;
          *)
            die 1 "Invalid --render value '$2'. Use mkdocs, vitepress, or both."
            ;;
        esac
        RENDER_STACK="$2"
        HAVE_RENDER=1
        shift 2
        ;;
      --serve)
        # --serve takes an optional port. Peek at the next token: if it is a
        # positive integer we consume it as the port; otherwise we leave it
        # for the next iteration. This mirrors render_docs.sh's own parser.
        SERVE=1
        if [[ "${2:-}" =~ ^[0-9]+$ ]]; then
          SERVE_PORT="$2"
          shift 2
        else
          shift
        fi
        ;;
      -h|--help)
        print_help
        exit 0
        ;;
      --)
        # End-of-options sentinel. Any remaining args are ignored — we have
        # no positional args to accept.
        shift
        break
        ;;
      -*)
        die 1 "Unknown option: '$1'. See -h for usage."
        ;;
      *)
        die 1 "Unexpected positional argument: '$1'. See -h for usage."
        ;;
    esac
  done

  # Required-arg guard. This is what handles the "naked command" case.
  if [[ -z "$REPOSITORY" ]]; then
    printf '\n' >&2
    print_help >&2
    die 1 "Missing required option: -r/--repository."
  fi

  # Cross-option validation: --serve only makes sense alongside --render.
  if (( SERVE )) && (( ! HAVE_RENDER )); then
    die 1 "--serve requires --render. Specify --render <mkdocs|vitepress|both> first."
  fi
}

# -----------------------------------------------------------------------------
# main()
# Orchestrate the full workflow in explicit, auditable steps.
# -----------------------------------------------------------------------------
main() {
  parse_args "$@"

  # Step 1: fail fast on missing tools before touching the filesystem.
  check_dependencies

  # Step 2: resolve the user's -r into a canonical clone URL.
  local clone_url
  clone_url="$(normalize_repository "$REPOSITORY")"
  log "Repository URL: $clone_url"

  # Step 3: ensure the output directory exists. `mkdir -p` is idempotent and
  # creates intermediate dirs as needed.
  if [[ ! -d "$OUTPUT_DIR" ]]; then
    log "Output directory does not exist; creating '$OUTPUT_DIR'."
    mkdir -p "$OUTPUT_DIR"
  fi

  # Step 4: compute the destination path inside OUTPUT_DIR.
  local repo_name repo_dir
  repo_name="$(derive_repo_dirname "$clone_url")"
  repo_dir="$OUTPUT_DIR/$repo_name"
  log "Repository directory: $repo_dir"

  # Step 5: get the code onto disk (clone or pull).
  clone_or_pull "$clone_url" "$repo_dir"

  # Step 6: generate the wiki.
  run_codewiki "$repo_dir" "$INSTRUCTIONS" "$HAVE_INSTRUCTIONS"

  # Step 7 (optional): render the generated Markdown into static sites.
  if (( HAVE_RENDER )); then
    render_docs "$repo_dir/wiki" "$repo_dir" "$RENDER_STACK" \
                "$SERVE" "$SERVE_PORT"
  fi

  log "Done."
}

# -----------------------------------------------------------------------------
# Entry point. Only execute main() when the script is run directly, not when
# it's being sourced (e.g. for unit testing its functions).
# -----------------------------------------------------------------------------
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
