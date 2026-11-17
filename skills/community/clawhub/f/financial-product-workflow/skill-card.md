## Description:

Helps financial product managers build an AI-assisted workflow for strategy, requirements analysis, product design, technical review, development follow-up, testing, launch, and operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

Financial product managers and product teams use this skill to plan, design, review, deliver, test, and operate financial products from 0 to 1 or through iteration. It provides structured prompts, compliance checklists, self-operation design guidance, and optional handoffs to work tools such as Jira and Confluence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes an unverified remote shell installer path.

Mitigation: Prefer direct prompt-template usage, or inspect and verify any installer before running it.

Risk: Configured integrations may create, update, post, query, or send content in external work systems.

Mitigation: Use least-privilege tokens, keep sensitive financial or customer data out of generated work items unless approved, and require explicit confirmation before external actions.

Risk: Financial product workflow outputs may be mistaken for final compliance approval.

Mitigation: Treat the built-in checklists as drafting aids and route product, marketing, data, and launch decisions through licensed compliance personnel.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lj22503/skills/financial-product-workflow)
- [Publisher Profile](https://clawhub.ai/user/lj22503)
- [Compliance Checklist](references/compliance-checklist.md)
- [STAR+ Compliance Framework](references/star-framework.md)
- [Self-Operation Design Guide](references/self-operation-design.md)
- [Tool Integration Guide](references/tool-integration.md)
- [MBTI Mapping Reference](references/mbti-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, tables, checklists, Mermaid diagrams, prompt templates, shell snippets, configuration guidance, and external-tool links when integrations are configured.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fallback output is Markdown or plain text when external tools are not configured.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
