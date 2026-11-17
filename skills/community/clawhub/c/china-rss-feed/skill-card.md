## Description:

Helps Chinese OpenClaw users set up an RSS subscription workflow with China mirror configuration, feed installation, OPML import, and RSS aggregation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roryyu](https://clawhub.ai/user/roryyu)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users in China use this skill to install an RSS feed tool with China mirror settings, import a curated OPML list of technical feeds, and aggregate subscriptions through a separate rss-digest skill.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The setup installs external software with an unpinned Go module version.

Mitigation: Review the resolved feed source and install a pinned version or commit before use.

Risk: The workflow asks users to install rss-digest by bare skill name, which can make publisher, version, and permissions ambiguous.

Mitigation: Verify the exact rss-digest skill, publisher, version, and permissions before installing it.

Risk: The imported OPML list causes the aggregation workflow to contact many third-party RSS sources.

Mitigation: Review the OPML feed list first and run setup in a container or non-sensitive environment where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roryyu/skills/china-rss-feed)
- [Publisher Profile](https://clawhub.ai/user/roryyu)
- [Referenced RSS feed recommendation post](https://x.com/zodchiii/status/2034924354337714642?s=46)
- [Go China module proxy](https://goproxy.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash, prompt, XML, and OPML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup guidance for Linux systems using apt, China Go proxy configuration, and prompts for a separately installed rss-digest skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
