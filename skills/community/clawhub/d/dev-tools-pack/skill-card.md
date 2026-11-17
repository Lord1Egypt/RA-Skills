## Description:

Dev Tools Pack provides Bash-based generators for Chrome extension templates, GitHub READMEs, SaaS landing pages, tech blog posts, tweet threads, and sample code-review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to scaffold common developer-facing artifacts and draft lightweight review or report content from Bash commands. Generated files and review output should be inspected before opening, deploying, publishing, or relying on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File generators can create or overwrite project files and can place user-provided names or descriptions into generated HTML, manifests, and Markdown.

Mitigation: Run the generators only in a disposable or empty directory and review generated files before opening, deploying, or publishing them.

Risk: The code-review command can produce misleading sample findings rather than dependable security or release guidance.

Mitigation: Do not rely on its output for security or merge decisions; perform real code review, testing, and security scanning separately.

Risk: Generated landing pages and extension templates may include CDN scripts, extension manifests, or placeholder code that are not ready for production.

Mitigation: Review generated HTML, extension manifests, CDN usage, and placeholder logic before packaging or deploying the generated project.

## Reference(s):

- [Dev Tools Pack on ClawHub](https://clawhub.ai/sunshine-del-ux/skills/dev-tools-pack)
- [Artifact skill description](artifact/SKILL.md)
- [Artifact metadata](artifact/_meta.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, shell output, and generated file trees]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generator scripts may create project directories or overwrite files such as README.md; generated artifacts require user review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
