## Description: <br>
Beep · 小喇叭 adds real-time spoken announcements for OpenClaw agent activity, including received messages, task progress, completion, and errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wililam](https://clawhub.ai/user/wililam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add audible status updates to OpenClaw workflows. It is most appropriate where spoken announcements are expected and prompt or response content has been reviewed for privacy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on spoken announcements can expose sensitive prompts, replies, or task details to nearby people. <br>
Mitigation: Use the skill only in environments where speech is acceptable, avoid announcing secrets or personal data, and disable announcements when privacy is required. <br>
Risk: Announcement text may leave the machine through edge-tts. <br>
Mitigation: Review messages before speech generation and avoid sending confidential content to the text-to-speech service. <br>
Risk: Generated speech may remain in local audio cache files. <br>
Mitigation: Review cache settings and clear local audio caches when announcements may contain sensitive information. <br>
Risk: Suggested edits to core agent files and hooks can make speech persistent across sessions. <br>
Mitigation: Review or skip the integration edits and hooks unless persistent announcements are explicitly desired. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/wililam/beep-skills) <br>
- [Publisher Profile](https://clawhub.ai/user/wililam) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands, Python helper usage, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, announcement commands may generate spoken audio and local MP3 cache files.] <br>

## Skill Version(s): <br>
2.2.1 (source: ClawHub release evidence; artifact files report 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
