## Description:

Agent Cluster coordinates ecommerce, ERP, CMS, inventory, procurement, finance, logistics, and model execution workflows through a multi-agent system for B2B foreign-trade operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure and run coordinated agents for B2B ecommerce, CMS publishing, ERP integration, inventory checks, procurement workflows, finance review, logistics tracking, and execution-engine routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the package bundles a broader ERP, CMS, and agent system than advertised.

Mitigation: Review scope before installation and confirm that the bundled ERP, CMS, Amazon, and model integrations are intended for the deployment.

Risk: Unsafe CMS execution paths may make live changes or upload local files under weak controls.

Mitigation: Use an isolated test environment until preview handling, approval timeouts, upload paths, and audit logging are fixed and verified.

Risk: Real ERP, CMS, Amazon, or model API credentials could be exposed or misused during evaluation.

Mitigation: Grant only narrowly scoped test credentials and do not provide production credentials until the security issues identified by clawscan are resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangm-a3/skills/agent-cluster)
- [ClawDIS homepage](https://github.com/WangM-A3/agent-cluster)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, YAML or JSON-style configuration, and workflow descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mermaid diagrams, API examples, task plans, approval records, audit guidance, and generated or modified project files.]

## Skill Version(s):

3.0.4 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
