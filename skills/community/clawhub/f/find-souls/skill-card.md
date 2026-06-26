## Description: <br>
Search and install AI persona prompts from the Agent Souls library for historical figures, fictional characters, and expert personas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wklken](https://clawhub.ai/user/wklken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to browse persona prompts, install a selected SOUL.md into a project, and roll back to a previous persona when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded persona prompts can shape future agent behavior. <br>
Mitigation: Confirm the selected persona, review the downloaded SOUL.md when the session matters, and reset the conversation only after installing intentionally. <br>
Risk: Installing a soul overwrites SOUL.md in the current project. <br>
Mitigation: Use the built-in confirmation, backup, and rollback flow, and keep .soul_backups/ until rollback is no longer needed. <br>
Risk: The skill fetches search results and persona files from agent-souls.com. <br>
Mitigation: Use the documented source URLs, refresh cached search data when results seem stale, and inspect downloaded content before use in sensitive projects. <br>


## Reference(s): <br>
- [Find Souls on ClawHub](https://clawhub.ai/wklken/find-souls) <br>
- [Agent Souls](https://agent-souls.com/) <br>
- [Agent Souls Search Index](https://agent-souls.com/search.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with numbered choices, URLs, and file-operation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download persona prompt content, update SOUL.md, and maintain .soul_backups/ for rollback.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
