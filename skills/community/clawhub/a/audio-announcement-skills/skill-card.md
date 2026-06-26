## Description: <br>
Beep - Xiao Laba provides voice announcements for agent status updates, including received requests, task progress, completion, and errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wililam](https://clawhub.ai/user/wililam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add spoken, real-time status announcements to OpenClaw workflows and command-line agent tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on spoken updates may reveal task context to nearby listeners or become disruptive during normal agent work. <br>
Mitigation: Install only when voice status updates are desired, keep announcement text generic, and use the provided enable/disable and configuration controls to limit when speech is active. <br>
Risk: The skill proposes persistent changes to global agent instruction and startup files, which can make announcements carry across future sessions. <br>
Mitigation: Review the proposed edits to AGENTS.md, MEMORY.md, IDENTITY.md, TOOLS.md, USER.md, and startup hooks before applying them, and remove persistence mechanisms that are not needed. <br>
Risk: Announcement text is sent through an online TTS dependency. <br>
Mitigation: Avoid using confidential or sensitive text in announcements, prefer short generic phrases, and pin dependencies before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wililam/audio-announcement-skills) <br>
- [Publisher profile](https://clawhub.ai/user/wililam) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, configuration snippets, and spoken audio side effects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Announcement text should be concise; the skill can play local audio, write user-level configuration and cache files, and fall back to console output.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata, artifact metadata, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
