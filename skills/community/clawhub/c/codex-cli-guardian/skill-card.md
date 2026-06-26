## Description: <br>
Codex CLI Guardian manages API key setup, background Codex task execution, result summaries, PID locking, status tracking, and worker orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alukardo](https://clawhub.ai/user/alukardo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding tasks to Codex CLI in the background while tracking, summarizing, and stopping active jobs. It also provides worker templates and orchestration patterns for multi-step coding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local credential storage can expose API keys if the workspace or skill directory is not tightly controlled. <br>
Mitigation: Use only a disposable or tightly scoped workspace and do not enter a valuable API key until secret input and storage are fixed. <br>
Risk: Background Codex execution can perform high-impact code actions with weak scoping. <br>
Mitigation: Review carefully before installing, run only in constrained workspaces, and scan outputs before using the skill on real projects. <br>
Risk: The security evidence flags a confirmed shell-command construction flaw around `bash -c` invocation. <br>
Mitigation: Replace the `bash -c` invocation with safe argument passing before using the skill on real projects. <br>
Risk: Bundled task history may expose prior task descriptions or summaries. <br>
Mitigation: Remove bundled task history before installation or distribution. <br>
Risk: Broad natural-language auto-triggers may start automation unintentionally. <br>
Mitigation: Use explicit confirmation and narrower trigger phrases before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alukardo/codex-cli-guardian) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Codex CLI reference](artifact/CLI.md) <br>
- [Format and workflow references](artifact/REFERENCES.md) <br>
- [Usage examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with bash command snippets and JSON task/status records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Background task runner with one active task guarded by PID locking, local credential setup, and task history summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
