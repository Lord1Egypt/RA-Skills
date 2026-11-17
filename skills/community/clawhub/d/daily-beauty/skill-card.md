## Description:

Daily Beauty retrieves one Xiaohongshu beauty blogger and returns nine full-body image results while filtering previously used bloggers, AI accounts, wallpaper accounts, and marketing accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorexxar](https://clawhub.ai/user/lorexxar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to fetch a curated daily set of Xiaohongshu beauty blogger images, with deduplication and account filtering applied before results are returned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can send results to a hardcoded Feishu recipient.

Mitigation: Remove or parameterize the recipient and require explicit confirmation before delivery.

Risk: The workflow downloads and processes unvalidated remote images locally.

Mitigation: Enforce HTTPS and host allowlists, add file size and file type checks, and sandbox ImageMagick conversion.

Risk: Persistent deduplication records may retain source image URLs and blogger identifiers.

Mitigation: Review retention requirements and clear or rotate the JSON records when they are no longer needed.

## Reference(s):

- [Daily Beauty ClawHub Skill Page](https://clawhub.ai/lorexxar/skills/daily-beauty)
- [Blacklist Reference](references/blacklist.md)
- [Whitelist Reference](references/whitelist.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown usage guidance and JSON runtime output with local image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime writes downloaded image files locally and updates JSON deduplication records.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
