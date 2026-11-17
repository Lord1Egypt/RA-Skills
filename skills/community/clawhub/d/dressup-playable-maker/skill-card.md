## Description:

Create dress-up style playable ads for mobile advertising platforms like Mintegral, using customizable character, clothing, background, and UI assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxnan](https://clawhub.ai/user/lxnan)

### License/Terms of Use:


## Use Case:

Developers and ad creative teams use this skill to generate or customize mobile dress-up playable ads with selectable fashion items and campaign CTA behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated playable ads may redirect users to an unintended campaign destination.

Mitigation: Review the generated CTA behavior and verify the destination URL before publishing.

Risk: Generated HTML may be unsafe when built from untrusted asset folders or copied command lines.

Mitigation: Use trusted asset directories, inspect generated files, and scan the output before deployment.

Risk: Playable-ad creative may behave differently across ad networks or mobile devices.

Mitigation: Test the generated ad in browser, mobile, and target platform environments before release.

## Reference(s):

- [Dressup Playable Maker on ClawHub](https://clawhub.ai/lxnan/skills/dressup-playable-maker)
- [Dressup Playable production guide](references/guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated playable-ad files such as HTML, JavaScript, and copied assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated ads should be reviewed before publishing, with special attention to asset sources and CTA destinations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
