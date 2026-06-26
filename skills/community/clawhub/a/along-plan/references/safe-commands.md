# Bash Command Safety Reference for Plan Mode

In plan mode, bash is restricted to read-only commands only.
A command is safe only when it matches a SAFE pattern AND does NOT match a DESTRUCTIVE pattern.

---

## SAFE Commands (Allowed)

These command prefixes are allowed in plan mode:

### File Reading
- `cat`, `head`, `tail`, `less`, `more`, `bat`
- `file`, `stat`, `wc`

### Search & Navigation
- `grep`, `rg` (ripgrep), `fd`, `find`
- `ls`, `exa`, `tree`, `pwd`

### Text Processing (read-only)
- `echo`, `printf`
- `sort`, `uniq`, `diff`
- `awk`, `sed -n` (sed with -n flag only — no writes)
- `jq`

### System Info
- `uname`, `whoami`, `id`, `date`, `cal`, `uptime`
- `env`, `printenv`
- `ps`, `top`, `htop`, `free`
- `du`, `df`
- `which`, `whereis`, `type`

### Git (read-only)
- `git status`
- `git log`
- `git diff`
- `git show`
- `git branch` (listing only)
- `git remote`
- `git config --get`
- `git ls-files`, `git ls-tree`

### Package Info (read-only)
- `npm list`, `npm ls`, `npm view`, `npm info`, `npm search`, `npm outdated`, `npm audit`
- `yarn list`, `yarn info`, `yarn why`, `yarn audit`

### Network (read-only)
- `curl` (GET requests)
- `wget -O -` (output to stdout only)

### Version Checks
- `node --version`, `python --version`, any `--version` flag

---

## DESTRUCTIVE Commands (Blocked)

These patterns are always blocked, even if they appear inside a safe-looking command:

### File System Mutations
- `rm`, `rmdir`
- `mv`, `cp`
- `mkdir`, `touch`
- `chmod`, `chown`, `chgrp`
- `ln`, `tee`, `truncate`, `dd`, `shred`
- Any redirection: `>file`, `>>file` (output redirect)

### Package Management (writes)
- `npm install/uninstall/update/ci/link/publish`
- `yarn add/remove/install/publish`
- `pnpm add/remove/install/publish`
- `pip install/uninstall`
- `apt/apt-get install/remove/purge/update/upgrade`
- `brew install/uninstall/upgrade`

### Git (writes)
- `git add`, `git commit`, `git push`, `git pull`
- `git merge`, `git rebase`, `git reset`
- `git checkout` (switching branches)
- `git branch -d` / `git branch -D`
- `git stash`, `git cherry-pick`, `git revert`
- `git tag`, `git init`, `git clone`

### System Control
- `sudo`, `su`
- `kill`, `pkill`, `killall`
- `reboot`, `shutdown`
- `systemctl start/stop/restart/enable/disable`
- `service <name> start/stop/restart`

### Editors (interactive)
- `vim`, `vi`, `nano`, `emacs`, `code`, `subl`

---

## Decision Rule

```
isSafe = NOT any(DESTRUCTIVE_PATTERN matches command)
       AND any(SAFE_PATTERN matches command)
```

When unsure: do NOT run the command. Describe what it would show instead.
