## Description: <br>
Evaluates a PA agent's tasks, skills, network health, integrations, memory quality, and supervisor performance into a structured report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
PA owners and operators use this skill to run on-demand or scheduled evaluations of task execution, integrations, memory hygiene, and PA network health. The skill produces scores, status checks, and prioritized recommendations for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads sensitive workspace data, sources local context, and uses stored credentials. <br>
Mitigation: Review the local context file and credential paths before use, narrow what data the eval may inspect, and require confirmation before credentialed API checks. <br>
Risk: The skill can create ongoing feedback logs and weekly saved evaluation files without explicit retention controls. <br>
Mitigation: Make feedback logging and saved eval files opt-in, and define clear retention and deletion rules before deployment. <br>
Risk: Broad trigger phrases can cause evaluation to run when the user did not intend a full inspection. <br>
Mitigation: Constrain trigger phrases to explicit eval requests and confirm before running broad workspace or service health checks. <br>


## Reference(s): <br>
- [Eval skill listing](https://clawhub.ai/netanel-abergel/eval) <br>
- [Anthropic Models API](https://api.anthropic.com/v1/models) <br>
- [monday.com API v2](https://api.monday.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with scoring tables, status summaries, shell command snippets, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local workspace files, source local context, call external APIs with stored credentials, and write weekly evaluation files.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
