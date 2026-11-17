## Description:

Ship a complete album in one run: write or reuse lyrics, render tracks, generate cover and slideshow art per song, publish either one album film or one video per track plus a playlist, deploy the audio to a radio host, premiere it on air, and fan out the links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and release operators use this skill to coordinate album release workflows that produce tracks, artwork, video assets, playlist publishing, radio deployment, premiere timing, and announcement copy from a JSON-driven pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can trigger public publishing, radio deployment, service restarts, playlist creation, premiere actions, and social posts without clear approval gates.

Mitigation: Require explicit human approval before uploads, deployment, service restart, playlist creation, premiere actions, and social posting.

Risk: Agents may access real music, video, social, OAuth, radio, SSH, or cron-sourced credentials while carrying out the workflow.

Mitigation: Review credential scope before installation, run with least-privilege accounts, and audit access to provider, host, OAuth, SSH, and cron-sourced credentials.

Risk: JSON configuration or shell plumbing mistakes could cause skipped work, malformed prompts, duplicate posts, or unintended operational behavior.

Mitigation: Parse JSON configuration as data, run preflight checks, verify ledgers and upload existence, and compare enabled fanout adapters before marking a release complete.

## Reference(s):

- [ClawHub skill page: Album Release Pipeline](https://clawhub.ai/nickflach/skills/album-release)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown guidance with JSON configuration examples and command-oriented operational notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide public upload, radio deployment, service restart, playlist creation, premiere, and social posting workflows that require manual approval and credential review.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
