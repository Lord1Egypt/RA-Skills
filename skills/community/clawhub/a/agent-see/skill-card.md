## Description:

Convert any website, SaaS product, or API into a live, discoverable, agent-executable integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert websites, SaaS products, or OpenAPI specifications into agent-ready bundles, then guide deployment, discovery publishing, backend connection, packaging, and maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to fetch code from GitHub and modify the local Python/browser environment.

Mitigation: Use an isolated project or container, pin and review the Agent-See repository before installation, and avoid system-level package overrides.

Risk: The skill includes deployment, public discovery publishing, and production-like testing workflows.

Mitigation: Require explicit confirmation before deployment, public publishing, production testing, or any state-changing backend action.

Risk: Backend connection workflows may involve API, database, or e-commerce credentials.

Mitigation: Keep secrets in platform secret stores, prefer staging environments for tests, and review authentication mappings before connecting real services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielfoojunwei/skills/agent-see)
- [Source repository from skill metadata](https://github.com/Danielfoojunwei/Convert-any-SaaS-application-into-an-Agentic-interface)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and generated file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through conversion, verification, deployment, discovery publishing, backend wiring, packaging, and maintenance workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
