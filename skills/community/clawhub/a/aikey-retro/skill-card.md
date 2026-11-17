## Description:

Reviews short-video performance against pre-publish expectations and records validated lessons for future content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

Solo knowledge creators use this skill to review published short videos against pre-publication predictions, identify evidence-backed lessons, and choose a next action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Companion instructions and agenda configuration were not bundled, so constraints that depend on those files cannot be confirmed from this release.

Mitigation: Before relying on cross-skill memory updates, confirm the intended companion files and content-vault configuration are available.

Risk: The workflow can update local memories and performance-tracking records.

Mitigation: Review proposed record changes and share only the analytics and audience messages needed for the review.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/iamzifei/skills/aikey-retro)
- [AI KEY rename and upgrade notes](https://github.com/iamzifei/aikey#老用户升级zmm-已改名为-ai-key)
- [Built-in review criteria](artifact/references/规则卡.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Files]

**Output Format:** [Markdown review and next-step guidance; may update configured local Markdown memory and tracking files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local memory and performance-tracking records in the configured content vault.]

## Skill Version(s):

0.3.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
