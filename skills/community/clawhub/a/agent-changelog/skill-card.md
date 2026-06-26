## Description: <br>
Advanced handling for agent-changelog requests (history, diffs, restores, rollbacks, snapshots) using git and OpenClaw scripts with clear, user-focused summaries and outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noambens](https://clawhub.ai/user/noambens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect workspace change history, compare versions, restore files, roll back changes, and set up automated git-based workspace versioning with optional GitHub or PromptLayer sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent workspace versioning automation and hooks. <br>
Mitigation: Install only when persistent versioning is intended, and review existing OpenClaw hooks before setup because setup can replace matching hook directories. <br>
Risk: The default tracked scope can include the whole workspace. <br>
Mitigation: Before setup or first sync, narrow `.agent-changelog.json` to specific paths when appropriate and audit `.gitignore` and tracked files for secrets. <br>
Risk: External sync can automatically push commits to GitHub or upload tracked workspace snapshots to PromptLayer. <br>
Mitigation: Enable GitHub or PromptLayer sync only after confirming that automatic pushes or full tracked-repository snapshots are acceptable for the workspace. <br>
Risk: PromptLayer sync requires a sensitive API key. <br>
Mitigation: Set `PROMPTLAYER_API_KEY` securely in the environment and do not paste the key into chat or tracked files. <br>


## Reference(s): <br>
- [Agent Changelog on ClawHub](https://clawhub.ai/noambens/agent-changelog) <br>
- [Publisher profile: noambens](https://clawhub.ai/user/noambens) <br>
- [PromptLayer public API endpoint](https://api.promptlayer.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured status, log, diff, restore, rollback, and setup output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return raw script stdout for explicit slash-command invocations; summaries are concise for conversational history and diff requests.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
