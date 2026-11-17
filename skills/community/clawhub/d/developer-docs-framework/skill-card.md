## Description:

Developer Docs Framework helps agents write, plan, audit, and improve technical documentation using Diataxis, Google OpenDocs, Good Docs Project templates, style guides, and enterprise documentation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anivar](https://clawhub.ai/user/anivar)

### License/Terms of Use:

MIT

## Use Case:

Developers, technical writers, and documentation teams use this skill to create or review developer and partner documentation, including tutorials, how-to guides, API references, migration guides, runbooks, and documentation strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad documentation triggers can cause the skill to influence many documentation-writing tasks.

Mitigation: Review whether the trigger breadth matches the intended agent context before deployment.

Risk: Credential examples and Stripe-style personalization guidance can normalize test-key handling if copied without controls.

Mitigation: Use masked, scoped, non-production credentials in examples and require platform controls before personalized keys are shown.

Risk: Generated documentation can be structurally sound while still being inaccurate or stale.

Mitigation: Pair the skill output with product or API source review, runnable code-example tests, and a documented freshness cadence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anivar/skills/developer-docs-framework)
- [Metadata source URL](https://github.com/anivar/developer-docs-framework)
- [Publisher profile](https://clawhub.ai/user/anivar)
- [Diataxis](https://diataxis.fr/)
- [Google OpenDocs](https://github.com/google/opendocs)
- [Good Docs Project](https://www.thegooddocsproject.dev/)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Content types reference](references/content-types.md)
- [Templates reference](references/templates.md)
- [Enterprise patterns reference](references/enterprise-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with examples, checklists, templates, and occasional code or shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces documentation guidance only; it does not declare tools, MCP servers, credential environment variables, or hidden execution behavior.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter metadata version is 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
