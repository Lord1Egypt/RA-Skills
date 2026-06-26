## Description: <br>
Manage Canva designs, assets, and folders via the Connect API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolmanns](https://clawhub.ai/user/coolmanns) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content operations teams use this skill to automate Canva design management, exports, asset uploads, folder organization, and brand-template autofill from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores refreshable Canva OAuth tokens locally. <br>
Mitigation: Use a dedicated Canva profile when practical, protect the local token file, and revoke Canva access when the skill is no longer needed. <br>
Risk: The skill can perform user-directed write-like or destructive Canva actions such as upload, delete, export, comment, and folder operations. <br>
Mitigation: Review requested commands, OAuth scopes, and target resource IDs before execution, and require explicit confirmation for delete, upload, export, or comment operations. <br>


## Reference(s): <br>
- [Canva Connect documentation](https://canva.dev/docs/connect/) <br>
- [Canva Connect API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/coolmanns/canva-connect) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Canva OAuth credentials and local token state; command results may include JSON from the Canva Connect API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
