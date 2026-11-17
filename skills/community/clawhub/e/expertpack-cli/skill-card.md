## Description:

Run local ExpertPack CLI tools to validate, repair, graph, strip frontmatter from, and prepare ExpertPacks for deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianhearn](https://clawhub.ai/user/brianhearn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run ExpertPack validation, repair, graph export, frontmatter stripping, and deployment preparation commands against local packs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run mutable third-party Python tools without a pinned version or integrity check.

Mitigation: Review or pin the ExpertPack repository to a known commit and verify scripts and copied configuration before use.

Risk: Doctor and fixer commands can modify local pack files.

Mitigation: Run dry-run previews or use a disposable clean working tree first, then inspect diffs before committing changes.

## Reference(s):

- [ExpertPack CLI Commands Reference](references/cli-commands.md)
- [ExpertPack repository](https://github.com/brianhearn/ExpertPack)
- [ExpertPack CLI ClawHub release](https://clawhub.ai/brianhearn/skills/expertpack-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on local files and may produce changed files, validation reports, graph metadata, or deployment copies depending on the selected ExpertPack tool.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
