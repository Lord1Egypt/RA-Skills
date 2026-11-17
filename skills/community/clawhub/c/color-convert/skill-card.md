## Description:

Converts colors between common formats, generates palette options, checks WCAG contrast, and helps prepare color output using a local pure-Python utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and other external users use this skill to convert color values, generate palette options, and evaluate WCAG contrast for UI and design work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented named-color lookup and CSS export behavior may be incomplete in the inspected script.

Mitigation: Verify required color commands in the local utility before relying on those features in release or production workflows.

Risk: Color and contrast results can still be misapplied if design context, text size, or accessibility requirements are not reviewed.

Mitigation: Review generated colors and WCAG contrast outputs against the target UI requirements before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/darbling/skills/color-convert)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown prose with optional inline code and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local pure-Python utility; security evidence found no hidden access, persistence, credential use, or network behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
