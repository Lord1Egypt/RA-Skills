## Description:

Monitors clipboard text and rewrites copied articles, links, or short topics into draft content for Douyin, Xiaohongshu, and Bilibili.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nh5gntnf78-oss](https://clawhub.ai/user/nh5gntnf78-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social-media operators use this skill to turn clipboard content into platform-specific Chinese draft posts and save them as local files for later review and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can monitor ordinary clipboard text and persist copied content to local desktop files.

Mitigation: Use one-time processing unless continuous monitoring is intentional, avoid copying secrets or private content while it runs, and store outputs in a non-synced folder.

Risk: Generated social-media drafts may retain sensitive or inappropriate source material from the clipboard.

Mitigation: Review generated Markdown and summary files before publishing, and delete generated files regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nh5gntnf78-oss/skills/clipboard-content-factory)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown draft files and a JSON summary written to a local output directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces separate draft files for Douyin, Xiaohongshu, and Bilibili, plus summary metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
