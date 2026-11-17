## Description:

Exec Inspector helps agents inspect and analyze OpenClaw exec tool history, including command searches, usage statistics, session views, exports, and live monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengzk-bj](https://clawhub.ai/user/zhengzk-bj)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to review OpenClaw command activity across sessions, audit recent work, search for specific commands, and export or monitor execution history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private OpenClaw session history across past sessions.

Mitigation: Treat displayed reports and exported history as sensitive, redact private data before sharing, and restrict use to environments where session-history inspection is acceptable.

Risk: Persistent monitoring can continue collecting exec activity after setup.

Mitigation: Start the monitoring daemon only after reviewing the script behavior, confirm how to stop it, and stop it when continuous monitoring is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhengzk-bj/skills/exec-inspector)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [README.md](artifact/README.md)
- [QUICKSTART.md](artifact/QUICKSTART.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summarized command-history reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive command history, exported JSON, session identifiers, timestamps, model metadata, and usage statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
