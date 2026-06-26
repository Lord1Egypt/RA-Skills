## Description: <br>
Turn OpenClaw into a PUA-driven execution workflow that pushes past shallow answers, explores real alternatives, and continues until evidence-backed completion or a hard blocker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LUO-2Q](https://clawhub.ai/user/LUO-2Q) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and other agent users use this skill to make coding, debugging, research, planning, and analysis tasks more persistent, evidence-driven, and bounded by explicit stop conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally encourages stronger task persistence, which can lead to over-extension if the agent ignores safety policies, user confirmations, budgets, or high-impact-task caution. <br>
Mitigation: Treat the skill as a workflow aid only; preserve safety policies, required confirmations, cost limits, and extra care for medical, legal, financial, account-changing, or other high-impact tasks. <br>
Risk: Persistent execution can produce misleading momentum if the agent continues without adequate evidence. <br>
Mitigation: Require the agent to distinguish facts, inferences, and hypotheses, collect evidence from available inputs or tools, and stop when the task is complete, hard-blocked, or further search has low expected value. <br>


## Reference(s): <br>
- [AI Potential Driver Framework](references/framework.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/LUO-2Q/ai-potential-driver) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown or structured text guidance for agent progress and final responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external tools or credentials are declared; output is bounded by the user task, evidence, and explicit stop conditions.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
