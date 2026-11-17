## Description:

Emperor Reply applies a Chinese emperor-and-minister response style when the user explicitly asks to be treated as a ruler, including courtly address terms and an immediate return to normal assistant tone when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[millihous](https://clawhub.ai/user/millihous)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users can use this skill to give an assistant a concise Chinese ruler-subject roleplay style for compatible conversations while preserving higher-priority safety, system, and exact-format requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Roleplay style could interfere with strict output formats such as JSON, code, SQL, CSV, regular expressions, translation-only output, or one-line rewrites.

Mitigation: The artifact requires exact-format requests to stay exact and adds role tone only when it does not change the required output.

Risk: A conversational style mode could persist longer than the user intends.

Mitigation: The artifact requires the assistant to exit immediately when the user asks to speak normally or not use the mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/millihous/skills/emperor-reply)
- [Publisher profile](https://clawhub.ai/user/millihous)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Natural-language responses, with exact requested formats preserved when required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies are normally in Chinese and use the requested courtly address style only while the mode remains active.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
