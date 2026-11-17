## Description:

Checks whether citation keys stayed in the same Markdown `###` subsections after editing, so citation drift is reported before claim-to-evidence alignment is lost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill after draft polishing to compare the current draft against a pre-polish citation-anchor baseline and produce a PASS/FAIL drift report. The intended workflow is audit-only and does not edit the draft content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is advertised as a small no-network citation checker, but the package includes broader research-pipeline tooling that can run scripts and persistently change workspace files, approvals, and reports.

Mitigation: Install and run it only in an isolated workspace with explicit filesystem and network limits, and avoid auto-approval or broad routing until the package contents match the declared scope.

Risk: The analysis-only description may not cover all bundled helper behavior.

Mitigation: Route the skill only for the citation anchoring audit, review bundled tooling before deployment, and do not rely on the no-network claim without runtime controls.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/willoscar/skills/citation-anchoring)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown PASS/FAIL report with citation drift details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes `output/CITATION_ANCHORING_REPORT.md`; reads `output/DRAFT.md` and `output/citation_anchors.prepolish.jsonl`.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
