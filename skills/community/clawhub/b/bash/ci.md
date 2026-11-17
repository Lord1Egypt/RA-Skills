# Scripts Inside CI Runners

A CI step is a fresh, non-interactive shell on a machine that will be destroyed. Three consequences drive everything below: no state carries over, nothing is a TTY, and the only evidence you will ever have is what the log captured.

## Each Step Is A New Shell

- Nothing persists between steps except the filesystem: not `cd`, not exported variables, not shell options, not background jobs. Persist deliberately — write to a file, or to the provider's env-file mechanism
- Strict mode does not carry over either. Every multi-line step starts with `set -euo pipefail`, or put the whole thing in a checked-in script and let the step call it (the version you can lint and test locally — `testing.md`)
- Providers differ in the shell they wrap around your block: GitHub Actions runs `run:` with `bash -e {0}` by default on Linux and macOS and only adds `pipefail` when you write `shell: bash` explicitly; GitLab uses `sh` in many images unless you set it. Confirm yours and stop guessing which flags you inherited
- The step's exit status is the LAST command's status. A step ending in `echo done` reports success no matter what happened above it — the reason `-e` and explicit checks matter more here than locally

## Non-Interactive Or It Hangs

- No TTY: every prompt is an infinite hang that ends as a job timeout with no useful log
- `apt-get install -y` plus `DEBIAN_FRONTEND=noninteractive`, `npm ci` not `npm install`, `git` with `GIT_TERMINAL_PROMPT=0`
- SSH: `-o BatchMode=yes -o ConnectTimeout=10` and a known_hosts entry provisioned in advance. `StrictHostKeyChecking=no` trades a hang for a silent man-in-the-middle window — pin the host key instead
- `TERM` is usually unset or `dumb`: no `tput`, no spinners, no `\r` progress (`interactive.md`)
- Wrap anything network-facing in `timeout` so a hang fails in 60 s with a message instead of at the job limit 45 minutes later (`processes.md`)

## Secrets

- Masking is substring matching on the log stream. It fails on transformed values: base64, URL-encoded, uppercased, or a multi-line secret printed one line at a time — the mask never fires and the value is in the log forever
- `set -x` prints every expansion, secrets included. Wrap credential handling in `set +x` … `set -x`, and never enable tracing job-wide "just for this debug run"
- Never pass a secret as a command-line argument: it is visible in `ps`, in crash dumps, and in any provider that echoes the command. Use an environment variable or a file with mode 0600
- Interpolating provider template variables into a shell block is a shell-injection hole: a value like a pull-request title becomes code. Bind it to an environment variable and reference `"$TITLE"` inside the script — the value never touches the shell parser
- Secrets are not available to pull requests from forks on most providers, by design. A pipeline that "works on main and fails on PRs" is usually this, not your script

## Reproduce Locally Before Debugging In A Loop

- Run the same container image the runner uses: `docker run --rm -it -v "$PWD:/w" -w /w <image> bash` — most "only fails in CI" bugs are a different image, not a different runner
- The environment delta is the diagnosis: `diff <(env | sort) <(ssh runner env | sort)`, or print `env | sort` in a step with secrets masked
- Push-to-test cycles cost minutes each. Extract the step into `scripts/ci-build.sh`, make it runnable on a laptop, and let the pipeline call it — that single move converts a 6-minute loop into a 6-second one
- Keep the debug artifacts: upload logs and the workspace listing on failure, because the machine is gone the moment the job ends

## Filesystem And Path Assumptions

- The workspace path differs per provider and per runner type; never hardcode `/home/runner/work/...`. Use the provider's variable or `${BASH_SOURCE[0]}`-relative resolution (`files.md`)
- Container jobs run as root with a different `$HOME`; a script caching in `~/.cache` writes somewhere unexpected and misses the cache every run
- The filesystem is ephemeral but shared BETWEEN steps of the same job: state written in step 2 is visible in step 5, and stale state from an earlier step is a real source of false passes
- Self-hosted runners are the opposite: state survives between JOBS. Anything that assumes a clean tree must clean it explicitly, and any lock or temp path must be unique per job

## Failure Modes That Only Appear In CI

- Timing: parallel jobs share one CPU quota, so a race that never triggers on a laptop triggers on every third build. Fix the race; retries hide it
- The job timeout kills the process group without running EXIT traps — cleanup that only exists in a trap never happens. Make external resources self-expiring (TTL tags, lifecycle rules) rather than relying on cleanup
- Rate limits and registry throttling look like random network failures; authenticate pulls and cache dependencies before adding retries
- `git` in a shallow clone (`fetch-depth: 1`) has no history: `git describe`, `git log`, and diff-against-base all fail. Request the depth you need
- Locale and timezone are C/UTC on runners and something else on your laptop — sort order and date formatting differ (`text-processing.md`)

## Making Logs Answerable

```bash
run_step() {                        # run_step "label" cmd...
  local label=$1; shift
  printf '::: %s\n' "$label"
  local start=$SECONDS
  "$@" || { printf '::: FAILED %s after %ds\n' "$label" "$(( SECONDS - start ))" >&2; return 1; }
  printf '::: ok %s (%ds)\n' "$label" "$(( SECONDS - start ))"
}
```

- Label and time each phase: the duration line is what makes "the pipeline got slower" diagnosable months later
- Print the versions of the tools that matter at the start of the job (`bash --version`, the language runtime, the CLI); half of "it broke overnight" is an upgraded runner image
- Echo the effective configuration once (flags, target, branch) — not the secrets — so a failed run can be reproduced exactly from its own log
