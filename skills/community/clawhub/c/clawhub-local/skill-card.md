## Description:

Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage ClawHub skills through the ClawHub CLI, including search, install, update, list, authentication, and publish workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forced or non-interactive bulk updates can overwrite local skill state or introduce unintended versions.

Mitigation: Verify the target directory, registry, and intended version before using `update --all`, `--force`, or `--no-input`; prefer pinned versions in controlled environments.

Risk: Publishing commands can upload unintended skill files or metadata.

Mitigation: Review the skill folder, slug, version, changelog, and files to be uploaded before running `clawhub publish`.

Risk: CLI-based skill management gives an agent meaningful write access to local skill directories.

Mitigation: Run without elevated privileges and install only when the ClawHub CLI source and registry are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andy27725/skills/clawhub-local)
- [ClawHub registry](https://clawhub.com)
- [Publisher profile](https://clawhub.ai/user/andy27725)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the npm-installed clawhub CLI; commands can modify local skill files or publish skill content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
