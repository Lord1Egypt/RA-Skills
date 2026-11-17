## Description:

Use when the user wants a periodic competitor digest - what tracked competitors changed, where the gaps are - as a document, from observation history or public diffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

External users, SEO teams, and site owners use this skill to produce concise competitor-change readouts from public page diffs, prior crawls, or TrustGrowth observation history. The output is intended for periodic reporting, gap triage, and owner-reviewed follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evidence validation depends on an external Groundcrew validator discovered in the active skills root.

Mitigation: Install only in trusted Groundcrew environments and prefer a version-pinned, bundled, or signed validator before using the skill with broad filesystem, credential, or network access.

Risk: Competitor comparisons may be misused as outward-facing claims.

Mitigation: Require owner review before publishing competitor-naming comparisons or irreversible recommendations.

Risk: Third-party traffic or ranking data can be mistaken for measured competitor facts.

Mitigation: Label third-party numbers as Estimated, name the estimator, and avoid presenting estimates as a competitor's actual performance.

## Reference(s):

- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with tables, verdict labels, action items, and evidence references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SHIP, FIX, BLOCK, and UNDECIDED verdicts; labels facts as Measured, User-provided, or Estimated.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
