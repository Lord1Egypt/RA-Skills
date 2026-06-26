## Description: <br>
Use OpenAI Codex CLI for code review, refactoring, CI repair, feature implementation, and Clawdbot delegation as a subagent or direct tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phucanh08](https://clawhub.ai/user/phucanh08) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to route coding tasks from Clawdbot to Codex CLI for code exploration, implementation, reviews, refactors, and CI fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad autonomous execution can edit files or run commands in repositories where the user did not intend that level of access. <br>
Mitigation: Start with read-only or approval-required modes, scope work with --cd and limited writable paths, and review diffs before committing. <br>
Risk: Full-auto, yolo, or danger-full-access modes can increase the impact of incorrect commands or untrusted repository behavior. <br>
Mitigation: Avoid --full-auto, --yolo, and danger-full-access for untrusted repositories; use stricter approval and sandbox settings first. <br>
Risk: Copied Codex authentication files may expose sensitive credentials. <br>
Mitigation: Treat Codex auth files as credentials and avoid sharing, committing, or moving them outside trusted local profiles. <br>


## Reference(s): <br>
- [Codex CLI Overview](https://developers.openai.com/codex/cli) <br>
- [Codex CLI Features](https://developers.openai.com/codex/cli/features) <br>
- [Codex CLI Reference](https://developers.openai.com/codex/cli/reference) <br>
- [Slash Commands Guide](https://developers.openai.com/codex/cli/slash-commands) <br>
- [AGENTS.md Spec](https://agents.md) <br>
- [Codex GitHub](https://github.com/openai/codex) <br>
- [Clawdbot Integration](clawdbot-integration.md) <br>
- [Codex CLI Quick Reference](cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON-style configuration examples, and guidance text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
