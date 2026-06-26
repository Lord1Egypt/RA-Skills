## Description: <br>
ChronoSync synchronizes OpenClaw session chat history into shared local memory files so other sessions can recover context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallccwc](https://clawhub.ai/user/smallccwc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to back up local session histories, share context across sessions, and derive local decision or todo files from synced chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly copies OpenClaw chat history into persistent shared local memory files. <br>
Mitigation: Install only when cross-session chat sharing is intended, review generated files under ~/.openclaw/workspace/memory/sync/, and avoid sensitive work unless this persistence is acceptable. <br>
Risk: A configured cron job can continue syncing sessions in the background. <br>
Mitigation: Review the cron entry after installation and remove it when automatic syncing is no longer wanted. <br>
Risk: Plugin behavior can derive and store decisions or todos from chat content. <br>
Mitigation: Keep only trusted plugin files enabled and review the generated decisions and todos directories. <br>


## Reference(s): <br>
- [ChronoSync ClawHub listing](https://clawhub.ai/smallccwc/chronosync) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Local JSON and Markdown files with shell command and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes shared chat history, decision notes, todo notes, and a change-detection hash file under the configured OpenClaw memory sync directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and changelog show 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
