## Description:

Builds Aicade application prompts by combining a user's base business prompt with the bundled Aicade platform integration workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aicadegalaxy](https://clawhub.ai/user/aicadegalaxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to assemble IDE-ready prompts for Aicade apps, check required Aicade environment variables, and follow the platform scaffold workflow before upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle Aicade upload credentials and save values into a project .env file.

Mitigation: Provide credentials only through local, private workflows; never paste real secrets into chat; verify .env is ignored by Git before saving.

Risk: Credential values or resolved upload variables could be exposed during review or command output.

Mitigation: Do not allow full secret values to be printed, logged, or included in prompts; use redacted values when confirming upload settings.

Risk: The upload workflow may use downloaded upload.js code or changed npm dependencies.

Mitigation: Review upload.js and dependency changes before running npm install or upload commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aicadegalaxy/skills/aicade-create-app-builder)
- [Aicade TypeScript bootstrap repository](https://github.com/aicade-galaxy/aicade-ts-bootstrap)
- [Aicade TypeScript bootstrap README](https://github.com/aicade-galaxy/aicade-ts-bootstrap/blob/main/README.md)
- [Aicade scaffold upload script](https://github.com/aicade-galaxy/aicade-ts-bootstrap/blob/main/upload.js)
- [Aicade Galaxy platform](https://www.aicadegalaxy.com/)
- [Prompt workflow reference](references/prompt-workflow.md)
- [SDK capabilities reference](references/sdk-capabilities.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a project .env file when the user provides Aicade credentials and approves the local workflow.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
