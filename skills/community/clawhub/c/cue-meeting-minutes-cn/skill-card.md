## Description:

将会议录音整理为带时间锚的逐字稿、话题分段、决策与待办，并标出需人工核实的内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

员工和团队可用此技能把会后录音整理成可回查的会议纪要、决策和待办；负责人仅在录音中自报时记录，不清楚的内容留待人工核实。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious for remote service discovery and credential-handling behavior that may not match the meeting-minutes purpose; its scan covered 11 of 13 components, with partial inspection of two.

Mitigation: Before installing, review the credential destination checks, network behavior, and the purpose mismatch identified in the security guidance; treat uninspected content as unassessed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-meeting-minutes-cn)
- [Cue Omni Reader setup and documentation](https://cuecue.cn/hub/omni-reader)
- [Cue API key setup](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown meeting-minutes card with timestamped transcript, topic segments, decisions, action items, and items for human review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional audio channel provides transcript and timestamp evidence. Per-file audio input is limited to the channel-reported byte ceiling (documented as 256 MiB); real-time transcription is out of scope.]

## Skill Version(s):

0.2.31 (source: SKILL.md frontmatter; server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
