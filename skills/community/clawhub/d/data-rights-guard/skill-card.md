## Description:

Helps assess training, fine-tuning, and evaluation data for traceable sources, licensing, commercial-use restrictions, and attribution requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT (Python code only); documentation and theory: All rights reserved

## Use Case:

Developers and data teams use this skill to screen dataset manifests before training, fine-tuning, or evaluation, flagging missing licenses, non-commercial restrictions, attribution gaps, and untraceable sources for review or exclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A lightweight license checker may miss legal or contextual restrictions and should not be treated as a complete compliance control.

Mitigation: Have a qualified reviewer verify actual license terms and authorization before admitting data to a training set.

Risk: Documentation describes CLI arguments that differ from the packaged manifest-based script.

Mitigation: Check the packaged CLI help and invoke it with a local manifest before relying on results.

Risk: Broad natural-language triggers may run checks for unrelated compliance requests.

Mitigation: Limit automatic triggering to explicit dataset-rights questions or require confirmation.

## Reference(s):

- [ClawHub release](https://clawhub.ai/zhaoxinghua09-cell/skills/data-rights-guard)
- [LGD theory (background reference, not release provenance)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON]

**Output Format:** [Text verdicts or JSON results for dataset manifest entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-entry status and issues; JSON mode includes an excluded count and advice.]

## Skill Version(s):

1.0.5 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
