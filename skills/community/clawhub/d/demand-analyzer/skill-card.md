## Description: <br>
A 7-part demand analysis framework that prompts an agent to clarify intent, constraints, ambiguity, information gaps, options, and an execution plan before acting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcz-user](https://clawhub.ai/user/zcz-user) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to slow down before responding to user tasks, questions, links, or vague requests and produce a structured clarification-first analysis. It is intended for request triage, option framing, and planning before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can slow routine interactions by making the agent pause, analyze, and ask for confirmation before acting. <br>
Mitigation: Use it for tasks where deliberate request analysis and confirmation are desired, and disable or bypass it for fast routine responses. <br>
Risk: The skill emphasizes Chinese-language structure and may produce tone or language mismatches for some audiences. <br>
Mitigation: Review generated analysis for audience fit and adjust language or tone before using it in user-facing contexts. <br>


## Reference(s): <br>
- [7 部分需求拆解框架](artifact/references/framework.md) <br>
- [ClawHub skill page](https://clawhub.ai/zcz-user/demand-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown with structured headings, lists, and option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language framework structure; may ask clarifying questions before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
