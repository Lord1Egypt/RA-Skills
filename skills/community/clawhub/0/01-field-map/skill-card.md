## Description:

Use when the user is new to a research direction and wants to scan papers to understand branches, representative works, common methods, benchmarks, metrics, saturated areas, and unclear areas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snake-fan](https://clawhub.ai/user/snake-fan)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and technical teams use this skill to build a field map for an unfamiliar research direction, including boundaries, seed papers, literature expansion, clusters, and evidence-backed opportunity candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper discovery may be incomplete when network access is unavailable or the user has not provided paper links.

Mitigation: Disclose unavailable searches and ask the user for paper links or permission to continue when network access is available.

Risk: Research opportunity candidates could become unsupported speculation if they are not tied to specific paper evidence.

Mitigation: Require opportunity candidates to link back to paper records and use the skill's confirmation gates before expanding the paper set.

Risk: Referenced formatting templates are not present in the provided artifact, which may affect consistency of generated files.

Mitigation: Review or supply the referenced templates before depending on standardized output formatting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snake-fan/skills/01-field-map)
- [Publisher Profile](https://clawhub.ai/user/snake-fan)
- [Server-Resolved GitHub Source](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/01-field-map)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown files and a zero-build static HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a structured field-map workspace with boundary, paper records, search strategy, clusters, research opportunities, and an index.html report.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
