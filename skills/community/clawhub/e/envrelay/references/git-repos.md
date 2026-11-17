# Git repositories

A repository whose work is all on a remote does not need to be in the backup —
it needs one line of metadata. A repository with uncommitted work in it is
irreplaceable and must be carried whole. Deciding which is which is the whole
of this file.

## Finding and classifying them

Use the classifier script — it finds, classifies and extracts the metadata in
one pass, instead of you improvising `find` and five `git` commands per repo:

```sh
python3 scripts/git_classify.py --scan ~ --max-depth 6
```

or for known paths:

```sh
python3 scripts/git_classify.py ~/dev/api ~/dev/site
```

It prints one JSON object with a `repos` array. The script only reports facts;
choosing a strategy from those facts is yours and the user's.

Nobody has vetted a repository the scan finds, and its `.git/config` can name
programs for git to start — an fsmonitor, a filter driver, a signature
checker. The script switches those off for its own git commands, which is one
more reason to run it rather than `git status` by hand. A filter driver only
the repository defines is switched off too (one the user installed, like git
lfs, keeps working), so files it would have cleaned can count as uncommitted —
which errs towards carrying the repository. This needs git 2.31 or newer; with
an older git every repository comes back `unknown`.

The scan prunes inside every repository it finds, so nested repositories
(submodules, vendored checkouts) do not show up separately — the outer one
carries the inner ones as files. It also prunes the standard cache directories
(`node_modules`, `.venv`, …) and caps the depth, because an unbounded walk of a
home directory descends into caches and snapshots and takes minutes.

## The five states

Not everything with a `.git` in it is a working repository. The `state` field
classifies what the directory actually is, and the strategy question only
arises for the first two:

| `state` | What it means | What to do |
|---|---|---|
| `complete-repository` | HEAD resolves, `git status` works | Choose a strategy below |
| `partial-repository` | git recognises it, but HEAD has no commit — a fresh `git init`, or a checkout that never finished | If the working tree has content, carry it with `"strategy": "files"`; an empty one is not worth carrying, but say so |
| `invalid-head` | `.git` exists but git errors on it — corrupt or interrupted | Never `clone`-strategise it: the metadata cannot be trusted. Carry it whole with `files` and tell the user it needs `git fsck` on arrival, or let them repair it first. Prefer repair over delete-and-reclone when the repo is large |
| `ordinary-directory` | No `.git` at all | Not a repo. It belongs in `files`, not `git_repos` |
| `unknown` | git missing or older than 2.31, or a command timed out | Report it; do not guess |

The script's per-repo output for functional repos includes `remotes`, `branch`,
`head`, and the three counts that decide everything: `uncommitted`, `unpushed`,
`stashes`. `unpushed` is the question people forget — a repo can be
`status --porcelain`-clean and still hold a week of commits that exist nowhere
else. Stashes live in `.git/` and do not travel with a clone.

## Choosing a strategy

**`"strategy": "clone"`** — all four must hold: has at least one remote,
`uncommitted` is 0, `unpushed` is 0, `stashes` is 0. Record the metadata in the
manifest and copy nothing.

**`"strategy": "files"`** — anything else, by default. Copy the whole
directory, `.git/` included, into `repos/<name>/`. Apply the exclude list
inside the copy (`node_modules/`, `target/`, `.venv/`) — but never to `.git/`,
which is the history and is the reason the repo is being carried at all.

**`"strategy": "metadata"`** — the escape hatch when a repo has local-only
state but the user, told the size and the counts, decides not to carry it.
Record everything `clone` records *plus* the non-zero counts and a `reason`
that says in words: **the uncommitted work, unpushed commits and stashes are
not in this backup.** This strategy is always the user's explicit choice, never
your default — it is the only one that knowingly leaves data behind.

Manifest shapes for all three are in `references/manifest.md`.

## Tell the user, per repo

This is the part that matters more than the mechanics. When a repository has to
be carried whole, say why in one line before you copy it:

> `~/dev/api` has 12 uncommitted files and 2 unpushed commits on
> `feat/parser`, so I am carrying the whole directory (340 MB). If you push
> first, it becomes a one-line clone entry instead.

The user often *wants* to push, and would rather know now than discover a
340 MB directory in the backup later. Give them the chance; do not push on
their behalf.

Repositories with **no remote at all** deserve a louder mention — that
repository exists nowhere else in the world, and this backup is about to become
its only other copy.

## Agent files inside a repository

Repositories now carry agent state of their own: `CLAUDE.md`, `AGENTS.md`,
`.claude/` (settings, hooks, skills, subagents), `.cursor/rules/`,
`.github/copilot-instructions.md`, `.mcp.json`, `.aider.conf.yml`. Two
consequences.

Tracked ones travel with the repository however it is carried, and need no
special handling — but a `"strategy": "clone"` entry brings back only what the
remote has, and the local-only ones (`.claude/settings.local.json` is the
usual case, `.gitignore`d by design) are exactly the state that strategy drops.
`git_classify.py`'s untracked count is the signal to look before choosing
`clone`.

And a restored repository's `.mcp.json` and `.claude/hooks/` are code that
runs the first time an agent opens that directory. Rule 4 applies to
repositories, not only to the home directory — see `ai-agents.md`.

## Restoring

Restore credentials **first**. Every SSH clone below depends on `~/.ssh` being
in place with the right modes.

For each `"strategy": "clone"` or `"strategy": "metadata"` entry:

```sh
git clone <origin-url> <expanded-original-path>
git -C <path> checkout <branch>
```

For a `metadata` entry, **before** cloning, show the user the recorded counts
and the `reason`: this repo had uncommitted work that the backup deliberately
does not contain, and the clone will not bring it back. They knew at backup
time; they deserve the reminder now, while the old machine might still exist.

Then add any non-`origin` remotes from the manifest.

Check the recorded `head` afterwards:

```sh
git -C <path> cat-file -e <head>^{commit}
```

If it is not reachable, the remote moved on since the backup — normal, and
worth one line in the report (ledger status `head-unreachable`) rather than an
error. If the *branch* no longer exists on the remote, say so and check out the
default branch instead.

Failures to expect and how to report them:

| Failure | What it means | Say |
|---|---|---|
| `Permission denied (publickey)` | Credentials not restored, or the key is not in the agent | Fix the credential step, then retry |
| `Repository not found` | Renamed, deleted, or access revoked | Report it; do not guess a new URL |
| Path already exists | The new machine already has this repo | Skip, report (`path-exists`), let the user reconcile |

For each `"strategy": "files"` entry, restore it like an ordinary directory,
then run `git_classify.py` on the restored path: it should come back
`complete-repository` (or `partial-repository` if that is what was carried)
with the same counts that went in. Show the user the state it came back in —
uncommitted work is what it was carried for, and they should see it land.

Record every repo in the restore ledger as you go: `cloned`,
`restored-files`, `head-unreachable`, `path-exists`, `clone-failed`.

Finally, remind the user that any directory the exclude list emptied out needs
its build step (`npm install`, `cargo build`, `./gradlew build`) before the
project will run.
