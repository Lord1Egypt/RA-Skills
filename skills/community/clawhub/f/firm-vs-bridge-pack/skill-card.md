## Description: <br>
VS Code bridge pack for context push/pull and session linking between VS Code and OpenClaw Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to share VS Code editor context with OpenClaw Gateway, retrieve context back into the agent workflow, and link or check editor sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editor selections, file content, diagnostics, or session details may be shared with OpenClaw Gateway. <br>
Mitigation: Use the skill only in workspaces where that sharing is intended, and avoid pushing secrets or proprietary code unless sharing is approved. <br>
Risk: The skill depends on a connected OpenClaw Gateway, the OpenClaw extension, and the external mcp-openclaw-extensions package. <br>
Mitigation: Install it only when those connected components and packages are trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/romainsantoli-web/firm-vs-bridge-pack) <br>
- [Publisher profile](https://clawhub.ai/user/romainsantoli-web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline tool-call and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve VS Code selections, file content, diagnostics, and session status from the connected OpenClaw Gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
