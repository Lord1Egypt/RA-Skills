## Description:

Generates personalized Chinese blessing and greeting messages from recipient, relationship, occasion, style, length, and recent-context details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to draft personalized Chinese greetings for holidays, festivals, and life events. It can tailor tone and wording for recipients such as family members, friends, managers, customers, and peers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Greeting prompts may include recipient descriptions, relationship details, and recent-life context that are sent to a configured remote LLM provider.

Mitigation: Avoid sensitive personal information, disclose remote processing to users, and only run the skill when the selected provider is acceptable for the data being entered.

Risk: The configured API key and endpoint can be mismatched or pointed at an unvalidated remote host.

Mitigation: Set provider credentials and endpoint deliberately, validate trusted HTTPS hosts, and couple each API key to its intended provider before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antonia-sz/skills/blessing-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/antonia-sz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with three generated Chinese blessing variants and a short usage tip]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable festival or occasion, target recipient, relationship, recent context, style, and length inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
