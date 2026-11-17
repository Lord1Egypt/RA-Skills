## Description:

Correction Memory helps agents persist user corrections by logging them per agent type and replaying recent corrections in future agent prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donovanpankratz-del](https://clawhub.ai/user/donovanpankratz-del)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to capture corrections to repeated agent mistakes and inject relevant recent corrections into future sessions for the same agent type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores free-form correction text and can replay it as future agent instructions.

Mitigation: Do not record secrets, private context, or broad behavioral instructions as corrections; review and delete memory entries before using the skill with higher-privilege agents or shared workspaces.

Risk: Local cross-session memory can preserve stale or unwanted behavior across agent runs.

Mitigation: Review correction files periodically and rely on the skill's recent-entry replay behavior so outdated corrections do not accumulate in prompts.

## Reference(s):

- [correction-tracker-template.js](references/correction-tracker-template.js)
- [ClawHub skill page](https://clawhub.ai/donovanpankratz-del/skills/correction-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets; runtime correction memory is stored as JSONL and replayed as markdown preambles.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores free-form correction entries locally for up to 30 days before replay into future same-agent prompts.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
