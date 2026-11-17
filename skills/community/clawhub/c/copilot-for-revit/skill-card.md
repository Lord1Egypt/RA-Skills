## Description:

Allows OpenClaw agents to detect Revit-related requests, check Revit status, list available tools, and execute Revit commands through an openclaw-bridge connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanchan720](https://clawhub.ai/user/ryanchan720)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, BIM users, and external OpenClaw users can use this skill to operate Autodesk Revit from chat workflows, including checking status, inspecting available commands, querying model elements, creating annotations, generating sheets, and changing model parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute commands that modify Revit projects, including writes and deletes.

Mitigation: Enable command confirmation for writes and deletes, and test first on backup or non-production Revit models.

Risk: The Revit bridge connection may expose broad project-modifying authority over a plaintext or insufficiently controlled network path.

Mitigation: Restrict the Revit service to localhost, VPN, or another authenticated channel.

Risk: The local bridge code is an external dependency that must be trusted before agent execution.

Mitigation: Use only trusted bridge code pinned to a known commit and review the installation before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryanchan720/skills/copilot-for-revit)
- [Copilot for Revit](https://github.com/ryanchan720/copilot-for-revit)
- [Copilot for Revit Quickstart](https://github.com/ryanchan720/copilot-for-revit/blob/main/QUICKSTART.md)
- [openclaw-bridge](https://github.com/ryanchan720/openclaw-bridge)
- [General Copilot Addins for Revit](https://github.com/ryanchan720/general-copilot-addins-for-revit)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell snippets and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses REVIT_MCP_URL and OPENCLAW_BRIDGE_DIR configuration to call Revit bridge commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
