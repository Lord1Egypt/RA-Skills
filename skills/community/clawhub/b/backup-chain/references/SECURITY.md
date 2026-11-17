# SECURITY — backup-chain

## Witness layer (v1.1)

- **Decision traces are authored text.** Keep secrets out of them the same
  way you keep them out of `carries` notes — the trace is hashed into the
  manifest and prefix-digested into every copy of the ledger, so a credential
  pasted into `--cot-belief` lands in every witness copy you have. The build
  runs the same SECRET-WARN heuristic over trace fields as over member paths;
  absence of a warning is still not an audit.
- **Acks are witnesses, not authentication.** `op=ack` attests that someone
  (or something holding the operator's session) appended a line. It raises
  the cost of silent forgery — the chain and the human must now be subverted
  in coordination — and nothing more. Any document or claim that promotes the
  ack to a guarantee is wrong; see `references/RESIDUAL_RISK.md`. The v1.2
  ack policy inherits all of this: `event=ack-off` records that a policy was
  *declared*, not that the declaration was honest, and a forged policy line
  is forgeable exactly like a forged ack — same channel, same trust class.
  Disabling acks changes no gate (there is no gate to change); it only moves
  the deployment onto the record.
- **Trace-digest disagreement is an alarm, not a gate.** `verify` reports
  `MISMATCH` between the manifest trace and the ledger digest without
  refusing. The refusal would be the dangerous choice: it converts a
  forensic signal into a configuration problem, and users solve configuration
  problems by re-running with flags.
- **Events inherit the consent boundaries.** `event=` lines go through the
  same adapter path as registrations: a command adapter still needs
  `--allow-cmd-ledger`, an external file ledger still needs
  `--allow-external-ledger`, and an event that cannot be recorded prints a
  stderr WARN while the custody operation itself keeps its result.

## Secrets in archives

The tool hashes and archives member files verbatim. If your member list
includes credentials, tokens, or keys, **every copy of every archive contains
them**, and so does every place you distribute archives to.

- `build`, `status`, and `verify` print a `SECRET-WARN` line for members whose
  basename looks credential-like (`credential*`, `*token*`, `*.pem`, `id_rsa`,
  `api_key`, …). The heuristic is a courtesy, not a guarantee — absence of a
  warning is not an audit.
- If you back up secrets: keep distribution targets **private**, prefer
  excluding secrets from members entirely (rotate what you cannot afford to
  lose), and consider a separate secret store with its own chain.
- Worklogs and notes are secrets too, more often than people expect — they
  quote endpoints, handles, and half a credential before anyone thought to
  redact. Review the member list (`status`) with that in mind.
- Since v1.3.0, archives and receipts land **owner-only (0600) by default** —
  see Archive file modes below. That protects the file on this machine; it
  says nothing about the places you distribute it to.

## Archive file modes (v1.3.0)

Archives, their `.sha256` receipts, and any `--stow-to` copies are created
**owner-only (0600) by default**, applied **verbatim**: umask does not widen
or narrow an explicit choice, so `--archive-mode 0644` means 0644 whatever
the ambient umask is, and the default means owner-only whatever the umask is.
What landed is printed on the G7 receipt line — the build output carries the
fact, not a stat you forgot to run.

- Widen deliberately when the deployment needs it: `build --archive-mode
  0640` (group-readable) per invocation. Since v1.3.1 (audit T09, round 7)
  widening is CLI-only: the persistent `archive_mode` config key may narrow
  the artifacts (any mode with no group/other bits — 0000/0200/0400/0600)
  but a value carrying group/other access is refused outright (rc 2, before
  anything is written). The reason is the skill's own config doctrine:
  `.vault/config.json` is workspace-contributed adversarial input, and a
  planted value must not be able to make your backups group- or
  world-readable — no matter how visible the mode is on the G7 line
  (visibility is not consent; the same argument that closed 1.0.4's T09 on
  command execution). Modes with exec/setuid/setgid/sticky bits, or
  anything above 0666, are refused for both origins (rc 2, naming where the
  value came from).
- Why the default changed: through 1.2.2 an archive landed `0666 & ~umask` —
  usually world-readable — while this file warned that archives can hold
  secrets, and the members a restore produces already landed owner-only
  through the staging discipline (see below). The docs and the default
  disagreed; the default moved to the safer, previously-documented side.
- This is not encryption and not a gate: a mode decides who can read a file
  on one machine. Off-site distribution is still the user's job, and an
  archive is only as private as every location it is copied to. The
  `archive_mode` config key is workspace-contributed state like the rest of
  config.json: a planted value can widen artifact readability to 0666 at
  most (visible on the G7 line) — it cannot redirect paths, disable gates,
  or run commands (RESIDUAL_RISK item 16).
- Restored members always land owner-only (0600), whatever the archived
  files' original modes were: restore writes through the same staged-fd
  discipline, which creates owner-only and never reopens a pathname. This
  behavior predates v1.3.0; it was never stated before, which is its own
  defect. A shared machine that needs other readers must chmod after
  restore.

## Ledger command adapter

`--ledger command` executes **your** commands — read via stdout, append
with the entry piped to stdin. This is the git-hook trust class:

- Commands run from the user's own config file, as argv vectors (`shlex`-split,
  `shell=False`) — never through a shell. Pipes, redirects and globs are inert
  unless the config names a shell itself (`sh -c '…'`), in plain sight in the
  WARN preview. Anyone who can write that config can run the program it names.
  Treat `.vault/config.json` as code.
- **Refuse-by-default (since 1.0.4, audit T09 round 3):** a warning is not
  consent. Every invocation that would execute a configured command must pass
  `--allow-cmd-ledger`. Without it, the read path is reported unreachable with
  guidance (status/check degrade to the marked-skip fencing semantics) and
  `build --register` fails loudly — a workspace-contributed config can no
  longer fire on a routine subcommand. The flag is per-invocation by design:
  automation passes it only inside scripts the operator has reviewed.
- **Runtime visibility (since 1.0.3):** every adapter execution prints a `WARN`
  line to stderr naming the executed command (`read_cmd` / `append_cmd`) and a
  truncated preview, once per command per process (since 1.0.4 it fires only
  after the opt-in). Warnings go to stderr only — stdout (JSON checks, ledger
  parsing) stays clean. If you see this warning in a workspace whose
  `.vault/config.json` you did not review, treat the workspace as hostile and
  stop.
- The tool adds no environment, no secrets, no network. Whatever your commands
  can reach, the adapter can touch; nothing more, nothing less.
- Review commands at `init` and after any config edit. On shared channels,
  filter for your identity inside the read command — the ledger parser trusts
  any line shaped like an entry, so one-issuer depends on your filter.

## Config path boundary

**Since 1.0.5 (audit T09 round 4),** the same "config is code" rule that gates
execution also gates *where the tool reads and writes*. Left unchecked, a
workspace-contributed config could redefine the backup root and collect files
far outside the project you selected — with `output_dir` and `chain_name`
steering where the archive lands. That was the reading-side twin of the
command-adapter issue, and it is closed the same way: the config proposes,
the invocation root and the operator dispose.

- **Root pin.** The stored `root` must resolve (`realpath`) to the invocation
  root. A config claiming another directory is refused with recovery guidance
  (fix `root` in the config, or `init --force`) — a moved workspace must say
  so explicitly, never silently re-target. Symlinked paths to the *same*
  workspace still pass.
- **Member re-validation.** Every configured member path is re-checked at
  load with the same `normalize_member` rules `member add` enforces — a
  hand-edited or planted config cannot smuggle `..`, `~`, or absolute paths
  past the CLI.
- **`chain_name` is a filename component.** Refused if empty, oversized, or
  containing path separators / `..` — it lands in `<name>-g<N>.tar.gz`, so it
  must not be able to traverse. Spaces and unicode stay legal (init derives
  the default from the workspace basename).
- **`output_dir` stays inside the workspace.** Absolute, home-relative, and
  traversing values are refused in the config; a symlinked output directory
  that resolves outside is refused before any bytes or directories are
  written — by ONE shared `realpath` + `commonpath` containment (the member
  reader's pattern) guarding build AND evict since 1.3.2. The round-4 gate
  had covered only build; evict (added 1.2.0) still carried the
  pre-round-4 pattern, and audit T09 round 8 caught it writing the
  credential-bearing eviction package and its receipt through a planted
  symlinked component (reproduced against shipped 1.3.1 before the fix).
  External destinations remain a per-invocation operator choice:
  `build --output <path>`, `evict --stow-to/--stow-cmd`.
- **File ledger destination (1.0.6).** The last config-controlled sink,
  closed one round after the rest: an append-only ledger is still a write
  primitive when its destination is attacker-chosen, so a file-ledger path
  that *resolves* outside the workspace — absolute, traversing relative, or
  through a planted symlink — refuses to append unless the invocation
  carries `--allow-external-ledger` (the read path reports
  unreachable-with-guidance, registration fails loudly naming the flag).
  Containment is `realpath`-checked at every use, so a symlink planted or
  swapped after approval still fails closed. In-root ledgers — including
  symlinked in-root targets — never consult the flag, and the documented
  wipe-safety setup survives with the destination chosen in the operator's
  own voice (`init --ledger-file /external/path`) plus the flag at runtime.
  The two consent flags are independent on purpose: `--allow-external-ledger`
  never enables the command adapter and `--allow-cmd-ledger` never unlocks
  external ledger paths.

## Custody hand-off and eviction (v1.2)

- **The stow command adapter is operator-voice, not config.**
  `--stow-cmd CMD` exists only as a per-invocation CLI argument — it is never
  read from `.vault/config.json` and never persisted — so the planted-config
  attack class the ledger adapter guards against (a workspace-contributed
  config firing on a routine subcommand) has no surface here. The command
  still runs in the same execution discipline: `shlex`-split argv vector,
  `shell=False`, with the archive bytes on stdin, and a stderr `WARN` line
  naming it the first time each process runs it. The bytes you pipe are
  archive contents: only hand them to commands and destinations that may
  hold those bytes.
- **Stow-cmd custody is claimed, not verified.** The skill cannot hash-check
  what a foreign command did with the bytes; it reports exactly that. Only
  `--stow-to` performs the roundtrip hash comparison: the copy is staged
  beside its destination, re-hashed there, and only then given its final name
  (v1.2.2), so a mismatched or partial copy never exists under the archive's
  name to impersonate custody. An `event=stow` witness
  line with `dest=cmd` means "the command exited 0", nothing more.
- **Eviction is refusal-safe by construction.** `evict` refuses to run
  without a stow destination, refuses non-members, and — the load-bearing
  one — refuses to untrack the member when the hand-off fails. A failed
  eviction leaves the package in the output dir with its receipt; the member
  stays tracked; nothing is lost by retrying. The witness line is
  best-effort like every event line: if the ledger cannot record it, the
  package's `evict-manifest.json` is the durable record.
- **Eviction packages are archives.** They carry member bytes, inherit the
  SECRET-WARN heuristic over evicted names, and deserve the same
  distribution discipline as any archive: private destinations for
  credential-looking content.
- **An exclude is a silent hole.** Unlike every other risk in this file,
  curation failures produce no warning at build time: a mistyped pattern
  simply removes paths from every future archive, invisibly, forever. The
  compensating controls are human ones — `member list` displays each
  member's patterns, `status` prints raw member sizes so an over-broad
  exclude shows up as missing weight, and a hand-edited pattern of the wrong
  shape is refused at load. The discipline: review excludes when you review
  the member list, and after any curation change, build once and read the
  DETECT largest-members line against what you expect.

## Restore discipline

- Restore **refuses** to overwrite differing files without `--overwrite`, and
  refuses fencing-refused archives without `--force`. Both refusals print why;
  both are the tool working.
- Restore targets are validated: `/` and the home directory are refused outright.
- Every extracted file is verified against the manifest's member map before it
  is renamed into place; a failed member leaves the workspace **not** healed
  and exits non-zero. Do not build on a partial heal.

## Staging discipline (v1.2.1)

- Every temporary file the tool writes — config/marker/receipt/state writes,
  build and eviction `.part` archives, restore `.restore-part` members — is
  created by `tempfile.mkstemp` **in the destination directory**: a random,
  `O_CREAT|O_EXCL` name that cannot be pre-planted, written through its file
  descriptor (never by reopening the pathname), fsynced, then moved into
  place with `os.replace`.
- Why: until v1.2.0 the staging names were predictable (`.<name>.tmp`,
  `<archive>.part`, `<member>.restore-part`) and the writes reopened the
  pathname, following symlinks. Anyone who could write to a destination
  directory (an operator-set `--output`, an external ledger path, a restore
  `--target`) could pre-create the staging path as a symlink and have the
  bytes land outside the boundary the operator chose — ClawHub audit T09,
  round 6 (v1.2.0 re-scan), "Predictable Temporary Files Permit Symlink-Based
  Writes Outside Authorized Boundaries". The consent-gate fixes of rounds
  3–5 are unaffected and remain the design.
- Crash leftovers keep the `*.part` suffix family, so the self-exclusion
  default excludes still shields them from re-collection by the next build.
- **Stow copies are staged too (v1.2.2).** 1.2.1's staging covered every
  temporary file but not `--stow-to`'s copy, which is a write to a
  *predictable final name* (`<chain>-g<N>.tar.gz`) in an operator-chosen
  directory. `shutil.copy2` reopened that pathname and followed a planted
  symlink to wherever it pointed — and the roundtrip hash, read back through
  the same link, still reported MATCH. The copy now goes through the same
  `mkstemp` staging, is verified *before* it takes the final name, and lands
  with `os.replace`, which swaps the directory entry itself (a planted link
  is replaced, never followed). A failed or partial copy is removed rather
  than left under the archive's name.
- Stated residual: an attacker who controls a destination directory still
  controls the files in it. Staging hardening removes the out-of-boundary
  write primitive, not the trustworthiness of a hostile directory — treat
  shared, attacker-writable directories as hostile inputs, as before.

## Ledger line discipline (v1.2.2)

The ledger is line-oriented, so *what counts as a line break* is a security
property, and it has to be the same for every writer and every reader.

- **The gap that existed.** Through 1.2.1, the single-line validators (`cot`
  fields, `ack`/`ack-policy`/`evict` notes) rejected `\n`, `\r` and NUL —
  but the readers split with `str.splitlines()`, which also breaks on VT, FF,
  FS/GS/RS, NEL (U+0085), U+2028 and U+2029. A note such as
  `x<U+2028>gen=1 sha256=<64 hex>` fits the length cap, was written as *one*
  physical line, and was read back as *two* — the second a forged build
  entry (`next-gen` jumped to 1000; a forged hash for a real generation
  could be planted). `evict` additionally wrote the member's *path* and the
  package filename into the ledger unvalidated, so a member whose name held a
  newline did the same thing without any separator trick.
- **Three layers, each sufficient for the case it covers.** Writers refuse
  the whole class (`has_line_break`, compared exhaustively against
  `str.splitlines()` in testing), enforced at the single `ledger_append`
  chokepoint so a future caller that forgets to validate still cannot forge
  an entry. Filename-derived fields (`path=`, `file=`, `dest=`, `target=`)
  are *escaped* (`%XX`) rather than refused, so a legal-but-hostile name is
  still witnessed, faithfully, on one line. Readers split on `\n` only, so a
  line poisoned by an older version is inert — and raises a `LEDGER-ANOMALY`
  alarm (never a gate) instead of being inert silently.
- **Output filenames** derived from a member's name (the evict package) are
  stripped of separators and control characters and length-bounded; an
  oversized name used to crash `evict` with a raw `ENAMETOOLONG` traceback.
- Stated residual: this closes forgery *through a legitimate write path*.
  Anyone who can append to the ledger directly can still write a well-formed
  line: ledger text stays authored text (RESIDUAL_RISK item 7), and a ledger
  and workspace subverted together fail together (item 3). Both unchanged.

## Inventory tripwire (v1.2.2)

What this tool can write or spawn is an inventory, not an impression.
`tests/check_sinks.py` (suite test T40) scans `scripts/backup_chain.py` and
compares every filesystem-write, process-spawn and archive-write call, the
import set, and the file set of `scripts/` against `tests/sink_registry.txt`.

- New, changed or stale rows fail the suite until someone classifies them with
  a reason. Pathname-reopening writers (`shutil.copy*`/`move`,
  `open(…,'w'/'x')`, `os.open`) are **not registrable**: they follow a planted
  symlink at a predictable name, which is how 1.2.1 shipped the stow defect.
  Run against 1.2.1's script, the tripwire names it.
- The import allow-list makes *"no network code in this script"* a checked
  claim. It does not make "no network" one: commands the operator supplies
  (`--stow-cmd`, a ledger adapter) run through `consent-exec` and can reach a
  network by design.
- The tripwire is itself tested by planting each kind of drift (T40). It
  records decisions; it does not verify them. Blind spots: RESIDUAL_RISK 14;
  method: `references/METHOD.md`.

## What the restore drill does and does not see (v1.2.2)

`build`'s G8 and the standalone `drill` are a **read-back**: every manifest
member is re-read from the decoded archive and hash-verified; nothing is
written to disk. They see corruption, truncation and missing members. They
cannot see a failure of the filesystem a real restore writes to. Through 1.2.1
the gate message said members were verified "in `.vault/drill`" and
`PROTOCOL.md` said G8 "re-extracts every member to staging"; neither was true
(the directory was created and cleared but never written to), so the message
and the docs now say what the code does. See RESIDUAL_RISK item 15.

## Trust boundaries

- **No network.** No sockets anywhere in the script. Off-site copies are made
  by the user; verification of those copies is the roundtrip pattern in
  `references/PROTOCOL.md`.
- **No content inspection.** Member bytes are hashed and streamed. Nothing is
  parsed, logged, or transmitted. Worklog-style metadata (manifest `carries`
  notes and v1.1 decision traces) is the only text the tool handles beyond
  paths and hashes — keep secrets out of both.
- **Archive path safety.** Names are validated on every read (absolute paths,
  `..`, NUL, backslash-normalized members). Extraction is bounded to
  `--target` in both senses: the names, and the filesystem — a pre-existing
  symlinked directory beneath the target would redirect writes outside it,
  so restore refuses (exit 2, unconditional) when any destination component
  under the target is a symlink, and a symlink at the final component is a
  conflict replaced only via `--overwrite` (which swaps the link itself,
  never the link target).
- **Symlinks** given directly as a member path are skipped (warned) — you are
  told, and nothing is silently dereferenced at the top level. A symlinked
  *file* found while walking a directory member is dereferenced **only if
  its resolved target stays inside the project root** (checked with
  `realpath` + `commonpath`, never string prefixes): the archive stores the
  link target's current content, and the manifest hash is computed over that
  same content — both must agree, or every restore drill on that member
  would fail. A symlinked *subdirectory* is held to the same boundary: `os.walk`
  never descends into a directory symlink either way (so an out-of-root one
  was already contributing no file content), but its bare name is now also
  excluded rather than left behind as an empty directory placeholder — the
  same "not part of what you selected" rule applies to a name as to bytes.
  A link (file or directory) resolving *outside* the root is skipped with a
  warning and enters neither the manifest nor the archive — no trace, not
  even an empty one, and no archive content or structure can escape the
  declared read boundary through a link planted inside a member directory.
  A *broken* symlink found the same way is skipped with a warning and never
  enters the manifest at all, so there is no member for the listing check to
  flag — it is absent by exclusion, not by silent corruption.
- **Non-regular files** (FIFOs, sockets, devices — including symlinks pointing
  at them) are skipped with a warning: hashing them would hang the build or
  crash it, and no archive format here would represent them honestly anyway.

## Known limitations (stated, not hidden)

- The symlink boundary checks validate a path, then use it: a process that
  swaps the link between the check and the read (TOCTOU) is not defended
  against on the **read** side — member collection and archive reads are
  still check-then-use. That would require O_NOFOLLOW / descriptor-relative
  I/O throughout, which the threat model here does not call for — the
  adversary is infrastructure amnesia, not a local process racing the
  backup. The **write** side is descriptor-based as of v1.2.1 (staging is
  `mkstemp` + fd-written + `os.replace`), so the race class the auditor
  flagged — writes redirected through a pre-planted staging symlink — is
  closed; what remains open is a hostile destination directory's control
  over its own entries, which no tool can give back. Stated so you can
  decide differently for your own deployment.

- The manifest is inside the archive and the chain is hash-linked, but nothing
  signs anything: an attacker who controls the machine at build time controls
  the archive. The protocol detects accidents and infrastructure amnesia, not
  malice with build-time access.
- The `file` ledger inside the workspace dies with the workspace by design —
  use `--ledger-file` outside the machine for real protection, and treat the
  in-workspace ledger as a test convenience.
- Generation uniqueness across **different machines/chains** requires distinct
  ledger channels; two chains sharing one ledger will fight over the counter
  (and, being append-only, will be visible doing it).
