## Description: <br>
Agent Harness is a workflow framework that helps an agent choose a planning, research, analysis, context-compression, or multi-agent coordination path before executing a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neltharion11](https://clawhub.ai/user/neltharion11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to structure multi-step work such as research reports, competitive analysis, task decomposition, context compression, and sub-agent coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate broadly for common planning, research, review, and analysis prompts. <br>
Mitigation: Use it only when the user intentionally wants this workflow framework, and confirm task fit before applying its multi-step process. <br>
Risk: The skill can spawn sub-agents for decomposed work. <br>
Mitigation: Require explicit confirmation before starting sub-agents, especially for sensitive tasks or work involving private data. <br>
Risk: The skill can save full sub-agent outputs under subagent_reports without clear retention guidance. <br>
Mitigation: Tell the user before saving reports, disclose the file path, and review or delete created files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/neltharion11/agent-harness) <br>
- [Decision Tree](references/01-DECISION.md) <br>
- [Execution Framework](references/02-PIPELINE.md) <br>
- [Research Workflow](references/03-WORKFLOWS/research.md) <br>
- [Subagent Workflow](references/03-WORKFLOWS/subagent.md) <br>
- [Analysis Workflow](references/03-WORKFLOWS/analysis.md) <br>
- [Context Workflow](references/03-WORKFLOWS/context.md) <br>
- [Quality Checklist](references/05-QUALITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, checklists, structured reports, task plans, and file-path notices for saved sub-agent outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to spawn sub-agents and save full sub-agent reports under subagent_reports.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
