# PROTOCOL — the reasoning behind backup-chain

This document argues the six invariants properly, records the incident classes
that produced each rule, and gives patterns this skill deliberately does not
implement in code. Read it once before trusting the tool with something you
cannot afford to lose.

## Threat model

The adversary is not a hacker; it is **infrastructure amnesia**. Observed
failure classes, all real, all in ordinary sandboxed agent environments:

- **Full workspace reset** — the project directory returns to an earlier state
  or to empty. Everything inside dies together: archives, configs, tools.
- **Partial rollback (the dangerous one)** — home dotdirs vanish while the
  project root survives, or vice versa; recent files roll back while older ones
  stay. Partial damage is worse than total loss because it *looks* fine: the
  workspace opens, the worklog is there, and only the credentials or the last
  three generations are gone.
- **The silent-extraction failure** — bulk extraction that exits 0 and writes
  nothing. Observed **twice** in production with GNU tar inside patched sandbox
  environments, on different days, against different archives. Both times the
  bulk restore "succeeded" and healed nothing. This is why invariant 5 exists
  and why the drill extracts and re-hashes rather than trusting `tar -x`.
- **The mtime trap** — after a rollback, timestamps lie. "Newest backup" by
  mtime or filename may be a stale handoff wearing fresh paint.
- **The helpful retry** — a recovery that restores an *older* generation
  cleanly and confidently, clobbering whatever newer state existed. A restore
  that completes but rolls you back is worse than a restore that fails loudly.
- **The smuggled path** — filesystem entries that look innocent by name but
  resolve somewhere else. Two directions, both closed by gates rather than
  trust: a nested symlink planted in a member directory that would pull
  *reads* (and archived bytes) from outside the project root at build time,
  and a symlinked directory left under a restore target that would push
  *writes* outside the target at restore time. Names are clean in both
  cases; only resolving the paths catches them. (Found by the ClawHub
  automated audit of 1.0.1; fixed in 1.0.2.)

Nothing here defends against an adversary who controls the machine *and* the
ledger. If the ledger channel can be rewritten, the protocol detects accidents,
not malice — say so in your own status docs.

## The six invariants

### 1. Ordering is asserted, never inferred

The generation counter is a fencing token: **one issuer, total order**. It
lives inside the archive, in the manifest, where a rollback cannot edit it
without breaking hashes; filenames carry it only as a human-readable label and
the tool never trusts them (a renamed archive, a colliding version number from
a destroyed predecessor session — both have happened; the manifest survived
both because it is the only authority).

`next-gen = max(local heads, ledger head) + 1` means a wipe that destroys the
local chain still cannot reissue an old number once the ledger remembers.

### 2. The chain is hash-linked

Each manifest records `parent_sha256`. The parent resolution order is:

1. **Ledger truth** — the sha256 registered for gen N-1. The ledger was written
   at registration time, outside the workspace; it cannot drift with the local
   filesystem.
2. **Local manifest truth** — the newest local archive whose *embedded
   manifest* says generation N-1. Its own sha256, computed now.
3. **Omit, loudly** — build proceeds with no parent and says the chain head is
   broken.

Filename-based guessing was removed after it produced a stale parent on a
production build (caught in review, overridden with manifest truth). The
sequence `parent → (gen, sha) → parent → …` turns N independent archives into
one falsifiable object: break any link and the break is provable.

### 3. The ledger lives outside the blast radius

The ledger answers three questions after a wipe:

- *What is the true head?* → `check` refuses anything older (stale handoff).
- *Which bytes were real?* → `verify` authenticates a pulled archive by hash.
- *What generation may the rebuilt workspace claim?* → `next-gen` stays
  monotonic even from an empty directory.

The skill ships three adapters and **no platform code**:

| adapter | wipe-safe? | use |
|---|---|---|
| `none` | — | testing, or when local-chain fencing is genuinely enough; every result is marked |
| `file` | only if the file lives outside the machine (`--ledger-file /mnt/persist/ledger.log`) | default; simplest real option |
| `command` | whatever your commands do | any append-only channel you already have: a gist, a paste, a forum post, a git branch, a database row |

For a shared or public channel, put identity filtering **inside the read
command** (`curl … | grep my-handle`), because the parser accepts any line
shaped like an entry. The one-issuer property of the fencing token depends on
it. Posting may be manual (some channels gate writes behind challenges or
moderation — solve them, then append); `build` prints the exact line either way.

### 4. A build is not done until a drill passed

The gates, in order — each exists because its absence was exploited by reality:

| gate | refuses |
|---|---|
| G1 member presence | building an archive that silently misses critical files |
| G2 generation fencing | reissuing a generation after a wipe |
| G3 parent resolution | a chain link nobody can vouch for (warns, does not guess) |
| G4 manifest inside | archives that order without describing themselves |
| G5 listing check | members that failed to make it into the tarball |
| G6 manifest roundtrip | a manifest that says something different from the archive built seconds ago |
| G7 sha256 receipt | later, undetectable bit rot; gives the off-site copy something to check against |
| G8 restore drill | everything above, if reading the archive back is broken (corrupt, truncated, incomplete) |

G8 re-reads **every** member from the finished archive — decoding the whole
gzip/tar stream — and hash-compares it against the manifest's member map.
Nothing is written to disk. It is the difference between "I created a file"
and "this file reads back intact." It is a read-back, not a restore
rehearsal: it cannot see a failure of the filesystem a real restore writes to
(disk full, path limits, permissions); `restore` verifies and reports those
per member (RESIDUAL_RISK item 15).

The manifest's **member map** (`path → sha256` for every file member) is what
makes restores verifiable without a surviving source: the archive carries its
own proof. Hashing every member at build time is cheap at workspace scale and
is the feature that turns a tarball into a chain node.

### 5. Restore is per-member, verified

The implementation streams each member out of the archive individually
(`tarfile.extractfile`), writes it under a temp name, fsyncs, hashes while
writing, compares against the member map, and only then renames into place.
There is no bulk extraction anywhere in the tool, and the drill would catch one
if someone added it.

Additional restore discipline:

- **Pre-gate** (`check`): refuse stale handoffs; mark skips loudly.
- **Authenticity**: if the ledger has an entry for this generation, the archive
  hash must match it before anything is written.
- **Overwrite separation**: existing differing files are counted and *refused*
  without `--overwrite`. A heal and a clobber must be two different decisions.
- **Post-receipt** (`recheck`): `ok` closes the incident; `stale` means bytes
  landed but the precondition did not — the ledger remembers more than the
  workspace now holds. Treat a stale like an incident, not a success.
- **Traversal defence**: member names are validated on read (absolute paths,
  `..`, NUL) and every write is resolved inside `--target`.

### 6. Fencing failures are loud or refused, never silent

The decision table:

| archive manifest | ledger reachable? | vs head | decision |
|---|---|---|---|
| absent | yes | — | **refuse** (provenance unknown while a sequencer exists) |
| absent | no | — | restore, *marked* (legacy heuristic) |
| gen N | yes | N < head | **refuse** (stale handoff) |
| gen N | yes | N < local head | **refuse** (stale vs local chain — assertable even when the ledger is silent; found by test, not by theory) |
| gen N | yes | N ≥ head, ≥ local head | restore (N > head is annotated: unregistered build) |
| gen N | no/error | N < local head | **refuse** (assertable locally even without the ledger) |
| gen N | no/error | N ≥ local head | **skip, marked** (unverified precondition) |

"A clearly marked untested solution is more useful than a falsely verified
one." The corollary: a refusal is the protocol working, not malfunctioning.
Investigate before `--force`. A deliberate rollback to an older generation is a
legitimate operation — but it must be a *decision*: with `--force` it proceeds
under an explicit OVERRIDE banner, without it the refusal stands.

## The witness layer (v1.1)

The six invariants are guards: they run at invocation, and **the adversary
attends the invocation** — vina's critique of invocation-time consent checks,
which the audit rounds 3–5 took seriously on the execution side. The witness
layer is the other half of that lesson: evidence written at rest, next to the
artifact, that no later reader has to take on faith from the moment of
invocation. Witnesses gate nothing. A refusal is a gate; a witness
disagreement is an alarm; confusing the two teaches users to fix the alarm.

Three witnesses, each with a named reason to exist:

**Decision traces (`cot`).** Custody and validity are different receipts
(§ Custody vs validity below): a sha256 proves a sentence survived a restore,
not that it was ever right. The route-file pattern answers validity with
documents; the decision trace answers it with a bounded, chain-native record
of *why the generation was decided*: trigger, belief, consciously-accepted
risk, falsifier. Two constraints carry the whole design:

1. **Decision time or nothing.** A trace written after the outcome is
   observable is a narrative with better formatting. The manifest copy is
   written at build time, inside the archive, where a rollback cannot edit it
   without breaking hashes; the ledger carries a space-free prefix digest, so
   the why survives even when the archives do not.
2. **Refusal, never truncation.** A cap that silently edits reasoning is a
   smaller version of the failure this skill exists to refuse. Overflow
   refuses the build and says so.

The falsifier field is what keeps a trace from being a diary entry: it must
name one checkable claim that, if false, indicts the reasoning that produced
the generation. A trace that cannot falsify itself is a narrative with better
formatting — the cap alone does not save it.

**Operator acks (`op=ack`).** The ledger is an automatic witness; the ack is a
human one. Their failure modes are different (bit rot, rewrite, silencing vs
coercion, fatigue, session hijack), which is exactly what makes two of them
worth more than one: silent forgery of history now requires subverting both
*in coordination*. That is a probability shift, not an elimination — nothing
in this protocol eliminates anything, and v1.1's docs are forbidden from
claiming otherwise (see RESIDUAL_RISK.md for the language discipline and the
full residual list). The ack attests the *looking*, not the believing; it is
written when the operator actually reads a drill receipt, never on a
schedule, and nothing anywhere requires one. A trail of honest gaps is more
informative than a wall of rubber stamps.

**Ack policy (`ack-policy off|on`, v1.2).** Acks are witnesses, not gates, so
a deployment whose human cannot ack (chat-only operators; unattended
automation) can disable them — and the disable act is itself witnessed,
because a chain with no acks on record must say WHY in the same ledger an
ack would live in. "Disabled by decision" and "nobody watching" must never
be indistinguishable to a later reader: the first is a policy, the second is
the exact failure the witness layer exists to make visible. Both directions
append their line (`event=ack-off` / `event=ack-on`) through the same
adapter path and consent boundaries as acks, and both refuse when the ledger
is unreachable or absent — an un-witnessable policy change is refused, not
made. While the policy is off, `ack` refuses (naming the recorded decision
and the re-enable path), and the empty-witness note in `verify`/`status`
attributes the absence to the policy, not to neglect. The policy lines are
authored text, forgeable like any ledger line (RESIDUAL_RISK item 11): they
raise the cost of passing neglect off as policy; they do not make it
impossible.

**Event lines (`event=restore|drill`).** The restore act is the most
consequential thing that ever happens to a chain, and before v1.1 it was the
one thing the chain never remembered: the ledger witnessed builds only.
Restores and standalone drills now append event lines — through the same
adapter path and consent boundaries as registrations. Verifies are
deliberately excluded: a verify is a read, repeatable at zero cost, and reads
do not belong in an append-only witness.

**Compatibility.** All witness entries are additive. `op=ack` and `event=`
lines are invisible to the build-entry parser by construction (the `gen=`
anchor is line-start), so pre-v1.1 tooling reads a v1.1 ledger unchanged, and
`next-gen` is untouched by witness traffic. Pre-v1.1 manifests read as "no
trace recorded" — an honest gap, not an error.

## Curation and custody hand-off (v1.2)

Two operator decisions shaped this layer, and both restate the founding
constraint: an agent using this skill may have **no storage beyond its own**,
and **no two workspaces look alike**. Everything here is therefore an option;
with no flags passed, every command behaves exactly as v1.1.1.

**Exclusions are an option, never a default.** The only built-in patterns
remain the self-exclusion class (`*.tar.gz`, receipts, `*.part`) — the chain
must not swallow its own archives. What is new: `member add PATH --exclude
PATTERN` (repeatable) curates a single member, alongside the pre-existing
config-global `exclude` list. One semantic tightened: an excluded **directory
now prunes the walk**, so a single pattern (`node_modules`) excludes the whole
subtree. Before, the descent continued and only the directory *entry* was
dropped — the reason the old docs demanded both `dir` and `dir/*` forms.
Configs that already listed both behave identically (strictly less work).

**Eviction with custody.** The incident class behind `evict`: dead weight was
removed from a production chain as a silent config edit — the "why" and the
"where did it go" existed only in the conversation that ordered the removal,
which is exactly the kind of record a later session with no memory cannot
find. `evict PATH --stow-to DIR|--stow-cmd CMD` makes removal a *recorded act
with custody*: the member's current content is packaged with a per-member
hash map and an `evict-manifest.json`, the package is handed to the chosen
destination, and only then is the member untracked and an
`event=evict` witness line appended. Without a stow destination the eviction
is **refused** — silent custody loss is what the command exists to prevent,
and `member remove` remains the deliberate silent drop. Two properties worth
restating: a failed hand-off keeps the member (custody is established before
tracking stops, never after), and the files on disk are never touched —
eviction stops *tracking* content; deleting it remains yours.

**Stow is the roundtrip pattern, automated for one destination.**
`build --stow-to DIR` copies the finished archive + receipt into `DIR` and
re-hashes the copy — steps 2–4 of the roundtrip pattern below, for the
directory case. `--stow-cmd CMD` feeds the bytes to **your** upload command
on stdin; its exit code is its claim of success, and the skill says
"claimed, not verified" wherever it reports that path, because it cannot
check what a foreign command did with the bytes. Both record `event=stow`
witness lines. Stow failures warn and never gate: the archive already exists
and passed its gates — a lost side-bucket copy is a custody gap to fix, not
a reason the backup does not exist.

**Detections are advisory failsafes.** A production chain was found quietly
creeping toward its size ceiling: the weight was visible in principle and
invisible in practice, because nothing failed at 20 MB, or 25, or 29. The
v1.2 detectors make weight visible instead of making it fatal: build-time
`DETECT` warnings for archive growth vs the parent generation, duplicate
content across members, and the largest members entering the chain; `status`
shows raw member/archive totals. They read only what was collected, they
size off raw bytes, and they never gate — a detector that blocks builds
teaches its users to disable detectors. The blind spot is stated in
RESIDUAL_RISK.md: a detector cannot see what an exclude already removed,
which is precisely where the other half of the risk lives.

## Off-site distribution (the part that is deliberately yours)

The tool has no upload code, so it cannot ship bad upload code. What it gives
you is everything distribution needs to be checkable:

**The roundtrip pattern** (the only proof that matters):

1. `build` → archive + `.sha256` receipt, drill PASS.
2. Upload archive + receipt (and the ledger line, if your ledger is manual).
3. **Fetch the uploaded copy back down** (signed URL, raw endpoint, whatever).
4. `sha256sum -c` the fetched copy against the receipt. Only a fetched-back
   hash-equal copy is a MATCH. Upload APIs report what you asked them to do;
   the roundtrip reports what actually landed.

**Rules of thumb learned from incidents:**

- Keep the newest archive + receipt + ledger line in at least two failure
  domains (e.g. local + one off-site). More is fine; one is zero.
- The ledger is small — replicate it more aggressively than the archives.
- Archives that contain credentials must go only to **private** storage. The
  tool prints `SECRET-WARN` for credential-looking member names; treat the
  warning as a prompt to check where the archive will be sent.
- After any heal, build a new generation whose `--carries` note records the
  incident and the cure. The chain then documents its own history, and the
  next session inherits the lesson without needing this conversation.

## Custody vs validity

sha256 proves a sentence **survived** a restore. It does not prove the sentence
was ever **right**. These are separate receipts, and this tool only issues the
first. The pattern that covers the second: alongside each consequential
conclusion, keep a small route file (premises with receipts, rejected
alternatives, priced uncertainty, a falsifier, a recheck date) and put the
route files **in the member list**. Routes then hash into the same chain as the
artifacts they audit: after a restore, an artifact whose route survived is
content-with-route; an artifact whose route is gone is content-without-route —
refuse to narrate its why, flag it for re-derivation. The tool stays
content-blind; the member list is where you teach it your epistemology.

## What a chain buys over "just copy files"

1. Ordering you can prove, even to a session with no memory and a lying clock.
2. Authenticity you can prove from outside the failure domain.
3. Completeness you can prove per restore, per file.
4. History: each manifest's `carries` note is the incident log of the workspace
   itself.
5. A short, honest failure vocabulary: refuse / skip (marked) / stale / ok —
   instead of "it seemed to work."
