## Description: <br>
Helps an agent break complex tasks into sequential reasoning steps with support for revision, branch exploration, and hypothesis validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paibwhgs](https://clawhub.ai/user/paibwhgs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent developers and operators use this skill to structure complex tasks into sequential thoughts, revisions, branches, and hypotheses. It is useful when planning multi-step work, comparing solution paths, or maintaining context across a complex task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reasoning notes may contain secrets, private data, confidential business details, or regulated legal, medical, or financial information if saved locally. <br>
Mitigation: Use explicit invocation for sensitive work and avoid saving local thinking logs unless storage and deletion practices are understood. <br>
Risk: Always-on use can shift agent behavior toward unnecessary planning overhead or expose more intermediate reasoning than intended. <br>
Mitigation: Install and invoke it as a reasoning helper for complex tasks rather than as a blanket behavior change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paibwhgs/agent-sequential-thinking) <br>
- [Publisher profile](https://clawhub.ai/user/paibwhgs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured reasoning notes, with optional JSON-style thought records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to record thinking notes in local Markdown files when configured to do so.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
