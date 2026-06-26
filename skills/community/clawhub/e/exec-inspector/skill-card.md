## Description: <br>
Exec Inspector helps agents inspect and analyze OpenClaw exec command history with search, statistics, daily views, exports, and live monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengzk-bj](https://clawhub.ai/user/zhengzk-bj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators using OpenClaw use this skill to review recent shell command activity, search session history, summarize tool usage, export records, and monitor new exec activity. It is most useful for local workflow review, troubleshooting, and audit-style inspection of OpenClaw sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session logs that may contain sensitive command history. <br>
Mitigation: Install only when local command-history access is acceptable, prefer targeted one-shot queries, and redact exported history or full JSON records before sharing. <br>
Risk: Persistent monitoring can continue exposing new exec activity if left running. <br>
Mitigation: Avoid enabling the daemon unless its script has been reviewed, and stop monitoring when the inspection task is complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhengzk-bj/exec-inspector) <br>
- [README.md](artifact/README.md) <br>
- [QUICKSTART.md](artifact/QUICKSTART.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown summaries with shell command snippets and optional JSON history exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw session logs; exported history may contain sensitive command data.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and artifact README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
