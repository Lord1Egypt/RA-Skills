## Description: <br>
Main orchestration skill for a Python/finance app team with full-stack web capability that routes tasks to sub-agents Simons, Carmen, and Ada. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camilla-oclm](https://clawhub.ai/user/camilla-oclm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to coordinate multi-agent work for Python, finance, and full-stack web application tasks. It helps route work to role-specific sub-agents, choose orchestration paths, and synthesize responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on local AGENTS.md, MEMORY.md, and referenced skills/orchestrate/ref_*.md files that are not included in the artifact. <br>
Mitigation: Confirm those local files are present, current, and trusted before installing or using the skill. <br>
Risk: The skill may route work to external model providers through sub-agent delegation. <br>
Mitigation: Avoid providing credentials, sensitive financial data, or proprietary code unless the configured provider and delegation path are approved for that data. <br>
Risk: Finance-related guidance or generated outputs may be incorrect or incomplete. <br>
Mitigation: Review sub-agent outputs before acting on them, especially when they affect financial decisions, code changes, or user-facing behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/camilla-oclm/finclaws) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with task routing, synthesized guidance, and code or shell command suggestions when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only orchestration output; no executable install behavior is reported in security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
