## Description:

Compare manifest XML files via Gerrit and Gitiles APIs and produce JSON, text, or Excel reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[craftslab](https://clawhub.ai/user/craftslab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to compare Android or repo manifest versions and generate change reports from Gerrit and Gitiles metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration can include Gerrit or Gitiles usernames, passwords, or API tokens.

Mitigation: Use least-privilege API tokens, keep populated config files permission-restricted, and avoid committing or sharing secrets.

Risk: The installation guidance uses an unpinned pip install for the diffmanifests package.

Mitigation: Install in an isolated environment and pin or verify the package version before use in controlled workflows.

Risk: Generated reports may expose private repository metadata, commit details, or change URLs.

Mitigation: Review report contents before sharing and limit distribution to authorized audiences.

## Reference(s):

- [diffmanifests ClawHub Skill Page](https://clawhub.ai/craftslab/skills/diffmanifests)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to produce command invocations and report paths; the CLI output file may be JSON, plain text, or Excel depending on extension.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
