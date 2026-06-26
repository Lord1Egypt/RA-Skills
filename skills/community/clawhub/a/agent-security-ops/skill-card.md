## Description: <br>
Stop leaking secrets with pre-commit hooks, repo security scans, and cron-friendly monitoring for agent-assisted development workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheAgentWire](https://clawhub.ai/user/TheAgentWire) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and small engineering teams use this skill to add local secret-scanning guardrails, security scan reports, and scheduled monitoring to repositories touched by AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default scans may inspect sensitive host locations outside the selected repository. <br>
Mitigation: Run it only when a broad local security audit is intended, and review what host areas are included before sharing results. <br>
Risk: Scan reports and .security-ops state can contain secret matches, local service details, SSH file paths, and repository metadata. <br>
Mitigation: Treat reports and generated state as sensitive, keep them out of version control, and redact findings before sending them to others. <br>
Risk: The --fix-ssh option changes permissions under ~/.ssh. <br>
Mitigation: Use --fix-ssh only when intentionally authorizing SSH permission changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TheAgentWire/agent-security-ops) <br>
- [The Agent Wire](https://theagentwire.ai) <br>
- [Secret Patterns Reference](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local security findings and monitoring state that may contain sensitive paths, service details, repository metadata, or matched secret material.] <br>

## Skill Version(s): <br>
1.2.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
