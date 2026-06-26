## Description: <br>
Coordinates multiple Cursor agents through tmux for parallel coding tasks and multi-model technical deliberation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to split independent coding work across multiple Cursor sessions, monitor their progress, and convene model-based reviews for architecture, technology selection, risk assessment, and other complex tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parallel agents may edit code or run commands with reduced approval prompts. <br>
Mitigation: Use disposable workspaces or separate git branches, keep task boundaries file-specific, and review each agent's changes before merging. <br>
Risk: Blindly approving waiting sessions can allow unwanted command execution. <br>
Mitigation: Inspect approvals before responding and avoid automatically sending approval keystrokes unless the command and workspace impact are understood. <br>
Risk: Council prompts and saved transcripts can retain sensitive context. <br>
Mitigation: Avoid secrets or customer data in prompts, and delete or protect saved council transcripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoyaner0201/cursor-council) <br>
- [Parallel Execution Guide](references/parallel-execution.md) <br>
- [Council Deliberation Guide](references/council-deliberation.md) <br>
- [Persona Engineering for AI Council](references/persona-engineering.md) <br>
- [Session README Template](references/session-readme-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and session templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux, the agent CLI, and a configured cursor-agent skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
