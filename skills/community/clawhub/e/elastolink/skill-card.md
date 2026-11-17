## Description:

Elastolink Meeting Skills helps an agent use Elastolink MCP tools to list meetings, check device status, view meeting details, and export meeting content as Markdown or Office documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netkiller](https://clawhub.ai/user/netkiller)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Elastolink meeting information, inspect meeting details, and export meeting artifacts. It is intended for workflows where an authorized user needs an agent to operate Elastolink meeting tools and present JSON results in a readable form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens and session identifiers are used to access Elastolink meeting data and may be exposed through command output, local files, or logs.

Mitigation: Use a minimally scoped, short-lived token; avoid production credentials; restrict access to the local environment file; and rotate the token after use.

Risk: Meeting detail and export tools may retrieve confidential or personal meeting content.

Mitigation: Run exports only for meetings the user is authorized to access, review storage locations before sharing files, and treat exported Markdown or Office documents as sensitive.

Risk: Token setup writes local configuration and may overwrite an existing Elastolink token file.

Mitigation: Confirm the target environment before saving a token and back up or inspect any existing configuration when preserving prior credentials matters.

## Reference(s):

- [MCP Tools Reference](references/mcp-tools.md)
- [Elastolink MCP endpoint](https://dev.ideasprite.com/mcp)
- [ClawHub skill page](https://clawhub.ai/netkiller/skills/elastolink)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown or plain text summaries of JSON-RPC responses, with shell commands and configuration steps when token setup is required.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exported meeting content or document references returned by the Elastolink service.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
