## Description: <br>
Use the Bluesky CLI for timeline, search, notifications, posts, replies, threads, images, likes, reposts, follows, blocks, and mutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent operate a local Bluesky command-line client for reading timelines, searching posts, managing notifications, posting content, and performing account actions after appropriate confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post publicly and change Bluesky account state. <br>
Mitigation: Use --dry-run for public posts when final text is not already approved, enable BSKY_CONFIRM_MUTATIONS=1 for confirmation prompts, and review exact targets before delete, follow, block, mute, repost, or similar actions. <br>
Risk: Bluesky credentials or session tokens provide account access. <br>
Mitigation: Use a Bluesky app password through the hidden CLI prompt, do not paste credentials into chat or command arguments, and revoke the app password from Bluesky settings if needed. <br>


## Reference(s): <br>
- [ClawHub Bluesky Skill](https://clawhub.ai/jeffaf/bluesky) <br>
- [Bluesky](https://bsky.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from read commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read commands may return structured JSON when invoked with --json.] <br>

## Skill Version(s): <br>
1.6.3 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
