# Processes — Jobs, Signals, Timeouts, Parallelism

Bash is a process orchestrator. Everything here is about the three things it does badly by default: knowing whether a child succeeded, stopping one that will not finish, and running several without melting the box.

## Background Jobs and Their Exit Codes

```bash
cmd &                 # start
pid=$!                # capture IMMEDIATELY — $! is overwritten by the next &
wait "$pid"           # returns THAT job's exit code; without wait you never learn it
```

- `wait` with no argument returns 0 after all children finish, hiding every failure. Waiting per-PID is the only way to attribute a failure to a job
- Collect statuses when starting many:
  ```bash
  declare -A pid_of
  for h in "${hosts[@]}"; do deploy "$h" & pid_of[$!]=$h; done
  rc=0
  for p in "${!pid_of[@]}"; do wait "$p" || { printf 'FAILED %s\n' "${pid_of[$p]}" >&2; rc=1; }; done
  exit "$rc"
  ```
- `wait -n` (`bash >=4.3`) returns as soon as ANY child exits — the primitive for a fixed-size worker pool
- A background job inherits stdout: two jobs writing to the same terminal interleave mid-line. Give each one its own log file, or a `tee` with a prefix
- Backgrounded pipelines: `$!` is the PID of the LAST element; the earlier stages are separate children you cannot wait on individually

## Signals

- `trap 'cleanup' INT TERM` catches Ctrl-C and orderly stops; `kill -9` (SIGKILL) is uncatchable, which is why cleanup must also be idempotent (`errors.md`)
- Exit codes report signals as 128+n: 130 = Ctrl-C, 143 = TERM, 137 = KILL (SKILL.md Exit Codes). A handler that exits 0 lies to the caller — `trap 'cleanup; exit 130' INT`
- While a foreground child runs, bash defers the trap until that child returns. A script that must react instantly runs the child in the background and `wait`s — `wait` IS interruptible by a trap
- Ignore a signal deliberately with `trap '' INT` (empty string), and restore with `trap - INT`. Note an ignored signal stays ignored in children, which can make them unkillable
- Sending: `kill -TERM "$pid"` targets one process; `kill -TERM -- -"$pgid"` (note the dash) targets the whole process group — the way to stop a child that spawned its own children
- Escalate, do not start with SIGKILL: TERM, wait a few seconds, then KILL. Killing first skips the child's own cleanup and leaves the mess for you

## Passing Signals Through: exec

`exec cmd` REPLACES the shell process instead of forking a child. Two consequences worth designing for:

- A wrapper script that ends in `exec "$@"` makes the real program the process the supervisor sees — it receives SIGTERM directly, so container and systemd stops work. Without `exec`, the shell is PID 1, does not forward signals by default, and the stop takes the full grace period
- After `exec`, nothing later in the script runs and no EXIT trap fires; do all setup before it

## Timeouts

- `timeout 30 cmd` exits 124 on expiry, 125 if `timeout` itself failed (SKILL.md Exit Codes)
- `timeout -k 5 30 cmd` sends TERM at 30 s and KILL 5 s later — the correct default for anything that may ignore TERM
- macOS has no `timeout` unless coreutils is installed (`gtimeout`); a portable fallback:
  ```bash
  cmd & pid=$!
  ( sleep 30; kill -TERM "$pid" 2>/dev/null ) & watcher=$!
  wait "$pid"; rc=$?; kill "$watcher" 2>/dev/null; wait "$watcher" 2>/dev/null
  ```
- Anything touching the network gets a timeout at the tool level too (`curl --max-time`, `ssh -o ConnectTimeout=`), because a TCP connect can hang far longer than your patience
- `read -t 5` bounds a read that may never receive input; it returns >128 on timeout

## Parallelism Without a Framework

```bash
# N workers, NUL-safe, one command per input, stops the batch on first failure
find . -name '*.png' -print0 | xargs -0 -P 8 -n 1 -- optimize.sh
```

- `-P N` sets concurrency; `-n 1` one argument per invocation. Without `-n`/`-I`, xargs packs as many arguments as fit and `-P` has almost nothing to parallelize
- Pick N from the bottleneck, not from the core count: CPU-bound → `nproc` (or `sysctl -n hw.ncpu`); network-bound → higher, bounded by the remote's rate limits; disk-bound on spinning media → 1-2
- xargs has its own exit-code scale, unrelated to `timeout`'s above: 123 if any invocation exited 1-125, 124 if one exited 255, 125 if one was killed by a signal, 126 not executable, 127 not found — check it, since the individual failures scroll past
- Output from parallel workers interleaves. Either write per-item files and concatenate at the end, or use `xargs -P … | cat` only for whole-line output under the pipe-buffer size
- Pure-bash pool with `wait -n` (`bash >=4.3`) when xargs cannot express the work:
  ```bash
  max=4
  for item in "${items[@]}"; do
    while (( $(jobs -pr | wc -l) >= max )); do wait -n; done
    work "$item" &
  done
  wait
  ```
- GNU `parallel` adds ordered output (`--keep-order`), retries, and remote execution; the dependency is worth it exactly when you need those, not as a default

## Detaching and Long Runs

- `nohup cmd &` survives a hangup but still shares the terminal's session; `setsid cmd` starts a new session, fully detached
- `disown -h %1` removes a running job from the shell's SIGHUP list without stopping it — the fix when you forgot `nohup`
- Neither survives a machine restart. Anything that must, belongs to a service manager or a scheduler (`cron.md`)
- A script that intends to run once at a time needs a lock, not a PID file check (`redirection.md`)

## Inspecting What Is Running

- `jobs -l` (this shell's children with PIDs), `pgrep -f 'pattern'` (match the full command line), `ps -o pid,ppid,stat,etime,args -p "$pid"`
- `pgrep -f` matching your own script is a classic self-detection bug: the grep pattern matches the checking process too — exclude it with `pgrep -f "pattern" | grep -v "^$$\$"` or, better, use a lock
- `$$` is the script's PID and does NOT change inside a subshell; `$BASHPID` (`bash >=4.0`) is the real current PID — the distinction matters when a subshell writes a PID file
- A child whose parent exits is re-parented to init and keeps running: killing the script does not kill its background jobs unless you trap and kill them yourself:
  ```bash
  trap 'kill 0' EXIT      # kill 0 = the whole process group, children included
  ```
