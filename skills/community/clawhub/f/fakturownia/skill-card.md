## Description:

Fakturownia CLI helps agents use the `fakturownia` command for authentication, schema discovery, diagnostics, and Fakturownia account, invoicing, payment, product, warehouse, webhook, and recipe workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sixers](https://clawhub.ai/user/sixers)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide an agent through authenticated Fakturownia CLI workflows, including account checks, invoice and payment operations, schema lookup, diagnostics, and generated invoice recipes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through broad Fakturownia account, invoicing, credential, webhook, and destructive business operations.

Mitigation: Use a least-privilege token, verify the resolved profile and destination host before API calls, and require manual approval before delete, cancel, email, KSeF, webhook, self-update, or attachment-visibility actions.

Risk: Raw output and direct command arguments may expose secrets or sensitive business data in stdout, shell history, or logs.

Mitigation: Avoid `--raw` unless stdout and logs are protected, and avoid putting passwords or tokens directly in command arguments.

Risk: An agent could operate against the wrong account or host if credentials or profile selection are unclear.

Mitigation: Run `fakturownia auth status --json` to confirm profile, prefix, and token source, then use `fakturownia account get --json` as an authenticated smoke test before task-specific reads or writes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sixers/skills/fakturownia)
- [Skills Index](references/skills-index.md)
- [Recipes Index](recipes/index.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples and JSON payload snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the `fakturownia` binary and authenticated profile or environment token before live API operations.]

## Skill Version(s):

0.6.7 (source: server release evidence and CHANGELOG, released 2026-04-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
