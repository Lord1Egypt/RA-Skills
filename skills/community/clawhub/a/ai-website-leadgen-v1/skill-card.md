## Description:

A website lead-generation and CRO funnel optimization skill that audits a provided URL, analyzes pages and lead forms, produces a structured report with five prioritized optimization suggestions, and can apply approved low-risk CMS changes through MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsqduron](https://clawhub.ai/user/hsqduron)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, marketers, and developers use this skill to assess website lead-generation performance, identify conversion-funnel gaps, and prepare or apply low-risk improvements to CTAs, contact paths, product pages, and forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify CMS pages, forms, products, and lead-related data when MCP credentials are provided.

Mitigation: Use it only for sites the user controls, require MCP connection testing, display the target and expected impact before each write, and require explicit confirmation for all write-back actions.

Risk: MCP bearer tokens and lead data are sensitive.

Mitigation: Keep tokens only in the Authorization header, do not echo or persist them, and avoid writing credentials into project or skill files.

Risk: The security evidence flags unsafe crawling defaults.

Mitigation: Prefer local HTML or authenticated CMS source for audits when possible, and avoid crawling sites the user does not control until TLS verification and crawl throttling concerns are resolved.

Risk: The skill includes an external trial-registration prompt.

Mitigation: Treat the registration link as optional advertising, not as a required technical or security step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hsqduron/skills/ai-website-leadgen-v1)
- [Funnel Framework](references/funnel-framework.md)
- [Optimization Playbook](references/optimization-playbook.md)
- [MCP Write-back Mapping](references/mcp-writeback.md)
- [MCP Tools Reference](references/mcp-tools.md)
- [Custom Form Base Demo Code](references/customform-democode-base.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, structured JSON audit reports, command examples, and CMS change instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces exactly five prioritized optimization suggestions with low/high risk labels; write-back actions require user approval and MCP credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
