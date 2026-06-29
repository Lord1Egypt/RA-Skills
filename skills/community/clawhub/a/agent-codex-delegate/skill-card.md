## Description: <br>
Use when OpenClaw should delegate coding, repository analysis, file edits, test runs, or code review to the local Codex CLI without asking for or embedding an OpenAI API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlacroix82](https://clawhub.ai/user/jlacroix82) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to delegate repository analysis, code changes, test debugging, code review, and refactoring tasks from OpenClaw to a locally authenticated Codex CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate coding tasks to a locally authenticated Codex CLI and may receive sensitive repository content or credentials if the operator includes them. <br>
Mitigation: Install only when intentional, use explicit invocation wording, and avoid sending secrets, private keys, or production data unless that exact data flow has been approved. <br>
Risk: Workspace-write or danger-full-access sandbox modes can allow file changes or broader system access. <br>
Mitigation: Use read-only for analysis, approve workspace-write only for intended edits, and reserve danger-full-access for isolated machines or containers with explicit operator approval. <br>
Risk: Delegated output may be incorrect or misleading for code review, debugging, or file-change tasks. <br>
Mitigation: Treat Codex output as another agent's report and verify important claims, diffs, and test results locally before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jlacroix82/agent-codex-delegate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown or plain text, with optional JSONL event logs and output files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegates to the local Codex CLI and returns Codex's final answer; optional wrapper flags control sandbox level, working directory, prompt source, JSON event logging, and output file capture.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
