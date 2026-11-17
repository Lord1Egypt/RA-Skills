## Description:

Baidu Netdisk AIVideoNotes creates transcript notes, outline notes, and image-rich notes from local or online videos using Baidu's AI video note APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ide-rea](https://clawhub.ai/user/ide-rea)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to send video URLs or permitted local videos to Baidu Netdisk AI video-note services, poll task status, and receive generated transcript, outline, or illustrated notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local videos may be uploaded to Baidu services during task creation.

Mitigation: Use the skill only with videos you are allowed to send to Baidu, and avoid sensitive local recordings unless the upload behavior is acceptable.

Risk: Requests can be routed through an environment-controlled proxy when DUMATE_SCHEDULER_URL and DUMATE_SESSION_ID are set.

Mitigation: Run the skill in a trusted environment and ensure those environment variables cannot be attacker-controlled.

Risk: The skill requires a Baidu API key for normal operation.

Mitigation: Provide BAIDU_API_KEY only in trusted shells or secret-managed environments and avoid exposing it in logs or shared command history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ide-rea/skills/ai-notes-for-video)
- [Baidu Qianfan API base](https://qianfan.baidubce.com/v2)
- [Baidu AppBuilder BOS upload endpoint](https://appbuilder.baidu.com/v2/tools/bos/upload)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; creates tasks, polls status, and prints generated notes or progress messages.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
