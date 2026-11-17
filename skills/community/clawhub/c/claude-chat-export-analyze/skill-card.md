## Description:

This skill guides agents through locally analyzing a Claude.ai web export (`conversations.json`) for search, timelines, theme extraction, statistics, and reports while preserving user privacy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaoqing404](https://clawhub.ai/user/shaoqing404)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill when they need an agent to help inspect a local Claude.ai web chat export, locate past conversations, summarize activity over time, extract themes, compute basic conversation statistics, or prepare privacy-conscious reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Claude.ai chat exports may contain secrets, personal information, or other sensitive conversation content.

Mitigation: Keep processing local, provide only the file path to the agent, review generated reports for sensitive content, and move or delete the export when analysis is complete.

Risk: Using the skill on an unsupported export format could produce incorrect analysis.

Mitigation: Validate that the file is a Claude.ai web `conversations.json` array with the expected session fields before running jq analysis, and stop for source clarification if the structure differs.

## Reference(s):

- [Claude.ai](https://claude.ai)
- [Server-resolved GitHub source](https://github.com/shaoqing404/ai-chat-timeline-skills/tree/main/skills/claude-chat-export-analyze)
- [ClawHub skill page](https://clawhub.ai/shaoqing404/skills/claude-chat-export-analyze)
- [ClawHub publisher profile](https://clawhub.ai/user/shaoqing404)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Analysis]

**Output Format:** [Markdown and text with inline jq and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local analysis summaries, timelines, selected conversation excerpts, or report drafts; sensitive output should be reviewed and redacted before sharing.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
