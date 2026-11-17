## Description:

Private-to-public repo sync that copies everything except ai/ to the public mirror, creates and merges a PR, and syncs releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to publish a private repository's sanitized contents to a public GitHub mirror, then sync release notes and package publication state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate or create a public GitHub repository, merge pull requests, delete remote branches, and create or update releases.

Mitigation: Run it only against an explicit allowlisted public repository after reviewing pending changes, and require manual approval or a dry run before merge and branch cleanup.

Risk: The skill can publish npm packages using local credentials.

Mitigation: Require explicit opt-in before npm publishing and verify package names, versions, registry target, and credentials before execution.

Risk: Private material could be exposed if exclusion rules miss sensitive files.

Mitigation: Run secret scanning and an allowlist review before public commits, and keep private-only paths explicitly excluded.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/deploy-public)
- [AI DevOps Toolbox homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git, GitHub CLI, bash, and appropriate repository and package publishing credentials.]

## Skill Version(s):

1.9.72 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
