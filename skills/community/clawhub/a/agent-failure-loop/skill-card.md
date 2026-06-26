## Description: <br>
An end-to-end self-improvement loop that detects agent failures, classifies them, tracks recurrence, auto-generates rules, and promotes repeated failures into AGENTS.md or CLAUDE.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reikys](https://clawhub.ai/user/reikys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record execution failures, analyze recurring patterns, and turn repeated mistakes into persistent agent rules. It is intended for local self-improvement workflows across OpenClaw, Claude Code, Codex, Cursor, and similar agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repeated failure notes can become persistent agent rules without a required human approval step. <br>
Mitigation: Run with --dry-run first, inspect .learnings/promotable.json and each proposed rule, and only enable automatic promotion after reviewing the rollback process. <br>
Risk: Failure records may capture sensitive prompts, errors, paths, or user corrections. <br>
Mitigation: Avoid recording secrets or sensitive user text in failure notes, keep outputs local unless sanitized, and review files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reikys/agent-failure-loop) <br>
- [Publisher profile](https://clawhub.ai/user/reikys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with local JSON and Markdown artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local learning summaries and promote repeated failure lessons into persistent agent-rule files.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
