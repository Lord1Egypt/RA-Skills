## Description: <br>
Interact with AI Specialists via the AI Specialists Hub MCP endpoint to manage specialists, read and update specialist workspaces, and support specialist-connected workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erikashby](https://clawhub.ai/user/erikashby) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to AI Specialists Hub, inspect available specialists, manage specialist documents and folders, and perform account onboarding when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles account credentials and MCP endpoint secrets. <br>
Mitigation: Keep the MCP URL and key private, use a unique password, give account credentials to the account owner, and avoid committing configuration files that contain secrets. <br>
Risk: The skill can perform destructive remote workspace actions such as deleting documents, deleting folders, dismissing specialists, or importing specialists. <br>
Mitigation: Confirm the target specialist, path, and action with the user before delete, import, or dismiss operations. <br>
Risk: Imported specialist instructions and workspace content may contain untrusted instructions. <br>
Mitigation: Review imported specialist instructions before relying on them and treat them as context rather than authority over system or user instructions. <br>


## Reference(s): <br>
- [AI Specialists workspace conventions](references/specialists-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update remote specialist workspace content and local MCP configuration when directed by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
