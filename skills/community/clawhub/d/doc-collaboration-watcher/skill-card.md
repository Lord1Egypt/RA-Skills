## Description: <br>
Monitors collaboration Markdown documents for changes, notifies configured communication channels, and records a lightweight change history for multi-agent or team workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lewistouchtech](https://clawhub.ai/user/lewistouchtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to watch shared project documentation, broadcast changes across OpenClaw-connected communication channels, and keep collaborators aware of updates. It is suited to multi-agent, cross-team, distributed, or documentation-heavy projects that need fast document-change visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged suspicious because it ships a plaintext ClawHub publishing token. <br>
Mitigation: Do not install or run this version until the publisher revokes and rotates the token and removes it from the package and history. <br>
Risk: Broad default monitoring and notification behavior can expose document activity across enabled channels. <br>
Mitigation: Limit monitored documents to non-sensitive files, disable or restrict automatic channel use when needed, and confirm where change-history or memory records are stored before running the watcher. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lewistouchtech/doc-collaboration-watcher) <br>
- [README](artifact/README.md) <br>
- [Skill configuration](artifact/skill.yaml) <br>
- [Channel configuration guide](artifact/examples/CONFIG-CHANNELS.md) <br>
- [Example configuration](artifact/examples/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text notifications, JSON configuration, shell command snippets, and change-history JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write doc_change_history.json and retains the most recent 100 change records.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
