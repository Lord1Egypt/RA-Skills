## Description: <br>
Dispatch coding tasks to the local OpenAI Codex CLI with background execution, status polling, and answerable clarifying questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeperl](https://clawhub.ai/user/abeperl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to delegate multi-file coding tasks, refactors, script creation, and project work from OpenClaw to a local Codex CLI process while preserving status polling and clarifying-question handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A background Codex process can perform broad automated coding work in the selected local work directory. <br>
Mitigation: Run it only in narrow, trusted, preferably git-tracked directories and review diffs before using the results. <br>
Risk: Prompts, logs, answers, status, and result data are stored on disk under ~/.codex-bridge. <br>
Mitigation: Avoid secrets in prompts and delete old task directories when they are no longer needed. <br>
Risk: Task identifiers map to local task directories. <br>
Mitigation: Use simple task IDs without path characters. <br>
Risk: Long-running background jobs may continue outside the initiating interaction. <br>
Mitigation: Monitor task status and logs while jobs are running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeperl/codex-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/abeperl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with shell commands, status output, JSON task records, and generated code or file changes from Codex.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the codex CLI; task state, prompts, output, logs, questions, answers, and results are stored under ~/.codex-bridge/tasks/<task-id>/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
