## Description:

Runs Gemini CLI as a headless worker agent for long-running, parallelizable, fallback, validation, deep research, and code-analysis tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cl0ckt0wer](https://clawhub.ai/user/cl0ckt0wer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate self-contained work to Gemini CLI when they need headless execution, parallel analysis, long-context review, or a fallback worker. It is best suited for file-based tasks where required inputs and writable outputs can be scoped explicitly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-approved Gemini CLI tool use can read, write, or execute through broad included directories.

Mitigation: Run in a dedicated environment with narrowly scoped include directories and separate read-only inputs from writable output folders.

Risk: Using --yolo on untrusted remote content can let external content influence autonomous file or shell actions.

Mitigation: Avoid --yolo on untrusted remote content unless a human has reviewed the prompt and inputs first.

Risk: Including home, root, credential, or shared temporary paths can expose sensitive files or shared state.

Mitigation: Do not include home, root, credential directories, or shared /tmp paths; create task-specific directories with minimal required contents.

## Reference(s):

- [ACP vs Headless](references/acp-vs-headless.md)
- [Prompt Patterns](references/prompt-patterns.md)
- [Troubleshooting](references/troubleshooting.md)
- [Wrapper Script](scripts/gemini-run.sh)
- [Agent Communication Protocol](https://agentcommunicationprotocol.dev/)
- [ClawHub Skill Page](https://clawhub.ai/cl0ckt0wer/skills/gemini-worker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and Gemini CLI file or stdout outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be written to caller-specified files or returned as concise stdout summaries; directory access depends on explicitly included paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG, released 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
