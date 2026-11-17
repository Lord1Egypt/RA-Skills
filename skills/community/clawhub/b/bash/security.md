# Security — Injection, Secrets, Privileges, Temp Files

The threat model for a shell script: any value the script did not write itself is potentially attacker-controlled — arguments, environment, filenames on disk, HTTP responses, git branch names, CI template variables. The whole discipline is keeping those values as DATA and never letting them become SYNTAX.

## Data Must Never Become Syntax

| Sink | Why it executes | Safe form |
|---|---|---|
| `eval "$cmd"` | Full shell parse of attacker text | An array plus `"${cmd[@]}"` (SKILL.md Core Rule 3) |
| `(( $n ))`, `arr[$n]` | Arithmetic contexts evaluate `a[$(cmd)]` — command substitution inside a subscript | Validate first: `[[ $n =~ ^[0-9]+$ ]] \|\| die` |
| `ssh host "cmd $v"` | The remote shell re-parses the string | `ssh host bash -s <<'EOF'` with values on stdin, or `printf '%q'` (`quoting.md`) |
| `sh -c "…$v…"`, `xargs sh -c` | Same second parse, locally | `sh -c 'f "$1"' _ "$v"` — the value arrives as `$1` |
| `awk "/$pat/"`, `jq ".$k"` | The value becomes part of the program | `awk -v p="$pat"`, `jq --arg k "$k" '.[$k]'` |
| `source "$file"` for config | A config file is executable code | Parse `key: value` lines yourself (`functions.md`) |
| `bash <(curl …)`, `curl … \| sh` | Executes whatever the server returns, including a truncated download | Download, verify a published checksum or signature, inspect, then run |

- Validate with an ALLOWLIST, never a denylist: `[[ $env == @(dev|staging|prod) ]] || die` beats trying to strip dangerous characters
- Length-bound anything that becomes part of a filename or a command line — an argument list is finite (`debugging.md`)
- Treat a value's TYPE as part of its validation: integers by regex, paths by canonicalization plus a prefix check, identifiers by `^[A-Za-z0-9_-]+$`

## Path Confinement

```bash
base=/srv/data
real=$(cd -- "$base" && cd -- "$(dirname -- "$user_path")" 2>/dev/null && pwd -P)/$(basename -- "$user_path")
[[ $real == "$base"/* ]] || die "path escapes $base: $user_path"
```

- `../../etc/passwd` and an absolute path both defeat naive concatenation; resolve to a physical path and check the prefix AFTER resolving, with the trailing slash in the pattern so `/srv/data-evil` does not pass
- Symlinks inside the tree can point out of it: for untrusted trees add `-P` semantics everywhere and consider `find … -type l -prune`
- Filenames beginning with `-` become options (`quoting.md`); filenames containing terminal escapes attack whoever reads your logs — print names with `printf '%q'`

## Secrets

- Argv is world-readable: `mysql -p"$pass"`, `curl -u user:"$pass"`, and `aws --secret …` are visible in `ps` to every local user. Use stdin, a config file with mode 0600, or an environment variable
- The environment is readable by the same UID's processes and appears in crash dumps and in `/proc/<pid>/environ`; it is better than argv, worse than a file descriptor
- `set -x` prints every value (`ci.md`); `PS4` output goes to stderr and straight into logs. Bracket credential handling with `set +x` … `set -x`
- Never write a secret into the repo, a temp file in `/tmp`, or a log line — and remember that `set -e` failures print the failing command in many CI wrappers
- History: a script does not touch `~/.bash_history`, but the human who tested the command by hand did. Advise `HISTCONTROL=ignorespace` and a leading space, or rotate the credential
- Give every fetched credential a lifetime: a short-lived token that leaks costs an hour, a static key costs until someone notices

## Temp Files Are A Public Space

- `/tmp` is world-writable and shared: `/tmp/myjob.$$` is guessable, and an attacker can pre-create it as a symlink so your write lands in their target. `mktemp` creates with mode 0600 and a random name, atomically — always use it (`files.md`)
- Never `chmod 777` a temp path to "fix permissions"; set the umask (`umask 077`) before creating instead
- Do the whole job inside one `mktemp -d` you own, and delete the directory in a trap. Working directly in `/tmp` means every intermediate is another race
- On multi-user hosts prefer `$TMPDIR` when it points somewhere per-user, and never assume `/tmp` is private on shared CI runners

## Privileges

- Check, do not assume: `(( EUID == 0 ))` for "must be root", and the inverse for scripts that must NOT run as root (a script that creates files as root breaks the user's tree)
- Setuid on a shell script does nothing on Linux — the kernel ignores it, and every workaround (wrapper binaries, `sudo` shims) is a privilege-escalation surface. Grant a narrow `sudo` rule for one exact command instead
- Sudo rules should name the binary and its arguments, never `ALL` and never a shell. `NOPASSWD: /usr/bin/systemctl restart app.service` is a rule; `NOPASSWD: /bin/bash` is a root shell for anyone who can run the script
- Escalate as late and as narrowly as possible: run the script as the unprivileged user and `sudo` the one command that needs it, rather than running the whole thing as root
- `sudo` resets the environment (`env_reset`, `secure_path`): pass what is needed explicitly, and remember the redirection is done by YOUR shell (→ SKILL.md Traps)
- PATH is an attack surface when it contains `.` or a user-writable directory: set `PATH` explicitly at the top of any privileged script, and call critical binaries by absolute path

## Fetching Things From The Network

- `curl -fsSL` — `-f` makes HTTP errors nonzero (without it, a 404 body is happily piped onward), `-sS` keeps the error message but drops the progress bar
- Verify before executing: download to a temp file, check `sha256sum -c` against a checksum you obtained separately, then run. A checksum published on the same page you downloaded from proves only integrity, not authenticity
- Pin versions and digests. "Latest" means "whatever the vendor pushed while you slept", and a compromised upstream reaches every host on the next run
- Set timeouts (`--max-time`, `--connect-timeout`) and a bounded retry; an unbounded retry loop against a failing endpoint is a self-inflicted outage

## Reviewing Someone Else's Script

Read in this order: the shebang and `set` line, then every `eval`, `sudo`, `rm -rf`, `curl`, and `>`; then where each variable in those lines comes from. That ordering finds the destructive and injectable paths in a minute, without reading the logic at all.
