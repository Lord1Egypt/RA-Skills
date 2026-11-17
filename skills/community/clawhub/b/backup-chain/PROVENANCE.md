# PROVENANCE — backup-chain

**Origin.** Distilled 2026-09-25 from a production backup chain that ran for
nine days across 14 workspace wipes (generations 1–59, ~1,300 files per
archive) in a sandboxed agent environment. Every rule in this skill has a
named incident behind it — the mtime trap, the stale handoff, the silent
zero-write bulk extraction (hit twice), the filename-collision parent, the
clean-completing stale restore.

**Design partners.** Co-developed by an AI agent (Super Z / GLM) and a human
operator. The human's contributions are structural: the demand that the skill
be **platform-agnostic** (no exact external services — users plug their own via
the command adapter), that it work **local-only by default** with off-site
distribution handled by the user, and that it contain **no personal data, no
credentials, and no platform identifiers** from the originating deployment.
The production system this was distilled from does use specific platforms; none
of them are named here, and nothing from their configurations survived the
abstraction.

**Dogfooding.** The skill was validated against a synthetic-workspace test
suite (14 scenarios, 47 assertions) before release; the suite caught two real
protocol bugs on its first run — a fencing gap (live-but-silent ledger skipped
the local-chain stale refusal) and an overwrite bug (`--overwrite` classified
conflicts but never restored them). Both fixes are argued in PROTOCOL.md.
The skill then went through an independent external review: six crash/UX
fixes (nested-symlink dereferencing, broken-symlink crash, drive-letter
hardening, single ledger read per restore, dry-run conflict preview, clean
refusals for missing arguments) were verified and adopted wholesale as
v1.0.1, with one further guard (non-regular-file hang protection) added in
the final pass because it belonged to the same defect family the review had
addressed. The ClawHub automated audit then found the two boundary escapes
that the dereferencing design had left open (reads out of the project root
through nested links; restore writes out of the target through symlinked
directories); 1.0.2 closes both with containment gates and the suite grew to
77 assertions — and immediately caught the first implementation of the
restore gate examining the wrong path components. Three defect classes,
three catches by the same drill-before-trust loop. The audit's second round
(against 1.0.2) returned 14 findings: the two 1.0.1-era escapes verified
gone, one finding (silent command-adapter execution) adopted as the 1.0.3
runtime warning, and thirteen triaged as duplicates, test-fixture false
positives (the scanner read the suite's own symlink fixtures as runtime
behavior), or deliberate documented design — every triage decision is
argued in the 1.0.3 CHANGELOG entry. The audit's third round (against 1.0.3)
elevated the command adapter to a full High finding (T09): the 1.0.3 warning
fires but does not ask consent, so a planted config still executed on routine
subcommands — the scanner itself noted the feature is legitimate for
deliberately configured commands. 1.0.4 answers with refuse-by-default
execution behind an explicit per-invocation `--allow-cmd-ledger` and
argv-only (`shell=False`) command execution; the warning stays, the silent
path is gone. One honest defect admitted in the same pass: the script's
`VERSION` constant had lagged at 1.0.1 through two doc-only releases. The
audit's fourth round (against 1.0.4) returned the T09 label with a different
finding behind it — the reading-side twin of round 3: a workspace-contributed
config could redefine the backup root and collect files outside the selected
project, with `output_dir`/`chain_name` steering where the archive lands.
1.0.5 closes the config path boundary the same way the execution boundary was
closed — the config proposes, the invocation root and the operator dispose:
root pin with refuse-on-mismatch, member re-validation at load, chain_name
and output_dir containment, `--output` as the per-invocation escape hatch;
the suite grew to 119 assertions, first-run green. The audit's fifth round
(against 1.0.5) held the T09 label but downgraded it to Warning/Medium and
narrowed it to the one sink 1.0.5 had deliberately left open — `ledger.file` —
with the scanner crediting the rest of the boundary in its own analysis.
1.0.6 concedes the point and closes it with the same consent class as the
command adapter: `--allow-external-ledger` (refuse-by-default, all
subcommands), realpath containment resolved at every use so planted or
swapped symlinks fail closed, shape validation of the ledger object at load,
and the wipe-safety setup preserved with the destination chosen in the
operator's own voice. The suite grew to 151 assertions — which also caught
and repaired a latent round-4 test bug (a bogus `ledger.ledger` config
subkey meant the "absolute ledger path accepted" assertion never exercised
an external path at all); the production code needed no such repairs.

**v1.1.0 (2026-09-26).** The witness layer — the first feature release — has
three parentage lines. The operator's philosophy set the frame: no guarantees
exist anywhere, we operate with probabilities, and the work is drawing the
acceptable-risk line before control-striving ruins everything; that line is
now references/RESIDUAL_RISK.md, and the release adds witnesses (decision
traces, acks, event lines) rather than guards on exactly that reasoning. The
operator's own feature idea — a very compressed chain-of-thoughts record per
generation — became the decision trace. And the ecosystem independently
demanded the same primitive: doctor_memory ("preserve inference steps instead
of identity") and katarina_martinity ("the receipt is written at decision
time") arrived at the invariant from other corners of the same network the
week this was drafted. A live incident the same day (a dotdir rollback eating
the operator's platform credentials, healed in two minutes by the Sep 23
archive's receipt + per-member extraction) supplied the empirical reminder
that the baseline already works — witnesses record how, not why not.

**v1.2.0 (2026-10-09).** The curation layer — the second feature release,
born when the production chain this skill was distilled from crept toward its
size ceiling again and a dead-weight audit slimmed it. The generalization
question ("what in that audit is skill-material?") produced three
proposals; the operator's three rulings shaped all of it, and the first two
are literally the skill's founding constraint re-applied by its own author:
no agent using this skill can be assumed to have storage beyond its own
(side-bucket features became per-invocation options, never defaults), and no
two workspaces look alike (exclusions became a per-member option, never a
default). The third ruling approved the audit's detections as failsafes —
implemented advisory, never gating, per the witness-not-gate doctrine. A
fourth ruling folded in before publishing: the ack disposition the
production deployment has lived under since September 26 ("acks: N/A —
chat-only operator; the human cannot run a shell, and an agent-typed relay
ack would be self-certification borrowing the operator's voice") became a
formal option, `ack-policy`, with the operator's own boundary on it:
disabling acks may never be traceless — a no-ack chain must say so where an
ack would have said otherwise, "no ack mentioned as much as ack, for
honesty." The refusal without a reachable ledger is that boundary
implemented: an un-witnessable policy change is refused, not made. The
`evict` command is the audit's workflow made protocol: in production, dead
weight left the chain as a silent config edit whose "why" and "where did it
go" lived only in a conversation a later session could not find; eviction is
now a packaged, hash-receipted, destination-verified, witness-recorded act
that refuses to drop custody when the hand-off fails. Version discipline
note for the record: possession of the skill had drifted (a platform
rollback reverted the local tree to v1.0.1 while ClawHub held the audited
v1.1.1); the possession was re-synced from the verified package BEFORE any
v1.2 work began, so 1.2.0 descends from the true published line, not from
the stale snapshot — the sync itself is the mtime-trap lesson applied to the
skill's own source.

**License of intent.** Copy it, fork it, port it. If it saves you one wipe, it
paid for itself.

**1.3.0 line discipline.** Version-discipline note, same rule as the 1.2.0
sync above: the 1.3.0 work descends from the audited 1.2.2 package (independently
reproduced before adoption — suite, sink tripwire, and the 22-assertion
mutation check against shipped 1.2.1), installed from the verified package
bytes into the skill directory BEFORE any 1.3.0 edit, after a restore from
the true chain head (g71). The stale local install (1.1.1, behind the
published 1.2.x line) was replaced by adoption, not edited in place — the
possession again follows the published line, not the other way round.

**1.3.1 line discipline.** Same rule, third verse: 1.3.1 descends from the
published 1.3.0 package, changed only after the finding was reproduced
against the shipped bytes (planted `archive_mode: 666` → world-readable
archive + receipt, rc 0) and the fix was mutation-checked against those same
bytes (new T43 family: 12 failures on 1.3.0, all in the new family). The
change is one rule at one resolution point per command; no gate, ledger
format, or exit-code contract changed for legal narrow-mode inputs.

**1.3.2 line discipline.** Fourth verse: 1.3.2 descends from the published
1.3.1 package, changed only after the finding was reproduced against the
shipped bytes (symlinked `output_dir` component → eviction package + receipt
outside the workspace, rc 0) and the fix was mutation-checked against those
same bytes (new T44 family: 8 failures on 1.3.1, all in the new family).
One containment, one helper, two callers; build's round-4 refusal message
and the `--output`/`--stow-*` escape hatches are byte-unchanged, so no legal
workflow changes shape — only the escape class loses its rc 0.
