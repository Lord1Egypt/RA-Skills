# Local, CI, and "Works On My Machine"

Environment differences are the cheapest bugs to prevent and the most expensive to diagnose, because the failure appears in a place where you cannot use your tools.

**Before debugging an environment**, read `## Commands` and `## Gotchas` in `~/Clawic/data/developer/repos/<repo>.md`. The env var that must be set, the version pin, the seed step — someone already found them, and this is the section they are in.

## The Difference Ladder

When something works in one place and fails in another, walk this in order. Each step is a one-minute check, and the order is by frequency.

| # | Difference | How to check |
|---|---|---|
| 1 | Runtime version | Print the version in both places, from inside the process, not from the shell |
| 2 | Dependency versions | Diff the lockfile against what is installed; a stale local `node_modules`/`venv` is not the lockfile |
| 3 | Environment variables | Dump the set of names in both (never the values into a log) — the missing one is usually the answer |
| 4 | Working directory and relative paths | A path that resolves from the repo root fails from a subdirectory or a container |
| 5 | Filesystem case sensitivity | macOS and Windows are case-insensitive, Linux CI is not — an import with the wrong case works locally forever |
| 6 | Clock and timezone | CI runs in UTC; your machine does not. Date-boundary tests fail after 22:00 in some zones |
| 7 | Parallelism | CI runs tests in parallel or in a different order; shared state surfaces there first (`tests.md`) |
| 8 | Data volume and shape | Empty CI database vs your seeded local one; production scale vs both |
| 9 | Locale and encoding | Sorting, uppercasing, number and date formatting all depend on it |
| 10 | Network access and DNS | CI may have no outbound access, a proxy, or different resolution |
| 11 | Resources | CI containers have less memory and fewer cores; OOM and timeouts appear only there |
| 12 | Build vs source | You are running a stale artifact somewhere (`bugs.md`) |

## A Setup Worth Having

The measure is: a new person clones the repo and has it running and tested in under 30 minutes, with one command per step.

- **One command to install**, one to run, one to test, one to reset. Written down and verified on a clean machine, not remembered.
- **Pin the runtime version in a file** the tooling reads (`.nvmrc`, `.python-version`, `go.mod`, the toolchain file). "Install Node 20" in a README is not a pin.
- **Dependencies come from the lockfile**, with the clean-install command (`npm ci` and equivalents), never a resolve-on-install.
- **Services in containers**, defined in the repo, so the database version matches production rather than whatever Homebrew installed in 2023 (`docker`).
- **Seed data is a command, idempotent, and realistic in shape.** Ten rows of nonsense hide the bugs that arrive at 100,000.
- **`.env.example` committed with every variable name and a safe placeholder**; the real `.env` gitignored, and never pasted anywhere (`security.md`).
- **A doctor/check command** that verifies versions, running services and required variables, and prints exactly what is missing. This is the highest-value 30 lines in most repos.

## Configuration

- Config comes from the environment; code reads it in one place and validates it at startup. Scattered `getenv` calls turn a missing variable into a mystery crash three layers deep, hours later.
- **Fail fast on missing or malformed config**, at boot, with a message naming the variable. Never a silent default for anything that differs between environments — that is how staging credentials reach production.
- Defaults are for the local case only. Anything whose wrong value is dangerous (a URL, a key, a mode) has no default.
- Keep the same variable *names* across environments; only values differ. Renaming per environment guarantees one of them is wrong.

## Parity, and Where to Stop Chasing It

Match production on: runtime major version, database engine and major version, and the way secrets and config are supplied. Do not try to match: scale, data volume, managed services, network topology, or hardware. The stated gaps get tested in staging or with production-shaped copies (`migrations.md`), and knowing which is which is the point — pretending local equals production is worse than a documented difference.

## Containers and Devcontainers

Containerizing the dev environment removes classes 1, 2, 5, 9 and 10 from the ladder above at the cost of file-sync performance, debugger attachment, and a layer between you and the process. Take that trade when onboarding is frequent or the stack is heavy; skip it for a single-language repo one developer works in (`docker`).

## CI-Only Failures

- Reproduce locally with CI's exact command, not your habitual one; CI often adds flags (coverage, parallelism, strict mode) that change behavior.
- Run the suite in the CI container image if there is one — that collapses most of the ladder in one step.
- Re-run with maximum verbosity, and keep the artifacts: logs, screenshots, core dumps. A CI failure you cannot inspect after the fact wastes the whole cycle.
- Passing on re-run means flaky, not fixed (`tests.md`).
- Timeouts in CI with none locally are usually resource limits or a missing warm cache, not slow code.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Manual setup steps in someone's head | Onboarding costs a day and the steps drift | One command per step, in the repo, verified clean |
| A README as the source of truth | Nothing enforces it, so it rots silently | The check command and CI enforce it |
| Installing dependencies without the lockfile | Your machine resolves different versions than CI | Clean-install from the lockfile |
| Different database version locally | SQL that works locally fails in production, and vice versa | Same major version, in a container |
| Real credentials in local config | They leak in a screenshot, a paste, or a commit | Local services and dummy credentials; pointers only (`security.md`) |
| Committing an editor-specific or machine-specific file | Breaks for everyone else | Gitignore it; share only what is portable |
| Debugging CI by pushing commits | 10-minute feedback loop, polluted history | Reproduce in the CI image locally; squash the attempts |
| Ignoring a slow local loop | The tax is paid every day by everyone | Measure it and fix the dominant step (`performance.md`) |

## Write Down What Made It Work

- **The exact commands that worked on this machine** — run, test, single test, lint, migrate, seed → `## Commands` in `~/Clawic/data/developer/repos/<repo>.md` (`memory-template.md`). This is the single most re-read section of the profile.
- **Every environment fact that cost more than five minutes** — a version incompatibility, a required variable, a port conflict, a container that must be up, a proxy or corporate CA → `## Gotchas` in the same profile.
- **A setup sequence that took real discovery to assemble** → `artifacts/setup-<repo>.md`, read whole when someone sets the project up again, with its `## Boxes` line in the same turn.
- **A CI-only failure and what the difference turned out to be** → `## Gotchas`, naming the rung of the ladder. Next time it is a lookup.
