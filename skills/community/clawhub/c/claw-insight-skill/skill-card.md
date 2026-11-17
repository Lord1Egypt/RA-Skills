## Description:

ClawInsight helps an agent draft market-research survey answers for the user to review, edit, and approve before sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tgzhou98](https://clawhub.ai/user/tgzhou98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use ClawInsight to draft answers for brand research surveys from approved profile and conversation context. The skill is intended to submit only answers the user has reviewed and approved to the ClawInsight service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse profile details and prior chats to draft market-research answers for an external service.

Mitigation: Require explicit per-session and per-answer review, and avoid sharing sensitive facts or direct quotes.

Risk: The ClawInsight API key can authorize actions if exposed.

Mitigation: Store the API key only in a secure credential store and send it only to the declared ClawInsight API.

Risk: Bulk drafting can lead to guessed or inaccurate survey answers.

Mitigation: Review every drafted answer, skip uncertain answers, and avoid approving bulk guesses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tgzhou98/skills/claw-insight-skill)
- [ClawInsight Homepage](https://claw-insight.vercel.app)
- [ClawInsight Skill API](https://claw-insight.vercel.app/api/skill)
- [Metadata-Declared Source Repository](https://github.com/ClawInsight/claw-insight-skill)
- [Metadata-Declared Publisher URL](https://github.com/ClawInsight)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before survey response submission and communicates with the ClawInsight API.]

## Skill Version(s):

0.1.18 (source: server release metadata); artifact SKILL.md and package.json report 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
