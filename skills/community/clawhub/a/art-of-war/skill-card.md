## Description: <br>
Apply Sun Tzu's Art of War principles to AI agent organization and task orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanikua](https://clawhub.ai/user/wanikua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide whether to deploy agents, plan multi-agent workflows, manage token and tool costs, and validate outputs during task orchestration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tool-heavy orchestration guidance can lead agents toward search, API calls, code execution, monitoring, or multi-agent runs without enough control. <br>
Mitigation: Keep user approval, token budgets, timeouts, and review gates around those actions, and review outputs before acting on them. <br>
Risk: The artifact README references a helper script that is not present in the reviewed files. <br>
Mitigation: Rely on the reviewed package files and the available assess-task.py script rather than unmatched README helper references. <br>


## Reference(s): <br>
- [The Thirteen Chapters - Detailed Agent Mappings](references/thirteen-chapters.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wanikua/art-of-war) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with checklists, decision trees, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes planning heuristics and an optional interactive task-assessment script.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
