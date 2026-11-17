## Description:

Review UI code for Web Interface Guidelines compliance and report findings for accessibility, design, UX, and best-practice checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrybenedict0515](https://clawhub.ai/user/terrybenedict0515)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and UI reviewers use this skill to audit web interface files against Web Interface Guidelines and receive concise file:line findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches changing remote guidelines at runtime, so review rules and output expectations can change between runs.

Mitigation: Review the fetched guideline source before use, or pin or vendor a reviewed guideline version for controlled environments.

## Reference(s):

- [Web Interface Guidelines source](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md)
- [ClawHub skill page](https://clawhub.ai/terrybenedict0515/skills/antfu-web-design-guidelines)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text or Markdown review findings in file:line format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings follow the output format specified by the fetched guideline source.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
