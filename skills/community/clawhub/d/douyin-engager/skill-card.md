## Description:

Automates Douyin searches and uses Playwright to comment on videos and follow creators with configurable keywords, comments, counts, and intervals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viv888-ai](https://clawhub.ai/user/viv888-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to guide an agent through Douyin engagement workflows that search for topic-relevant videos, post selected comments, and follow creators through a logged-in browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a logged-in Douyin session to post comments and follow creators.

Mitigation: Install and run it only when that account automation is intentional; review the keyword, comment text, count, and interval before execution.

Risk: The browser profile may retain login state in `browser_data`.

Mitigation: Use a dedicated account in an isolated environment and clear `browser_data` when retained login state is not desired.

Risk: Frequent automated engagement may trigger platform controls or unwanted account activity.

Mitigation: Keep counts and intervals conservative, confirm the target content before running, and stop if Douyin surfaces warnings or failed actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viv888-ai/skills/douyin-engager)
- [Douyin website](https://www.douyin.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text, configuration]

**Output Format:** [Markdown guidance with inline shell commands and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also create a local JSON engagement log when the automation script runs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
