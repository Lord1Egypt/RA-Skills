## Description: <br>
Figma integration for browsing team projects and files, reading design structure, pages, and nodes, exporting images, managing comments, viewing version history, inspecting components, component sets, styles, and retrieving design variables through MorphixAI-mediated Figma API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and design-system maintainers use this skill to inspect Figma files, export design assets, review comments and versions, and retrieve components, styles, and design tokens through linked Figma access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on MorphixAI and a linked Figma account, which can expose workspace data through authorized API access. <br>
Mitigation: Install only when MorphixAI is trusted, store MORPHIXAI_API_KEY as a secret, and link the least-privileged Figma account or workspace access available. <br>
Risk: Comment actions can post, reply to, or delete comments in shared Figma files. <br>
Mitigation: Require explicit approval before comment-changing actions and review the target file, comment, and message before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/paul-leo/figma-2) <br>
- [Publisher Profile](https://clawhub.ai/user/paul-leo) <br>
- [MorphixAI API Keys](https://morphix.app/api-keys) <br>
- [MorphixAI Connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown, text] <br>
**Output Format:** [Markdown with tool-call examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Figma account for live Figma access.] <br>

## Skill Version(s): <br>
0.1.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
