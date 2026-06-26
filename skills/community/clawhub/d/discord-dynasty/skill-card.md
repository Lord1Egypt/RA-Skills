## Description: <br>
Handles Discord task-center forum: create task posts, archive tasks by tag, and respect model tags. Supports six-ministries style channel template (司礼监+六部). Use when user says 新建任务、开个任务、归档任务、建六部管理频道, or when asked to create a task from todo/calendar. Requires Discord forum integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nannyu](https://clawhub.ai/user/nannyu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage Discord forum-based task centers, including creating task posts, archiving tasks with tags, and setting up optional six-ministries channel templates. It is intended for agents with Discord forum integration and the permissions needed for thread, tag, and optional channel operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Discord task threads, tags, and optional channel structures as part of its stated workflow. <br>
Mitigation: Use a least-privilege Discord bot, limit access to the intended server or channels, and review any bulk channel-template creation before execution. <br>
Risk: Forum tag and channel operations depend on Discord tool support and permissions. <br>
Mitigation: Confirm that the Discord integration supports forum threads, applied tags, channel creation, and the required permissions before relying on automated task-center setup. <br>


## Reference(s): <br>
- [Discord task-center API and implementation reference](reference.md) <br>
- [Six-ministries channel template](templates/six-ministries.json) <br>
- [Minimal six-ministries channel template](templates/six-ministries-minimal.json) <br>
- [ClawHub Discord skill](https://clawhub.ai/steipete/discord) <br>
- [OpenClaw Discord channel documentation](https://docs.openclaw.ai/channels/discord) <br>
- [Ai Court reference architecture](https://clawhub.ai/wanikua/ai-court) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with Discord tool/API call instructions, optional shell commands, and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Discord threads, tags, and channels when the paired Discord tool and permissions are available.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
