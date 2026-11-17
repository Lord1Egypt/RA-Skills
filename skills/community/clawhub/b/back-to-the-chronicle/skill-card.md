## Description:

Back to the Chronicle reconstructs missing founding or historical project Chronicles from approved session logs, Git history, artifacts, receipts, traces, ledgers, and external-state readbacks while preserving evidence-class boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to recover project history, founding decisions, abandoned experiments, corrections, and evidence-backed Chronicle entries from explicitly approved local sources. It supports a proposed manifest and manual Chronicle integration while keeping private evidence and public summaries separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project and session inventories can expose private paths, identifiers, Git metadata, hashes, or sensitive source material when broad stores are scanned.

Mitigation: Use only explicitly approved project roots and session stores, keep generated inventories private, and review derivatives for the intended audience before disclosure.

Risk: Retrospective narratives can overstate inferred intent or turn historical results into live capability.

Mitigation: Classify claims as witnessed, artifact-measured, or inferred intent; keep the required inferred-intent warning and verify anchors before appending or acting.

Risk: Unpinned external install sources may differ from the reviewed release.

Mitigation: Install only from trusted repositories or package versions and pin or verify reviewed commits or releases.

Risk: Canonical Chronicle updates may mutate an operational history beyond the analysis authorization.

Mitigation: Prepare a proposed manifest first and append to a Chronicle only after separate approval of destination and mutation scope.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antreasantoniou/skills/back-to-the-chronicle)
- [Chronicle Compatibility](references/chronicle-compatibility.md)
- [Backfill Evidence Standard](references/evidence-standard.md)
- [Session JSONL Custody](references/session-jsonl-custody.md)
- [Public Chronicle CLI](https://github.com/AntreasAntoniou/chronicle)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown narrative, JSON manifests, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create private inventory/session JSON files and proposed Chronicle manifests; canonical writes require separate approval.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
