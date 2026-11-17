## Description:

Screens antibody and other biological sequences for similar-sequence patent hits, patent-family relevance, and preliminary FTO risk before formal legal analysis.

This skill is for research and development only.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, patent analysts, and antibody R&D teams use this skill to run preliminary sequence-level FTO screening for therapeutic antibodies before detailed patent counsel review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided antibody sequences may be confidential when used with external patent-search tools.

Mitigation: Confirm that external patent-search use is acceptable for the relevant confidentiality and legal workflow before installing or using the skill.

Risk: Preliminary patent and FTO screening can be mistaken for formal legal advice.

Mitigation: Use the output for research triage only and have patent counsel review claims before making FTO conclusions.

Risk: Patent or sequence conclusions may be unsupported when source tools return no relevant data.

Mitigation: Keep conclusions tied to traceable source markers and state explicitly when tools return no matching results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/antibody-sequence-fto)

## Skill Output:

**Output Type(s):** [text, html, guidance]

**Output Format:** [HTML report with source-linked analysis tables and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preliminary research output only; formal FTO conclusions require patent attorney review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
