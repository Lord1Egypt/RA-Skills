# Landing in an Unfamiliar Codebase

The goal of orientation is not understanding the system. It is finding the one place your change goes, and knowing what will break. Budget ~20-30% of the estimate, capped near two hours, and end it by shipping something trivial (SKILL.md Rule 3).

**Before the first command**, open `~/Clawic/data/developer/repos/<repo>.md` if `## Repos` in `memory.md` has a row for it. Someone already paid for the run command, the seed step and the three gotchas below; re-deriving them is the most repeated waste in this domain.

## The First Two Hours, In Order

1. **Run it.** Not read it. A repo you cannot start is a repo you cannot verify a change in, and the setup failures happen now rather than at 6pm (`environments.md`).
2. **Run the tests.** Note the wall time and how many fail on a clean checkout. A suite that is already red is the single most important fact about this codebase — it means CI is not a signal and your change has no safety net.
3. **Trace one real request end to end.** Pick the most common operation and follow it: entry point → router → the function that does the work → the write. Set a breakpoint or add one log line at each hop. The call stack you get is the map; folder names are marketing.
4. **Read the data model.** Table or schema definitions, in one sitting. Names of entities and their relationships explain more of the code's shape than any architecture document, and they are the thing that is expensive to change (SKILL.md Reversibility).
5. **Read the tests around the area you will change.** They are the specification that is actually enforced. What is untested is what you can break silently.
6. **Ship something trivial.** A typo fix, a log line, a test. Prove build → test → review → deploy works for you before the real change is in flight.

## Finding Where a Change Goes

| You know | Search this way |
|---|---|
| A string the user sees | Grep the literal, then grep the key if it resolves to a translation file |
| An endpoint or URL | Grep the path fragment, not the full URL — prefixes are assembled at runtime |
| A field in a payload or DB row | Grep the field name; serializers and validators cluster around the truth |
| Only a symptom | Reproduce, then stack-trace or log-bisect it (`bugs.md`) |
| Only a feature name | Look for the flag key, the migration that added the table, or the test file |
| Nothing at all | `git log --diff-filter=A` on the area to find the commit that introduced it, then read that PR |

Grep beats reading directory trees. A codebase's structure lies about where behavior lives; string literals do not.

## Git as an Archaeology Tool

| Question | Command |
|---|---|
| Who last touched this and why | `git log -p -- <path>` — the message plus the diff, not just `blame` |
| Why is this weird line here | `git log -S '<exact string>' --oneline` — finds the commit that introduced or removed it |
| Was this line moved or written | `git blame -w -C -C <file>` — ignores whitespace and follows code moved between files |
| What usually changes together with this file | `git log --format=%H --name-only -- <path>` and count co-occurring paths — coupling the imports do not show |
| Is this code alive | Last commit date plus whether its tests exist; a file untouched for years with no tests is either perfect or dead |

A line that looks wrong and has survived three years usually encodes a requirement nobody wrote down. Find the commit and the ticket before "fixing" it.

## Reading Order for a Big System

- **Config and environment first**: what it needs to boot names its dependencies more honestly than any diagram.
- **The entry points**: `main`, the server bootstrap, the CLI definition, the job registry. Everything else is reachable from there.
- **The seams, not the layers**: where the system talks to something it does not control — HTTP boundaries, queues, the database, the filesystem, the clock. Those are where behavior is observable and where tests can grab it (`tests.md`, `legacy-code`).
- **Skip**: utility folders, generated code, vendored dependencies, and anything named `common` — they are consequences, not causes.

## Signals to Read Off a Repo in Ten Minutes

| Signal | What it tells you |
|---|---|
| CI config | The real definition of done: what must pass before a merge is possible |
| Lockfile present and committed | Whether builds are reproducible at all (`dependencies.md`) |
| Test count vs source size, and the newest test date | Whether tests are maintained or ceremonial |
| Number of contributors in the last 90 days | One means tribal knowledge and no review culture; many means conventions are enforced |
| Open PRs older than a month | Review is a bottleneck here; size your PRs down accordingly (`reviews.md`) |
| A `docs/adr/` or similar | Decisions are recorded — read them before proposing an alternative that was already rejected |
| TODO/FIXME density near your area | Known debt; check whether a ticket exists before adding a fourteenth |

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Reading the whole codebase before starting | Comprehension decays faster than you accumulate it; you will re-read it anyway | Trace one path, change one thing |
| Trusting the README | READMEs describe the setup of the day they were written | Trust the CI config; it must be true or the build fails |
| Assuming folder names mean what they say | `utils/` holds business logic in most repos over two years old | Follow the call stack |
| Refactoring on day one | You cannot yet tell an accident from a constraint | Note it in `## Gotchas`, revisit after the first shipped change |
| Asking a question the repo answers | Burns the one thing you have limited credit for | Ask only what is not in the code, the tests, or the log (`collaboration.md`) |

## Write Down What You Learned

Orientation is the most reusable work in this skill and the most commonly lost. Before the session ends, write `~/Clawic/data/developer/repos/<repo>.md` (`memory-template.md`) with: the map (entry point → the file where the real work happens), the exact run/test/lint/migrate commands as they worked on this machine, the conventions you inferred, and every gotcha that cost you more than five minutes. Add its row to `## Repos` in `memory.md` in the same turn. Reviewers and code owners you identified go to `~/Clawic/data/contacts/contacts.md`, not into the repo profile.
