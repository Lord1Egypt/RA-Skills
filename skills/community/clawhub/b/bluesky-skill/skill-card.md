## Description: <br>
Manage a Bluesky account for posting, replies, likes, reposts, follows, blocks, mutes, search, timelines, threads, notifications, direct messages, and profile updates via the AT Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JohannesSeikowsky](https://clawhub.ai/user/JohannesSeikowsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a Bluesky social media account from shell commands, including reading timelines, engaging with posts, managing social graph actions, sending direct messages, and updating profile content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make sensitive Bluesky account changes, including posting, deleting, direct messaging, profile updates, and social graph actions. <br>
Mitigation: Require explicit user approval before any posting, deleting, direct messaging, profile, follow, mute, block, like, or repost action. <br>
Risk: Authentication uses a Bluesky app password and stores a reusable session token on disk. <br>
Mitigation: Use a dedicated Bluesky app password, avoid unnecessary direct-message access, and delete ~/.bsky_session.json when switching accounts, using a shared machine, or revoking access. <br>
Risk: Running the wrong local command could operate on an unintended script or account context. <br>
Mitigation: Confirm the actual script path and the BLUESKY_HANDLE value before running account-changing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JohannesSeikowsky/bluesky-skill) <br>
- [Bluesky app passwords](https://bsky.app/settings/app-passwords) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; command responses are JSON objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus BLUESKY_HANDLE and BLUESKY_APP_PASSWORD; authentication may create ~/.bsky_session.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
