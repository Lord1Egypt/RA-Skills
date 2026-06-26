## Description: <br>
Context window optimizer that analyzes, audits, and helps optimize an agent's context utilization before prompts are sent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkuehnl](https://clawhub.ai/user/tkuehnl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze workspace prompts, memory files, tool definitions, and installed skill overhead, then generate context efficiency reports or snapshots for optimization planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports and saved snapshots may reveal sensitive workspace or configuration details such as file paths, token counts, tool names, and prompt-derived context. <br>
Mitigation: Run the skill only on workspaces and configuration files intended for audit, review outputs before sharing, and store snapshots in controlled locations. <br>
Risk: Approximate token estimates may differ from model-specific tokenizer counts and can make recommendations less precise. <br>
Mitigation: Use a model-specific tokenizer for exact budgeting and review recommendations before applying prompt, memory, or configuration changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tkuehnl/context-engineer) <br>
- [Project homepage from skill metadata](https://github.com/cacheforge-ai/cacheforge-skills) <br>
- [Anvil AI](https://anvil-ai.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; terminal reports and optional JSON snapshots from the bundled script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses approximate token estimates and can save comparison snapshots when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and changelog show 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
