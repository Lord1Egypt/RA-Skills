# Files — Paths, Globs, Temp Files, Atomic Writes

Everything in this file exists because filenames are arbitrary bytes, directories are shared state, and a script that dies halfway must not leave a half-written file behind.

## Where Am I, Where Is The Script

```bash
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)   # physical dir of THIS file
```

- `$0` is how the script was invoked (`bash script.sh`, a symlink, a PATH lookup) — `${BASH_SOURCE[0]}` is the file being executed and is also correct inside a sourced library
- `pwd -P` resolves symlinks; `pwd` (logical) keeps the path the user typed. Pick `-P` for anything you will compare or delete
- `realpath`/`readlink -f` are GNU and modern-BSD; the `cd && pwd -P` idiom needs nothing and works on bash 3.2
- Never build paths by string concatenation with a trailing-slash guess: `"$dir/$file"` is correct even when `dir` ends in `/` (POSIX collapses `//`), but `"$dir$file"` silently concatenates names
- Relative paths break the moment the script runs from cron or a CI runner (`$HOME` and the workspace root are different) — resolve to absolute once, at the top

## Globs

- `shopt -s nullglob` — a non-matching glob expands to nothing instead of to its own literal text. Without it, `for f in *.txt` in an empty directory processes a file literally named `*.txt`
- `shopt -s failglob` — a non-matching glob is an ERROR. Right for a script where a missing input is a bug; wrong for optional sets
- `shopt -s dotglob` — include dotfiles. `*` never matches `.` or `..`, but it also never matches `.env` without this
- `shopt -s globstar` (`bash >=4.0`) — `**/` recurses; note `**` follows symlinked directories, so a symlink loop makes it hang. For large trees `find` is faster and interruptible
- `shopt -s nocaseglob` for case-insensitive matching; remember macOS filesystems are usually case-INSENSITIVE, so `Makefile` and `makefile` collide there and not on Linux
- Set these per script, not per user: options are not inherited by scripts (`debugging.md`)
- Quoting kills globbing: `ls "$dir/*.txt"` looks for a file whose name contains an asterisk. The variable is quoted, the pattern is not: `ls "$dir"/*.txt`

## find Without Surprises

- Order matters: `find . -name '*.log' -mtime +7 -delete` applies tests left to right; `-delete` implies `-depth`, and putting it before a filter deletes everything
- Quote the pattern — an unquoted `-name *.log` is expanded by the shell first and `find` sees a filename
- `-exec cmd {} +` batches (one process for many files, like xargs); `-exec cmd {} \;` runs once per file. Use `+` unless the command takes exactly one argument
- `-print0 | xargs -0` for hostile names; `-exec … +` is already safe and needs no NUL
- `-prune` skips a subtree: `find . -name .git -prune -o -name '*.sh' -print` — the `-o -print` is required or you get the pruned entries too
- `-mtime +7` means strictly more than 7×24 h ago and truncates fractions; `-mmin +N` gives minute resolution when the boundary matters
- Depth limits before filters: `find . -maxdepth 2 -type f` — cheap, and it keeps a stray mount out of the traversal

## Temp Files

```bash
tmp=$(mktemp) || die "mktemp failed"                       # file
dir=$(mktemp -d) || die "mktemp -d failed"                 # directory
trap 'rm -rf "$tmp" "$dir"' EXIT                           # the next line, always
```

- Never hardcode `/tmp/myscript.$$`: the PID is predictable and the file may already exist as a symlink pointing somewhere fatal (`security.md`)
- Portable template: `mktemp "${TMPDIR:-/tmp}/myjob.XXXXXX"` — GNU accepts a bare `-t prefix`, BSD/macOS wants the template; the explicit form works on both
- `mktemp -d` in the same directory as the final destination when you plan to `mv` into place — a rename across filesystems is a copy and is no longer atomic
- Large intermediates belong in `$TMPDIR`, not next to the source; on many hosts `/tmp` is tmpfs (RAM) and a multi-GB spill turns into memory pressure

## Atomic Writes

```bash
out=/etc/app/config.yaml
tmp=$(mktemp "$(dirname "$out")/.config.XXXXXX")
render_config > "$tmp"
chmod 0644 "$tmp"          # mktemp creates 0600; set the mode you actually want
mv -f -- "$tmp" "$out"     # rename is atomic within one filesystem
```

- Readers see either the old file or the new one, never a truncated one. `> "$out"` gives them a window of empty file at every run
- The same pattern makes a script re-runnable: a crash leaves an orphan dot-file, never a corrupt target
- Durability beyond the rename (surviving a power cut) needs `sync`; for config and build artifacts the rename alone is the honest guarantee

## Deleting Without Regret

- `rm -rf "${dir:?}/"` aborts when `dir` is empty or unset (→ SKILL.md Traps); make it a habit, not a special case
- Delete by construction, not by pattern: build the list with `find` first, print it under `--dry-run`, delete on the second pass with the same expression
- `rm -- "$f"` for names that may start with a dash; `rm -f` for idempotent cleanup so a second run does not fail
- Deleting inside a directory you do not own is a race with whoever else writes there — do destructive work inside your own `mktemp -d`

## Copying and Syncing

- `cp -a` preserves mode, ownership, timestamps and symlinks (GNU); BSD equivalent is `cp -Rp`. Plain `cp -r` silently resets permissions and follows symlinks
- `rsync -a src/ dst/` copies the CONTENTS of src; `rsync -a src dst/` creates `dst/src`. The trailing slash is the entire semantics — put a comment on the line
- `rsync --dry-run --itemize-changes` before any destructive `--delete`; the itemized output is the review artifact
- Preserve hard links and sparse files explicitly (`rsync -aH --sparse`) — a VM image copied without them can multiply in size

## Ownership, Modes, and Space

- `umask` decides the mode of every file the script creates; a service manager's umask differs from your shell's, so set it explicitly (`umask 077`) when the output is sensitive
- `install -m 0644 -D src dst` creates parent directories, sets the mode, and copies in one atomic-ish step — cleaner than `mkdir -p && cp && chmod`
- Check space before a large write, and check the RIGHT filesystem: `df -Pk "$(dirname "$out")" | awk 'NR==2{print $4}'` gives free KB (`-P` forces one line per filesystem, defeating long-device-name wrapping)
- Inodes run out before bytes on caches full of small files: `df -i` is the second check when writes fail on a disk that looks empty
