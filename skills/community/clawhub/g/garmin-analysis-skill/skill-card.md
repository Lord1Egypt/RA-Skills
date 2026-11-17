## Description:

Bilingual Chinese-English workflows for using the cycling-health CLI to sync Garmin China wellness data, analyze Garmin, Intervals.icu, iGPSPORT, and Strava cycling data, and query or download Xingzhe route books.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baijian](https://clawhub.ai/user/baijian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, coaches, and self-tracking cyclists use this skill to guide an agent through supported cycling-health CLI workflows for syncing Garmin China wellness to Intervals.icu, analyzing personal cycling and recovery data, and querying route or activity sources without exposing account secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow expects a `cycling-health upgrade --output json` step that can replace local executable code before account and activity data are accessed.

Mitigation: Install only if the user trusts the CLI publisher and update channel, or require manual approval and version pinning before upgrade.

Risk: The skill handles sensitive Garmin credentials, Intervals.icu API keys, OAuth tokens, account descriptions, FIT/GPX files, and health or activity data.

Mitigation: Keep secrets and downloaded files local, use CLI authentication and status flows without pasting secrets into chat, and avoid exposing logs or file paths unless needed for troubleshooting.

Risk: Some workflows can write or delete remote or local state, including Intervals.icu wellness/settings/events, credential revocation, and GPX overwrites.

Mitigation: Preview or dry-run changes first, require explicit authorization for `--confirm`, `--overwrite`, deletes, and revocation, and read back results after writes.

Risk: The iGPSPORT integration is documented as an unsupported private CN API adapter whose behavior can change.

Mitigation: Label iGPSPORT results as unsupported private API data, preserve exact CLI errors, and avoid bypassing the public CLI with improvised raw API calls.

## Reference(s):

- [cycling-health CLI repository](https://github.com/baijian/cycling-health)
- [Garmin CLI Workflows](references/cli-workflows.md)
- [Intervals.icu CLI Workflows](references/intervals-workflows.md)
- [iGPSPORT CLI Workflows](references/igpsport-workflows.md)
- [Strava CLI Workflows](references/strava-workflows.md)
- [Xingzhe CLI Workflows](references/xingzhe-workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese-English responses; may direct the agent to create local FIT, GPX, or configuration files only when requested or authorized by the user.]

## Skill Version(s):

0.2.3 (source: evidence.json release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
