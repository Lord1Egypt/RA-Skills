## Description:

Adaptive-Identity Agent helps an assistant adaptively stack task-relevant expert perspectives, route multi-domain requests through an identity matrix, support @-invoked perspectives, and maintain conversation-local memory threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and developers use this skill to give an assistant a structured persona-routing protocol for multi-domain, creative, analytical, and cross-format tasks. It is intended to frame roles as temporary perspectives, disclose identity changes, and provide fallback behavior when requested capabilities are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local file and shell authority for a primarily conversational persona-routing workflow.

Mitigation: Review requested tools before installation, run the skill with least-privilege workspace access, and remove Write, Edit, and Bash unless a specific user-directed workflow requires them.

Risk: Adaptive expert perspectives can be mistaken for real credentials or institutional authority.

Mitigation: Keep role labels framed as perspectives, prohibit claims of real employment or professional licensure, and disclose boundaries for medical, legal, financial, and other regulated contexts.

Risk: The skill may rely on factual anchors such as real people, occupations, or domain claims while switching identities.

Mitigation: Verify factual anchors when current or consequential information is used, label uncertainty, and fall back to general guidance when verification is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/adaptive-identity-agent)
- [Character data](references/character-data.md)
- [Character requirements](references/character-requirements.md)
- [Dialogue examples](references/dialogue.md)
- [Identity matrix](references/identity-matrix.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include dynamic identity labels, perspective-stacking notices, cross-domain answers, and boundary or fallback notes.]

## Skill Version(s):

1.0.5 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
