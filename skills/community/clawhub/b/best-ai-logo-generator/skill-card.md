## Description:

Generates professional logos, brand icons, app icons, favicons, and other visual identity assets through ailogogenerator.online.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq919006380](https://clawhub.ai/user/qq919006380)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in Claude Code to turn brand requirements into generated logo image files, including icons and visual identity assets. The skill handles login, generation requests, polling, and local download of the finished logo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends logo prompts and brand details to ailogogenerator.online.

Mitigation: Use it only for information you are comfortable sharing with that third-party service, and avoid confidential brand plans or sensitive customer data.

Risk: The skill stores and reuses a local bearer token.

Mitigation: Keep ~/.config/ailogogenerator.online/auth.json protected, do not display or share the token, and delete the file to log out or rotate accounts.

Risk: Each logo generation can spend service credits.

Mitigation: Use explicit invocation and confirm generation parameters before making requests, especially for multiple variations.

Risk: The skill downloads generated files into the working directory.

Mitigation: Review the generated download URL and destination path before saving, and use descriptive filenames to avoid overwriting important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq919006380/skills/best-ai-logo-generator)
- [Publisher profile](https://clawhub.ai/user/qq919006380)
- [AI Logo Generator service](https://ailogogenerator.online)
- [Claude Code CLI](https://claude.ai/code)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and generated PNG logo files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or reuses a local auth token at ~/.config/ailogogenerator.online/auth.json and saves generated logo images to the current working directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
