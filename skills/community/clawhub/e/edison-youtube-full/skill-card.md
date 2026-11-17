## Description:

Complete YouTube toolkit for agents: search videos, fetch metadata, browse channels and playlists, and pull transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edisonchenai](https://clawhub.ai/user/edisonchenai)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to find YouTube videos, retrieve video, channel, and playlist metadata, and extract transcripts as JSON for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package references scripts and a requirements file that are not included in the artifact.

Mitigation: Verify that the missing files are supplied by a trusted publisher or repository before installing or running the skill.

Risk: The skill uses a YouTube API key, which is a credential.

Mitigation: Use a restricted API key and avoid exposing it in shell history, logs, shared outputs, or committed files.

Risk: Search and metadata lookups can consume YouTube Data API quota.

Mitigation: Set appropriate query limits, batch requests where supported, and monitor quota usage during automated workflows.

## Reference(s):

- [Google Cloud YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; referenced scripts are expected to output JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YouTube Data API key for API-backed searches and metadata lookups.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
