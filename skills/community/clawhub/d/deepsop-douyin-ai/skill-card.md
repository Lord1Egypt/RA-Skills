## Description:

Automates Douyin login, account validation, and video or note publishing through social-auto-upload while preparing the local runtime for the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuoai](https://clawhub.ai/user/kukuoai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to help an agent prepare the social-auto-upload runtime, verify Douyin account state, and generate or run the appropriate commands for publishing videos or image notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the local environment by downloading and running third-party code through mirrors.

Mitigation: Review carefully before installation; prefer a version that pins and verifies the external repository and disables untrusted mirror fallback by default.

Risk: The skill can use local Douyin session data and publish content publicly.

Mitigation: Require explicit confirmation before login or publish actions, and run login only in the user's real local terminal.

Risk: Server security evidence reports broad authority with weak user controls.

Mitigation: Review commands before execution and require explicit user approval for actions that install dependencies, access session data, or publish content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kukuoai/skills/deepsop-douyin-ai)
- [Runtime requirements](references/runtime-requirements.md)
- [CLI contract](references/cli-contract.md)
- [Troubleshooting](references/troubleshooting.md)
- [social-auto-upload project](https://github.com/dreammis/social-auto-upload)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, PowerShell, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local runtime setup steps, Douyin account names, media file paths, titles, descriptions, tags, scheduling options, and publish-mode flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
