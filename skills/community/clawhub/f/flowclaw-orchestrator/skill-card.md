## Description:

YAML-driven workflow orchestrator for AI agent teams with human-in-the-loop approval gates. Includes optional Notion, n8n, and Discord integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanhuelsing](https://clawhub.ai/user/vanhuelsing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Flowclaw to define and run multi-step OpenClaw agent workflows from YAML, with optional Notion-triggered n8n automation and Discord notifications. It is suited to workflow execution where human approval gates are needed before sensitive steps continue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executor API key can authorize workflow execution and approvals.

Mitigation: Generate a strong WORKFLOW_EXECUTOR_API_KEY, keep the service on loopback or behind strong authentication, and treat the key as an approval-capable credential.

Risk: Approval and production-deployment controls may be weaker than the user-facing description implies.

Mitigation: Review workflows before installation and do not enable fastlane production deployment until approval or pre-approval checks are enforced server-side.

Risk: Dashboard or metrics exposure could reveal operational details if made network-accessible.

Mitigation: Keep dashboard and metrics endpoints local, or add authentication before exposing them beyond loopback.

Risk: Unpinned production dependencies may change behavior over time.

Mitigation: Pin Python dependencies before production deployment and retest the security and validation suite after upgrades.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vanhuelsing/skills/flowclaw-orchestrator)
- [README](README.md)
- [Security Policy](SECURITY.md)
- [Integration Steps](docs/INTEGRATION-STEPS.md)
- [n8n Integration Guide](docs/n8n-integration-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, JSON, environment variable, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow orchestration guidance and configuration for a local executor; runtime behavior depends on configured OpenClaw agents and optional Notion, n8n, and Discord services.]

## Skill Version(s):

1.1.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
