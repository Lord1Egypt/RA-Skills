## Description:

When blocked, report the exact blocker, attempts made, and minimum user input needed to enable fast unblock without back-and-forth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to have agents produce structured blocker reports with exact errors, attempted remedies, the smallest needed user input, and a fallback option.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blocker reports can accidentally expose credentials, tokens, or sensitive local paths when error messages are copied verbatim.

Mitigation: Redact tokens and keys from error messages, use generic paths when sensitive, and avoid pasting real tokens or sensitive paths back into chat.

Risk: A blocker report may be less actionable if the agent stops before trying a corrected retry and a fallback path.

Mitigation: Require at least two documented attempts before reporting a blocker, then include the smallest needed user action and one fallback option.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dalomeve/skills/blocker-min-input)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown blocker report with bullets and inline code where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires exact blocker text, at least two documented attempts, minimum unblock input, and a fallback option.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
