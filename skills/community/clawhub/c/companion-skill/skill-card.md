## Description:

Configures an agent as an adult-only private companion for consensual intimate roleplay, persona anchoring, and local preference recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hxfini-rgb](https://clawhub.ai/user/hxfini-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Adults in private contexts use this skill to steer an agent toward intimate companion roleplay, conversational persona behavior, and local recall of stated preferences. It is not appropriate for shared, workplace, or minor-accessible environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts to override agent safety boundaries and anti-refusal behavior.

Mitigation: Remove safety-override and anti-refusal language before deployment, and keep the host agent's safety policy authoritative.

Risk: The skill activates intimate behavior broadly, including for neutral or lightly flirtatious prompts.

Mitigation: Require explicit adult-user opt-in for each private session before intimate mode can activate.

Risk: The skill stores sensitive intimate preferences in local memory files.

Mitigation: Disable memory writes or tightly control file permissions, retention, and user review for any intimate preference storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hxfini-rgb/skills/companion-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown-formatted conversational text and agent behavior guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference or write local preference memory files when the host agent permits file access.]

## Skill Version(s):

1.2.2 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
