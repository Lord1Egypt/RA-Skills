# Portability — macOS vs GNU, Old Bash, POSIX sh, WSL

Two different portability problems get conflated. One is the SHELL (which bash version, or not bash at all — SKILL.md Version Floors). The other is the TOOLS (BSD vs GNU coreutils), and it bites scripts that never use a single bashism.

## Decide The Target Before Writing

| Target set | Write | Cost |
|---|---|---|
| Linux servers and CI only | bash 5, GNU tools, no hedging | Breaks on a colleague's Mac |
| Linux + macOS developer laptops | bash 3.2-compatible syntax OR require Homebrew bash in the header, intersection of tool flags | ~10% more code |
| Containers with `/bin/sh` = busybox/dash | POSIX sh: no arrays, no `[[ ]]`, no `${var^^}`, no process substitution | Rewrite, not a port |
| Anything a user might run anywhere | bash 3.2 + POSIX tool flags + runtime capability checks | Highest; justify it |

Record the answer in the header comment and in `bash_floor`/`target_os` (SKILL.md Configuration) so reviewers apply the same rule.

## The Shell Itself

- macOS `/bin/bash` is 3.2 forever (GPLv3). `#!/usr/bin/env bash` picks up a Homebrew bash 5 at `/opt/homebrew/bin/bash` if it is on PATH; `#!/bin/bash` never will
- Enforce, do not hope: `((BASH_VERSINFO[0] >= 4)) || die "needs bash 4+ (brew install bash)"` at the top beats a `bad substitution` on line 200
- Debian/Ubuntu `/bin/sh` is dash, not bash: a script with `#!/bin/sh` that uses `[[ ]]`, arrays, or `<<<` fails only on those systems. `checkbashisms` or `shellcheck -s sh` finds them
- Alpine images ship busybox `ash` and often no bash at all — `#!/bin/bash` gives "no such file or directory" even though the file exists (that message refers to the interpreter)
- What breaks first on bash 3.2, in observed order: `mapfile`, `declare -A`, `${var^^}`, `${arr[-1]}`, `declare -n`, `&>>`, `;&`. Fallbacks for each are in the guides for arrays and expansion

## GNU vs BSD Tool Flags

| Task | GNU (Linux) | BSD (macOS) | Portable |
|---|---|---|---|
| In-place edit | `sed -i 's/a/b/' f` | `sed -i '' 's/a/b/' f` | temp file + `mv` (`files.md`) |
| Extended regex | `sed -E` / `grep -E` | same | `-E` (avoid `-r`, GNU-only) |
| PCRE match | `grep -P` | not available | `grep -E`, or `perl -ne` |
| Date arithmetic | `date -d '+1 day' +%F` | `date -v+1d +%F` | `python3 -c`, or branch on `date --version` |
| Epoch to date | `date -d @1700000000` | `date -r 1700000000` | branch |
| File size | `stat -c %s f` | `stat -f %z f` | `wc -c < f` |
| Resolve path | `readlink -f p` | (newer only) `readlink -f p` | `cd "$(dirname p)" && pwd -P` |
| Checksum | `sha256sum f` | `shasum -a 256 f` | detect once, alias into a variable |
| Base64 one line | `base64 -w0` | `base64` (already one line) | `base64 \| tr -d '\n'` |
| Skip empty input | `xargs -r` | implicit (and `-r` may be rejected) | `find … -exec cmd {} +` |
| CPU count | `nproc` | `sysctl -n hw.ncpu` | `getconf _NPROCESSORS_ONLN` |
| Reverse a file | `tac` | `tail -r` | `awk '{a[NR]=$0} END{for(i=NR;i;i--) print a[i]}'` |
| Timeout | `timeout 30 cmd` | `gtimeout`, or none | the watchdog pattern in `processes.md` |
| find printf | `find -printf '%p\n'` | not available | `find … -exec stat …` or `-print` |

- Detect once, at the top, and store the choice — never branch inside a loop:
  ```bash
  if sed --version >/dev/null 2>&1; then SED_INPLACE=(sed -i); else SED_INPLACE=(sed -i ''); fi
  "${SED_INPLACE[@]}" 's/a/b/' file          # array, so the empty argument survives (SKILL.md Core Rule 3)
  ```
- Homebrew's coreutils installs GNU versions prefixed with `g` (`gsed`, `gdate`, `gstat`); a script may prefer them when present: `SED=$(command -v gsed || command -v sed)`
- macOS ships bsdtar as `tar` (GNU flags mostly work) and BSD `awk` (no gawk extensions — `text-processing.md`)
- macOS filesystems are case-insensitive by default: `File.txt` and `file.txt` are the same file there and two files on Linux. Any script that generates filenames from user data must assume collisions

## Downgrading To POSIX sh

Only when the target genuinely contains dash or busybox (SKILL.md Where Experts Disagree). The mechanical translation:

| bash | POSIX sh |
|---|---|
| `[[ $a == $b ]]` | `[ "$a" = "$b" ]` — quote everything, no pattern matching |
| `arr=(a b); "${arr[@]}"` | positional parameters: `set -- a b; "$@"` |
| `$(( ))` | same (POSIX), but no `++`/`**` |
| `local x` | `local` is not POSIX but works in dash and ash; document the assumption |
| `<<< "$s"` | `printf '%s\n' "$s" \|` |
| `<(cmd)` | temp file, or restructure the pipeline |
| `set -o pipefail` | not in dash — check exit codes stage by stage through temp files |
| `${var^^}` | `printf '%s' "$var" \| tr '[:lower:]' '[:upper:]'` |
| `source f` | `. f` |
| `function f {}` | `f() {}` |

Verify with `shellcheck -s sh script` AND by actually running it under `dash script` — the linter finds syntax, the run finds behavior.

## Windows: WSL, Git Bash, CRLF

- CRLF is the number one Windows-origin bug: `$'\r': command not found`, `bad interpreter`, and conditions that mysteriously never match because the value ends in `\r`. Fix at the source with `.gitattributes` (`*.sh text eol=lf`), not with a `tr -d '\r'` in every script
- Git Bash (MSYS2) rewrites arguments that look like paths: `curl -H /api` may arrive as a Windows path. Disable per invocation with `MSYS_NO_PATHCONV=1`
- WSL and Windows share files but not permissions: a script on `/mnt/c` often shows mode 0777 and cannot be made executable — keep repos inside the Linux filesystem
- Line-ending and permission damage travels through git: `git config core.autocrlf false` on the Linux side of a shared repo, and `git update-index --chmod=+x script.sh` when the exec bit is lost

## Capability Checks Over Version Checks

Prefer asking whether the feature exists to asking what version is installed — versions lie in containers and on patched distributions:

```bash
command -v jq >/dev/null || die "jq required"
printf 'x' | grep -qP 'x' 2>/dev/null && has_pcre=1 || has_pcre=0
(( BASH_VERSINFO[0] > 4 || (BASH_VERSINFO[0] == 4 && BASH_VERSINFO[1] >= 4) )) && has_inherit=1
```

Cache each answer in a variable at startup: capability probes are forks, and a probe inside a loop is the accidental slowdown described in `performance.md`.
