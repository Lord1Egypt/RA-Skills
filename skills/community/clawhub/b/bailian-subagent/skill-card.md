## Description: <br>
Spawn a bailian (百炼 DashScope) subagent to handle token-heavy or compute-intensive tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuelhsin](https://clawhub.ai/user/samuelhsin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to delegate large, repetitive, or token-heavy work to a Bailian subagent, including data processing, code generation, document analysis, news fetching, and DataWorks or MaxCompute SQL tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells users to pass cloud credentials, production-like DataWorks details, and potentially privileged SQL authority into a fresh subagent prompt. <br>
Mitigation: Avoid pasting long-lived Alibaba Cloud keys or privileged production access into prompts; use short-lived, least-privilege, runtime-bound secret handling and narrow when sensitive cloud work may be delegated. <br>
Risk: Delegated DataWorks or MaxCompute tasks may include destructive or state-changing SQL operations. <br>
Mitigation: Review generated SQL and subagent outputs before execution, especially for DROP, CREATE, INSERT, or other operations that affect production data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces subagent tasking guidance and example invocation patterns; delegated work should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
