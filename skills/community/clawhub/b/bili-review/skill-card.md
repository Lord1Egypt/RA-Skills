## Description:

bili-review helps agents summarize Bilibili videos by collecting official AI subtitles, danmaku timing, and threaded comments into a structured Markdown review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frozentearz](https://clawhub.ai/user/frozentearz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to quickly assess Bilibili videos, compare the creator's claims with audience reactions, and produce decision-oriented summaries for reviews, tutorials, commentary, or explainers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read browser login cookies for Bilibili, save them locally as cookies.txt, and send them to Bilibili APIs.

Mitigation: Review carefully before installing, prefer a disposable or low-risk Bilibili account, avoid shared repositories, and delete generated cookie files when finished.

Risk: Persisted cookies could expose Bilibili account access if copied, committed, or left in an unsafe workspace.

Mitigation: Run the skill only in a private workspace, keep cookies.txt out of source control, and verify local file permissions before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frozentearz/skills/bili-review)
- [Project homepage](https://github.com/frozentearz/bili-review)
- [Publisher profile](https://clawhub.ai/user/frozentearz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with video metadata, speed-read cards, detailed analysis sections, timestamped subtitle and danmaku evidence, and comment excerpts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local Python commands and yt-dlp to fetch Bilibili subtitles, danmaku, and comments before the agent writes the final summary.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
