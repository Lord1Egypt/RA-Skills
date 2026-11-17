# Interactive Scripts — Prompts, TTY, Color, Progress

Every interactive feature must degrade to nothing when the script runs from cron, CI, or a pipe. The test is one line, and it belongs before any prompt or escape sequence: `[[ -t 0 ]]` for input, `[[ -t 1 ]]` for output.

## Detect Before You Decorate

```bash
interactive=0; [[ -t 0 && -t 1 ]] && interactive=1
color=0; [[ -t 1 && -z ${NO_COLOR:-} && ${TERM:-dumb} != dumb ]] && color=1
```

- A prompt with no TTY hangs forever — the single most common cause of a cron job that never finishes (`cron.md`)
- Respect `NO_COLOR` (any non-empty value means "no ANSI") and `--no-color`; hardcoded escape codes turn CI logs into `ESC[0;32m` noise
- `TERM=dumb` (many CI runners, some editors' terminals) means no cursor control at all — no spinners, no line rewrites
- Non-interactive default must be the SAFE one: unattended runs proceed only for read-only work and abort for anything destructive unless `--yes` was passed (`destructive_confirm`)

## Prompting

```bash
read -r -p "Target host: " host              # -p prompt goes to stderr-ish tty, -r keeps backslashes
read -rs -p "Password: " pass; echo          # -s no echo; print the newline yourself
read -r -t 30 -p "Continue? " answer || die "timed out waiting for input"
read -r -n 1 -p "Press any key" _            # -n 1 returns after one character
```

- Always `-r`. Without it a backslash in the answer is an escape character
- `read` returns nonzero on EOF and on timeout — under `set -e` that ends the script silently unless you handle it, which is the correct behavior for a piped run
- Prompts belong on stderr when stdout is data: `read -r -p` writes the prompt to stderr already for a terminal, but a prompt you print yourself must be `>&2`
- Never accept a secret as a command-line argument: `ps` shows the full command line to every user on the box. `read -rs`, an environment variable, or a file (`security.md`)

## Confirmation That Cannot Be Fat-Fingered

```bash
confirm() {                                   # confirm "message" — default NO
  local reply
  [[ ${assume_yes:-0} == 1 ]] && return 0
  [[ -t 0 ]] || return 1                      # no TTY = no consent
  read -r -p "$1 [y/N] " reply
  [[ ${reply,,} == y || ${reply,,} == yes ]]  # bash >=4.0; on 3.2 use a case statement
}
confirm "Delete $count objects from $bucket?" || die "aborted"
```

- Default no, and make the answer type-out-able only for the dangerous direction: for irreversible operations require the resource name (`read -r name; [[ $name == "$bucket" ]]`)
- Show the exact scope in the question — the count and the target — because that is the only moment a human can catch a wrong variable
- One confirmation per run, at the top, not per item: a prompt inside a loop trains users to hold Enter

## Menus

`select` builds a numbered menu in four lines and handles redisplay:

```bash
PS3="Choose an environment: "
select env in dev staging prod; do
  [[ -n $env ]] && break
  echo "invalid choice" >&2
done
```

- `select` loops until an explicit `break`; an empty `$env` means the user typed something outside the range
- It reads from stdin, so it is unusable inside a `while read` loop over the same stream — pass the loop's input on another descriptor (`redirection.md`)
- More than about ten options belongs to a filter tool (`fzf`) or a flag, not to a menu

## Color and Styling

```bash
if (( color )); then
  bold=$(tput bold); red=$(tput setaf 1); green=$(tput setaf 2); reset=$(tput sgr0)
else
  bold= red= green= reset=
fi
printf '%sOK%s %s\n' "$green" "$reset" "$msg"
```

- `tput` reads terminfo, so it works on terminals where hardcoded `\033[…` codes do not, and it degrades to empty strings when `TERM` is unusable
- Define the variables once and always emit them; the "no color" branch sets them empty, so there is a single printf path instead of two
- Color is redundancy, never information: prefix `OK`/`FAIL` words too, or the output is meaningless in a log file
- Reset at the end of every line — an unterminated attribute bleeds into the user's prompt after the script exits

## Progress

- Single-line update: `printf '\r%-60s' "$msg"` overwrites; end with `printf '\n'` or the shell prompt lands mid-line. Only under `(( color ))`/TTY conditions — a `\r` in a log file produces an unreadable single line
- For a known total, a percentage beats a spinner: `printf '\r[%3d%%] %s' "$(( done * 100 / total ))" "$item"` — integer arithmetic, no fork
- Long unattended jobs print a line per completed item instead; a CI log wants append-only records, not animation
- Hide the cursor only if you restore it on every exit path: `tput civis; trap 'tput cnorm' EXIT`, or a Ctrl-C leaves the user's terminal without a cursor
- `pv` gives byte-level progress for pipelines for free when it is installed; check with `command -v pv` and fall back silently

## Terminal Hygiene

- Width for formatting: `${COLUMNS:-$(tput cols 2>/dev/null || echo 80)}` — `COLUMNS` is not exported to scripts by default
- Anything that changes terminal state (`stty -echo`, raw mode, alternate screen) needs a restoring trap on EXIT, INT, and TERM; `stty -g` saves the full state and `stty "$saved"` restores it exactly
- `clear` between screens destroys scrollback the user may need — reserve it for full-screen TUIs
- When output is not a TTY, emit plain machine-readable text (TSV) and let `column -t` beautify only in the interactive branch (`text-processing.md`)
