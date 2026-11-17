## Description:

从用户指定的 Java 方法向上追溯调用方，在当前 Git 仓库内生成到 HTTP、RPC 或其他入口为止的调用图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraskittles](https://clawhub.ai/user/extraskittles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to trace upstream callers of Java methods within the current Git repository and summarize how calls reach HTTP, RPC, scheduled, messaging, or root entry points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional GitNexus indexing step may use an unpinned npx command.

Mitigation: Prefer a trusted preinstalled GitNexus binary or pin and verify the npm package version before running the indexing command.

Risk: Static caller graphs may be incomplete for reflection, AOP, events, asynchronous calls, or dynamic dispatch.

Mitigation: Label uncertain branches as possible or unclosed and verify conclusions with source evidence and rg checks.

## Reference(s):

- [代码引用 examples](artifact/examples.md)
- [ClawHub skill page](https://clawhub.ai/extraskittles/skills/code-yinyong)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese Markdown with Mermaid diagrams, summary tables, and evidence file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analysis limited to the current Git repository; cross-service calls are labeled as boundaries and not traced further.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
