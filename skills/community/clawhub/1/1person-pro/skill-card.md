## Description: <br>
Your personal AI assistant platform - multi-agent orchestration, task management, and autonomous workflow execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiyanhui](https://clawhub.ai/user/shiyanhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to connect an agent to 1Person Pro for multi-agent orchestration, task management, delegated execution, reusable workflows, and persistent task context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 1Person Pro API key, which gives the agent access to the connected 1Person Pro service. <br>
Mitigation: Store ONEPERSON_API_KEY in a managed secret or environment setting, limit access to trusted agents, and rotate or revoke the key if exposure is suspected. <br>
Risk: Delegated workflows and persistent memory can retain context or act on tasks beyond a single prompt. <br>
Mitigation: Review 1Person Pro approval, data retention, and context deletion controls before using the skill with sensitive or regulated information. <br>


## Reference(s): <br>
- [1Person Pro homepage](https://1person.pro) <br>
- [1Person Pro documentation](https://docs.1person.pro) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ONEPERSON_API_KEY for service access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
