## Description: <br>
Decompose complex user tasks into multi-step workflows using DAG-based execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keweizhan](https://clawhub.ai/user/keweizhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to break natural-language requests into dependency-aware task graphs, schedule independent work in parallel, and return structured execution results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OpenAI API key and sends task descriptions to OpenAI for decomposition. <br>
Mitigation: Use an appropriate API key handling process, avoid submitting secrets in task descriptions, and install only when external API processing is acceptable. <br>
Risk: Generated task graphs may not match the intended workflow or may contain unsafe follow-on steps. <br>
Mitigation: Review generated task graphs before execution and confirm dependencies, task wording, and expected outputs. <br>
Risk: Extending the placeholder tool registry to real tools can introduce file, account, production system, or public-content modification risk. <br>
Mitigation: Gate real tool integrations with least privilege, human approval for sensitive actions, and focused tests before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/keweizhan/agent-workflow-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/keweizhan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text and JSON-like task execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task lists, dependency graphs, execution status, and generated commands or configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
