## Description:

UUID inspector that parses UUIDs, reports version and variant, and extracts timestamps for UUID v1 and v7 plus MAC addresses for UUID v1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze, validate, or audit UUIDs, including checking UUID version consistency and extracting available timestamp or node identifier data from time-based UUIDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: UUID v1 analysis can reveal embedded timestamps and node identifiers.

Mitigation: Use the skill only on UUIDs and batch files that are intended for inspection, and treat extracted MAC or timestamp data as potentially sensitive.

Risk: The manifest evidence is stale relative to the packaged SKILL.md hash.

Mitigation: Review package hashes from current server evidence before relying on the manifest for integrity checks.

Risk: UUID v6, v7, and v8 support is documented as partial, and Microsoft variant validation is not strict.

Mitigation: Use results for inspection and triage, and confirm edge-case UUID interpretations with a standards-compliant parser when correctness is critical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-uuid-analyzer)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Code]

**Output Format:** [Plain text or JSON from CLI usage, with Python dictionary results when used as a local module.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local UUID inspection; batch mode reads one UUID per line from a user-selected file.]

## Skill Version(s):

0.1.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
