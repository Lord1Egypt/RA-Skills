## Description: <br>
DevLoop Agent Pack coordinates six specialized agents across product discovery, architecture design, parallel implementation, testing, research, and marketing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weitanai](https://clawhub.ai/user/weitanai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to run a product-driven development loop with dedicated agents for PRD creation, architecture planning, implementation, testing, market research, and launch support. It is intended for teams that want structured agent collaboration, durable project notes, and repeatable handoffs across the software delivery lifecycle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can write durable project notes, reports, and memory files that may persist sensitive or incorrect information. <br>
Mitigation: Review SOUL.override.md, USER.md, MEMORY.md, memory files, and generated reports before reuse; keep secrets and private data out of persistent memory. <br>
Risk: Agents may run build, test, git, and shell commands or prepare commits and pushes as part of development work. <br>
Mitigation: Use the skill only in repositories where this level of agent action is acceptable, and review planned git actions before they are executed. <br>
Risk: Web research and multi-agent handoffs can introduce stale, misleading, or low-quality guidance into product, research, or marketing artifacts. <br>
Mitigation: Validate research findings and review cross-agent outputs before treating them as product, engineering, or launch decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weitanai/devloop-agent-pack) <br>
- [DevLoop workflow overview](skills/devloop-workflow/SKILL.md) <br>
- [Collaboration protocol](skills/devloop-workflow/references/collaboration-protocol.md) <br>
- [Agent design background](skills/devloop-workflow/references/agent-design-background.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, development artifacts, shell commands, code changes, configuration notes, and persistent project memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include durable notes, reports, test specifications, design documents, bug trackers, commit plans, and agent handoff messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and plugin metadata list 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
