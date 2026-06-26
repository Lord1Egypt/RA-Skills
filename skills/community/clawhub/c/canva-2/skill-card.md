## Description: <br>
MCP skill for Canva that lets an agent search, read, generate, import, export, organize, and comment on Canva designs through 22 OAuth-backed tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manojbajaj95](https://clawhub.ai/user/manojbajaj95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to Canva so it can find existing designs, inspect design content, create or import new designs, export files, manage folders, and participate in comment threads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OAuth-backed access to a user's Canva account and can read or change Canva content. <br>
Mitigation: Review requested Canva scopes during authorization, use the connector only with accounts where that access is appropriate, and revoke the connector or remove persisted local tokens when no longer needed. <br>
Risk: Some tools can reorder, merge, move, comment on, or delete Canva content. <br>
Mitigation: Require explicit user confirmation before destructive or structural changes, and review the affected design, folder, or comment thread before relying on the result. <br>
Risk: Persisted OAuth tokens may expose Canva access on shared or poorly protected machines. <br>
Mitigation: Avoid shared machines unless token files are protected, and remove the persisted token directory when the connector should no longer retain access. <br>


## Reference(s): <br>
- [Canva skill on ClawHub](https://clawhub.ai/manojbajaj95/canva-2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Files, Configuration guidance] <br>
**Output Format:** [JSON-like MCP tool results with Canva design metadata, content, URLs, comments, folders, generated design candidates, and export download links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OAuth-backed Canva access and may create or modify Canva resources according to the selected tool.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
