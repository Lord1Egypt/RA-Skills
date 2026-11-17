## Description:

Finds reference video clips on frameset.app from keywords, returns collection pages and original YouTube or Vimeo links, and can guide downloads to the local Downloads folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredhnian](https://clawhub.ai/user/fredhnian)

### License/Terms of Use:


## Use Case:

Creative researchers, video editors, and agents assisting Chinese-language users use this skill to search Frameset for advertising or film reference clips, confirm selections from screenshots, collect source links, and optionally download selected videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill browses third-party video-reference sites and may download selected YouTube or Vimeo videos to ~/Downloads, creating rights and storage risks.

Mitigation: Only download content the user has rights to store, confirm selected items before downloading, and monitor file sizes.

Risk: Bulk selections can lead to many video lookups or downloads.

Mitigation: Ask for confirmation when more than 10 items are selected and cap processing at 15 selections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fredhnian/skills/find-reference-video)
- [Frameset search](https://frameset.app/search?search=%E5%85%B3%E9%94%AE%E8%AF%8D)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown table with collection links, original video links, and optional inline bash download commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include screenshots for user selection and optional downloaded video files in ~/Downloads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
