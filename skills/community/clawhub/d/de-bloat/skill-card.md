## Description:

用于任何会产生或修改代码的任务：写代码、新增功能、加接口、改代码、重构、修 bug、写脚本，涉及 C++、Go、Java、Python、Node.js 时同样适用。用户说「简单点」「别过度设计」「复用已有的」「抽一下公共方法」「按官方规范写」「至简」「de-bloat」「YAGNI」，或代码里出现重复造轮子、复制粘贴的相似代码、层层 try-catch、空兜底、为未来预留的抽象时，即使没有点名也应使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninetyhe-90](https://clawhub.ai/user/ninetyhe-90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software engineering agents use this skill when creating or changing code. It guides them to inspect the project, reuse existing behavior, make focused changes, follow the relevant language conventions, preserve security basics, and verify claims with current evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may invoke the skill for coding tasks where its full workflow is not relevant.

Mitigation: Confirm the request involves creating or changing code and apply only the workflow steps that fit the task.

Risk: The security assessment notes partial inspection coverage and unresolved purpose-mismatch flags in evaluation samples.

Mitigation: Review recommendations against the task and verify resulting changes with the project's checks before relying on completion claims.

## Reference(s):

- [Reuse discovery guidance](artifact/references/reuse-discovery.md)
- [Over-defense patterns](artifact/references/over-defense-patterns.md)
- [Security floor](artifact/references/security-floor.md)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Go documentation comments](https://go.dev/doc/comment)
- [Oracle Java Code Conventions](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html)
- [Oracle Javadoc Tool Guide](https://www.oracle.com/technical-resources/articles/java/javadoc-tool.html)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown responses with code changes or diffs, commands, and verification evidence as appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-dependent; may include concise rationale and current command output]

## Skill Version(s):

1.5.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
