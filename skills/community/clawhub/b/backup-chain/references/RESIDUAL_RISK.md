# RESIDUAL RISK — backup-chain (the acceptable-risk line, v1.2)

This annex is the line, not a disclaimer. It says what this skill does **not**
protect against, in one place, versioned with the code — so that every future
control addition has to pay for itself in honesty before it pays for itself in
safety.

## Standing premise

Nothing here is guaranteed. The protocol operates with probabilities: an
error probability that looks negligible will be ignored until it fires
spectacularly, and the correct response to that fact is not infinite
hardening — it is an explicit line between acceptable and unacceptable risk,
drawn *before* the strive for control ruins everything, the operators
included. Of the three values this kind of engineering usually serves —
scientific detachment, efficiency, control — control is the one whose
uncorrected excess does the most damage, because every control is also a new
failure surface wearing the costume of a fix.

## What backup-chain does NOT protect against

1. **Operator coercion or compromise.** The human is inside the trust
   boundary by definition. A coerced operator acks lies, approves bad
   registrations, and can rewrite every doc you are reading.
2. **Full workspace compromise at build or restore time.** An attacker who
   controls the machine controls the bytes, the manifest, the trace, and the
   drill. The chain detects accidents and infrastructure amnesia; it does not
   detect malice with build-time access.
3. **Ledger + writer co-subversion.** If the ledger channel *and* the
   workspace are subverted in coordination, the two-witness model of v1.1
   adds no separation — its alarms all come from witnesses that fail
   together.
4. **Silencing.** Deleting the archive store and the ledger together ends the
   chain. Append-only is not indestructible; it is unforgeable-in-place at
   best, and only until silenced.
5. **The restoring process itself.** G1–G8 verify the archive's past; they
   cannot verify the process doing the restoring, the target filesystem's
   future, or the operator reading the output.
6. **Shared-ledger counter fights.** Two chains pointed at one ledger channel
   will fight over the generation counter — visibly, but only to someone who
   reads the ledger.
7. **The witness lying surfaces.** Decision traces, acks, and event lines are
   authored text and forgeable like any ledger text. What bounds the damage:
   traces make checkable claims (`b` vs the member map, `f` by construction),
   so a lie tends to leave a detectable disagreement with evidence that
   survived it. *Tends to* — that is a probability, priced honestly.
8. **Curation holes (v1.2).** An exclude pattern is a hole punched in every
   future archive, and it is the one control in this skill whose failure
   produces no signal at build time: a mistyped pattern simply removes paths,
   silently, forever. The compensations are human — `member list` shows the
   patterns, `status` prints raw weight so missing weight can be noticed,
   wrong shapes refuse at load — but a human has to look. Detections cannot
   see what was never collected; neither can any witness. Curation is the
   place where this skill's "loud or refused" doctrine structurally cannot
   reach, and that is the price of making archives match a workspace instead
   of a template.
9. **Claimed custody (v1.2).** `evict`/`build --stow-cmd` accept a foreign
   command's exit code as its claim of successful off-site custody; the
   skill cannot hash-check what that command did with the bytes. The output
   says "claimed, not verified" and the `--stow-to` path remains the only
   hash-verified hand-off, but a claimed stow is a probability, priced
   honestly: the witness line records that a command was *told*, not that
   bytes *landed*. An eviction whose package survived only in a lying
   command's destination is a loss the chain will report as custody
   established.
10. **Detector habituation (v1.2).** The DETECT warnings are advisory by
   design, sized off raw bytes (not compressed weight), blind to excluded
   paths (item 8), and blind to growth between non-adjacent generations. A
   detector that never gates is one that can be safely ignored — and a
   signal that can be safely ignored eventually is. The failsafe against the
   failsafe is the same one this annex always names: a human who reads the
   numbers at `status` occasionally, especially after curation changes.
11. **Ackless legitimacy (v1.2).** The ack policy makes a no-ack chain a
    first-class state, and the ONLY thing distinguishing "disabled by
    decision" from "nobody watching" is one authored ledger line
    (`event=ack-off`) — forgeable like any ledger text, so a forged policy
    line launders neglect into policy. The compensations are placement and
    refusal, not strength: the line lives where an ack would have lived,
    both policy changes refuse without a reachable ledger (no witness, no
    policy), and `verify`/`status` attribute silence explicitly instead of
    leaving it to read as debt. And the record has the ledger's own
    mortality: a wipe that takes the ledger takes the policy record with
    it, and the distinction collapses back to the reader's judgment — the
    same probability, priced honestly, as every witness in this skill.
12. **Unpredictable staging (v1.2.1).** The staging hardening that closed the
    T09 round-6 write-escape also removed an observability signal: staging
    names can no longer be predicted, so an operator (or agent) can no longer
    watch for `.<name>.tmp` / `<archive>.part` files to observe a build or
    restore in flight. The compensations: exit codes and stdout stay loud,
    `--dry-run` still previews, and crash leftovers carry the `*.part`
    suffix so they remain visible to a directory listing and excluded from
    collection. And the underlying residual stands regardless of staging:
    an attacker who controls a destination directory controls that
    directory — this hardening closes the out-of-boundary write primitive,
    not the trustworthiness of a hostile directory.
13. **Line discipline and stow staging (v1.2.2).** Two controls, three blind
    spots, named here because the standing rule requires it. (a) *Refusal over
    truncation* means a note that legitimately contains one of the refused
    characters is rejected, not trimmed — loud (rc 2, with the reason), never
    silent, and the operator rewrites it. (b) *Escaped filename fields* trade
    readability for safety, and `%` itself is not escaped, so a real filename
    containing the literal text `%0A` is indistinguishable in the witness from
    one containing a newline — a cosmetic ambiguity in a field that is
    evidence, not an index. (c) *The reader splits on `\n` only*, so a
    command-adapter channel that terminates records with some other separator
    would have its records merged into one line and its entries missed —
    which is why the reader also raises `LEDGER-ANOMALY` on any line holding a
    break character: a missed entry here is an alarm, not a quiet gap. The
    stow staging closes the planted-symlink write at a predictable name; it
    does not make a hostile stow directory trustworthy (item 12's residual
    applies unchanged).
14. **The inventory tripwire (v1.2.2).** The sink registry makes drift in what
    the tool can write or spawn visible; it does not make any sink safe.
    Blind spots: (a) it is *syntax over one file* — a sink reached through a
    construct the scan does not model is invisible to it, and only the file set
    of `scripts/` is guarded, not the rest of the tree; (b) registry reasons
    are authored text, so a hurried or compromised reviewer can write a
    plausible one — `TODO` and empty reasons are refused, a reason's truth is
    not checked (item 7's problem, one level up); (c) a function rename shows
    as one NEW and one STALE row, friction by design, and friction teaches
    people to regenerate-and-paste, which `--print` resists by emitting `TODO`
    and nothing else can resist; (d) it scans the script, not what
    operator-supplied commands launch — "no network *code*" is checked, "no
    network" is not and cannot be. It fails loud (rc 1, function named), and
    is tested by planting each kind of drift.
15. **The drill reads back; it does not rehearse a restore (v1.2.2).** G8 and
    `drill` hash members from the decoded archive stream and write nothing.
    They see corruption, truncation and missing members; they cannot see a
    failure of the filesystem a real restore writes to — disk full,
    path-length or character limits, permissions. `restore` verifies and
    reports per member and exits non-zero on any failure, so such a failure is
    loud at restore time rather than at drill time. A passing drill means "the
    archive reads back intact," not "restore will succeed on this machine." A
    true rehearsal (extract to a scratch directory) would close this at the
    cost of doubling the I/O; it is left to the operator, and named here so
    the word "drill" does not carry more than the check does.
16. **Archive file modes (v1.3.0; config narrow-only since v1.3.1).** The
   0600 default and `--archive-mode` decide who can READ an artifact, not
   who can TRUST it: a mode is a filesystem bit, not a verification. Blind
   spots: (a) the mode is applied verbatim, so an operator who relied on
   umask to narrow a wide mode now gets exactly what they typed — the G7
   line prints what landed; (b) group- or world-readable archives remain
   one explicit CLI flag away, on purpose — the residual is whatever that
   choice is pointed at; (c) since v1.3.1 (audit T09) the config key can no
   longer widen anything: 1.3.0 capped a planted value at 0666 and called
   the G7 line's visibility enough, and the audit was right that visibility
   is not consent — config may now only narrow (a group/other bit is
   refused, rc 2, before anything is written), so the widening residual
   moved entirely to the operator's own flag; (d) restored members land
   owner-only regardless of the archived modes (the staging discipline;
   true since v1.1, stated here first) — a shared-machine restore workflow
   that needs other readers must chmod after restore.
17. **Everything not listed.** The absence of a risk from this list means it
   was not seen, not that it does not exist. That is the standing blind spot,
   and it belongs at the end of every version of this annex.

## The standing rule (control-inflation guard)

> **Every future control addition must name, in the same version, the blind
> spot it creates — or it is refused as control-inflation.**

This is the meta-failsafe: failsafes fail from blind spots, and naming the
blind spot is the only failsafe on failsafes that does not multiply them. In
practice, for every proposed feature or gate, answer three questions in the
changelog entry:

- What new failure does this control itself introduce? (If the answer is
  "none," the answer is wrong — look again.)
- Which witness does it duplicate, and what does the duplication cost?
- Does its failure mode fail loud (marked, refused) or silent? Silent
  failures are refused on sight.

## Language discipline

Words are the cheapest place a risk line erodes. Across all v1.1+ documents
and command output:

- **Permitted:** *witness, raises cost, probability shift, detects, marks,
  refuses, evidence, alarm.*
- **Forbidden:** *guarantee, tamper-proof, secure against, unforgeable,
  prevents.* (Where this annex says "unforgeable-in-place" above, read it as
  shorthand for "rewriting in place is detectable by the hash chain" — which
  itself assumes the hashes were not computed by the attacker. See item 2.)
- **The list is an example set, not the discipline.** A banned-word filter
  only stops the exact strings on it; it does nothing about a synonym that
  quietly imports the same certainty a banned word carried — "impossible to
  alter unnoticed," "immune to silent rewrite," "ensures integrity" claim
  exactly what "tamper-proof" claims, and are equally forbidden. Whoever
  edits this annex or SECURITY.md checks new wording against the *claim*
  (does this still say something no probability can back?), not against
  whether it happens to dodge the four words above. An automated version of
  this check — scoring prose against a similarity model — was considered and
  rejected here: this codebase has no embedding model, no semantic-distance
  scorer, and (for command output) no access to whatever process is calling
  it, so a "detector" built from what's actually on hand would be a keyword
  list with extra steps, claiming a rigor it doesn't have. That is precisely
  the control-inflation the standing rule below refuses — a check does not
  get to skip paying for itself in honesty just because it sounds like it
  measures something.

## Versioned movement

The risk line moves only by an explicit decision recorded in this annex with
the version that moves it, never by silent accumulation of one more
harmless-seeming check. If a change and its annex entry cannot be written in
the same commit, the change waits.
