## Description:

Deep multi-source research agent for researching topics, questions, claims, literature reviews, competitive analyses, fact-checks, briefings, and cited reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharoonsharif](https://clawhub.ai/user/sharoonsharif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research-focused agent users use this skill to decompose research questions, gather and compare sources, track confidence, and produce cited research summaries or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local research index script can be tricked into reading Markdown files outside the intended research folder when given untrusted report slugs.

Mitigation: Review before installing, avoid untrusted report slugs, and prefer a patched version that validates slugs and confines report file access to the intended research directory.

Risk: Research outputs can become misleading if citations, source quality, or confidence levels are not reviewed.

Mitigation: Use the skill's triangulation, counterargument, citation, and confidence-rating steps, and review important findings against source material before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sharoonsharif/skills/claw-researcher)
- [Publisher profile](https://clawhub.ai/user/sharoonsharif)
- [Research Methodology Reference](references/methodology.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown reports and inline text with citations, confidence ratings, methodology notes, and optional local report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deep and exhaustive modes may save Markdown reports under the user's research directory and update a local research index.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
