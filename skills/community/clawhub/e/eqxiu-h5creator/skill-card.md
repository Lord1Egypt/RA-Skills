## Description:

易企秀H5制作 helps agents create, preview, edit, and update Eqxiu AIGC H5 pages from a user's natural-language request through the bundled CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eqxiu](https://clawhub.ai/user/eqxiu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to automate Eqxiu AIGC H5 creation from event or page requirements, then return preview and edit links. The skill can also support follow-up text edits, body image replacement, material listing, and local material upload for an Eqxiu account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files to remote Eqxiu material services.

Mitigation: Approve the exact local file before running upload commands and avoid uploading sensitive or unintended files.

Risk: A saved Eqxiu token can be sent to configurable network endpoints.

Mitigation: Keep commands on the default Eqxiu service hosts, avoid untrusted endpoint or environment overrides, and remove or rotate the saved token when no longer needed.

## Reference(s):

- [Eqxiu AIGC HTTP API Reference](references/http-api.md)
- [Recommended Conversation Workflow](references/workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/eqxiu/skills/eqxiu-h5creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Create operations return previewUrl and editUrl; follow-up commands can update text, replace body images, list materials, or upload local files.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
