## Description:

Generate a deep, code-first project wiki and VitePress documentation site (DeepWiki-style) for a repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samzong](https://clawhub.ai/user/samzong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to generate a code-first documentation site for an existing repository, including structured Markdown, Mermaid diagrams, VitePress navigation, and evidence metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository source code may be summarized into generated Markdown and codewiki/.meta JSON files.

Mitigation: Run the skill only on repositories whose contents may be documented, and review generated files before sharing or committing them.

Risk: Documentation site setup can install npm packages and optional deployment tooling.

Mitigation: Use a clean branch, pin npm and wrangler versions or add a lockfile, and review dependency changes before use.

Risk: Optional Cloudflare deployment can publish generated documentation using the user's Cloudflare account.

Mitigation: Run the deployment workflow only when publication is intended and account permissions have been verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samzong/skills/codewiki-generator)
- [README](_README.md)
- [Structure and Heuristics](references/structure-and-heuristics.md)
- [Documentation Templates](references/doc-templates.md)
- [Cloudflare Deployment Workflow](references/deploy-cloudflare.md)
- [Internationalization Setup](references/i18n-setup.md)
- [Evidence Rules](references/evidence-rules.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, JSON metadata, VitePress configuration, Mermaid diagrams, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a codewiki/ documentation site, .meta JSON files, a quality report, and optional Cloudflare deployment or i18n guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
