## Description: <br>
Create local chat rooms for AI agents with channels, mentions, task claims, and durable summaries in the workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multiple AI agents through local workspace room files, including channels, directed mentions, task claims, jobs, and handoff summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Room files can accumulate operational context that should not be treated as private storage. <br>
Mitigation: Keep secrets, tokens, and unrelated personal data out of room logs; periodically review summaries, inbox entries, and saved defaults. <br>
Risk: Stale summaries, jobs, or claims can misdirect later agents or block shared work. <br>
Mitigation: Refresh summaries when work pauses or changes, release stale claims, and keep handoffs tied to an explicit next owner. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ivangdavila/chat-rooom) <br>
- [Skill homepage](https://clawic.com/skills/chat-rooom) <br>
- [Setup process](artifact/setup.md) <br>
- [Room protocol](artifact/protocol.md) <br>
- [Daily operations](artifact/operations.md) <br>
- [Memory template](artifact/memory-template.md) <br>
- [Example room patterns](artifact/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local room, channel, inbox, claim, job, summary, and durable preference files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
