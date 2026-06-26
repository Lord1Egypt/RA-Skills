## Description: <br>
Runs long-running Codex CLI coding tasks in the background for git repositories, including task logs, status checks, process stopping, and sandbox-bypass execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianyn1990](https://clawhub.ai/user/tianyn1990) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to launch and manage long-running Codex coding work in a local git repository while keeping the main OpenClaw session available. It is intended for implementation, test, and build workflows that may continue in the background. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsandboxed background Codex jobs can modify local files without ongoing approval. <br>
Mitigation: Use only in a dedicated, backed-up git repository with no secrets or sensitive files, and review resulting changes before relying on them. <br>
Risk: Arbitrary task text or target paths can cause unintended work in the wrong directory. <br>
Mitigation: Use trusted task descriptions and known target directories; avoid passing untrusted input or sensitive paths to the command scripts. <br>
Risk: Background processes may continue after the initiating session returns. <br>
Mitigation: Monitor ~/.codex-logs, check process status, stop the Codex process when finished, and verify it has exited. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianyn1990/codex-runner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON session payloads; command scripts emit plain text logs and status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start background processes and write task logs under ~/.codex-logs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
