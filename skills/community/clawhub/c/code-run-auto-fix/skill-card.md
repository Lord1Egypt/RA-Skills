## Description:

自动运行并调试 Python、C 和 x86_64 汇编代码，在出错时调用龙虾平台 LLM 修复并返回可执行版本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyk-404](https://clawhub.ai/user/zyk-404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to run Python, C, or x86_64 assembly snippets and receive a repaired code version when execution, compilation, assembly, or linking errors occur.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs user-submitted and LLM-modified code on the host without visible sandboxing or approval gates.

Mitigation: Install and run it only in a disposable, least-privileged sandbox or container with no secrets, no sensitive source trees, strict resource limits, and network access disabled unless explicitly needed.

Risk: Submitted code and error output may be sent to the platform LLM during automatic repair.

Mitigation: Do not submit proprietary code, credentials, or sensitive data unless that disclosure is acceptable for the deployment environment.

Risk: Dependencies are not pinned in the artifact requirements file.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zyk-404/skills/code-run-auto-fix)

## Skill Output:

**Output Type(s):** [Code, Text, Shell commands]

**Output Format:** [Plain text code returned by MCP tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the final code string after running the submitted code and, when an error is detected, one LLM repair attempt.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
