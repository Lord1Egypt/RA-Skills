## Description:

Content Template helps agents create, render, compare, and polish content templates using Jinja2 variables, conditions, loops, inheritance, simple A/B comparisons, and a content category catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to manage reusable content templates, render localized or personalized copy, compare template variants, polish marketing copy, and inspect supported content generation categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored Jinja2 templates are rendered with unsandboxed Python capabilities.

Mitigation: Install and run only trusted templates, review template changes before deployment, and avoid accepting unreviewed template content from users.

Risk: Generation and polishing actions can send brand profiles, persona data, style fingerprints, knowledge-base excerpts, and content guidelines through configured LLM providers.

Mitigation: Do not pass confidential business context unless tenant policy permits those providers and the data has been approved for external processing.

Risk: The skill imports local shared OpenClaw modules and can write template JSON files into the local content template store.

Mitigation: Install only in trusted OpenClaw environments and review file-write behavior, permissions, and backups before using it in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/content-template)
- [Business rules](artifact/references/business_rules.md)
- [Error codes](artifact/references/error_codes.md)
- [Examples](artifact/references/examples.md)
- [Content template reference](artifact/scripts/content_template_reference.json)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON responses containing rendered or generated content, plus Markdown guidance and inline shell-command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local template JSON files and may use configured LLM providers when generation or polishing actions are invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
