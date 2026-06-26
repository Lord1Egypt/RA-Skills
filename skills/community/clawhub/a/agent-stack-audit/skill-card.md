## Description: <br>
Agent Stack Audit helps agents audit automation stacks for inactive scheduled jobs, dead scripts, unused API keys, superseded skills, stale memory files, and tool subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pingukim225](https://clawhub.ai/user/pingukim225) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review an agent automation stack, rank cleanup candidates, and prepare approval-driven maintenance actions before changing files or subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to inspect sensitive local and account data, including automation directories, scheduled tasks, logs, API or subscription inventory, installed skills, and memory files. <br>
Mitigation: Define exact paths and accounts in scope before running the audit, require secret redaction in outputs, and avoid sharing generated reports until sensitive values are removed. <br>
Risk: Cleanup recommendations or script edits can disrupt active automation if they are applied without clear approval boundaries. <br>
Mitigation: Treat findings as recommendations, require an explicit reviewed diff and rollback plan before any change, and approve each cleanup action separately. <br>


## Reference(s): <br>
- [Agent Stack Audit on ClawHub](https://clawhub.ai/pingukim225/agent-stack-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit brief with tables and approval-oriented recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated audit reports such as state/stack_audit_YYYY-MM-DD.md when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
