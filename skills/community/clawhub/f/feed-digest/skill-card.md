## Description: <br>
Feed Digest helps an agent fetch, triage, and summarize RSS, Atom, and JSON feed entries using the feed CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odysseus0](https://clawhub.ai/user/odysseus0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to catch up on feed subscriptions by fetching unread posts, selecting high-signal entries, reading full Markdown content, and summarizing why each item matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external feed CLI source. <br>
Mitigation: Install only from trusted sources and verify the feed CLI before use. <br>
Risk: The workflow can mark triaged feed entries as read. <br>
Mitigation: Ask the agent not to run the mark-read command, or require confirmation before changing read status. <br>


## Reference(s): <br>
- [ClawHub Feed Digest skill](https://clawhub.ai/odysseus0/feed-digest) <br>
- [Publisher profile: odysseus0](https://clawhub.ai/user/odysseus0) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown digest with inline shell commands and feed entry summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the external feed CLI; full entries are read as Markdown and selected entries may be marked read.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
