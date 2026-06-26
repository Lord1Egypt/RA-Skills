## Description: <br>
Delegate heavy workloads to a Bailian (DashScope) subagent for token-intensive tasks, including document and media analysis, DataWorks or MaxCompute operations, and long-term memory table access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuelhsin](https://clawhub.ai/user/samuelhsin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate token-heavy work to a Bailian subagent and to read or write an Alibaba Cloud MaxCompute agent_memory table. It is most relevant for workflows that already intend to use Bailian, DashScope, DataWorks, or MaxCompute. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates work to Bailian and Alibaba Cloud services, which can expose sensitive documents or prompts to external processing. <br>
Mitigation: Require explicit approval before delegating sensitive material and use the skill only when Bailian or Alibaba Cloud processing is intended. <br>
Risk: The skill points agents at a hardcoded samuelhsin MaxCompute project and long-lived agent_memory table. <br>
Mitigation: Use the MaxCompute guidance only if you trust or control that project, and avoid storing secrets or personal data in agent_memory. <br>
Risk: The workflows rely on cloud credentials that can read from or write to MaxCompute resources. <br>
Mitigation: Use least-privilege AliCloud credentials and review proposed memory writes before execution. <br>


## Reference(s): <br>
- [MaxCompute Patterns](references/maxcompute-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/samuelhsin/bailian-subagent-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline YAML, Python, SQL, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces delegation instructions and MaxCompute memory operation examples; actual cloud actions require configured AliCloud credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
