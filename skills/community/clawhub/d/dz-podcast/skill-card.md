## Description:

Generate and publish a dual-host daily podcast. Fetches news, generates a conversational script between two hosts, synthesizes audio via Fish Audio or Edge TTS, publishes to S3 with RSS feed for Apple Podcasts, Spotify, etc. Fully automated with cron support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dz1922](https://clawhub.ai/user/dz1922)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to generate daily news podcast briefs, rewrite them as a two-host dialogue, synthesize audio, publish episodes to an RSS feed, and automate recurring production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated public publishing can distribute inaccurate, confidential, or copyrighted material.

Mitigation: Add a manual review and approval step before uploading audio or updating the public RSS feed.

Risk: S3 feed mutation and cron automation can overwrite or publish unintended podcast content.

Mitigation: Use a dedicated bucket, least-privilege AWS credentials, backup feed.xml before mutation, and test updates before enabling cron.

Risk: External TTS sends generated script text to Fish Audio and the bundled script contains placeholder API key handling.

Mitigation: Avoid confidential source text, load API keys from environment variables or a secret manager, and verify TTS provider terms before use.

## Reference(s):

- [RSS Feed Format Reference](references/rss-format.md)
- [Fish Audio](https://fish.audio)
- [ClawHub Skill Page](https://clawhub.ai/dz1922/skills/dz-podcast)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash commands, script-generated MP3 audio, and RSS XML updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured news sources, TTS voices, S3 hosting, and cron scheduling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
