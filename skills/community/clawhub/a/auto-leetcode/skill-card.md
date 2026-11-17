## Description:

LeetCode刷题辅助技能。当用户提供LeetCode题目序号+名称时，自动获取题目内容、生成解题思路和带注释的代码，并在指定目录下创建题目文件夹。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fourierer](https://clawhub.ai/user/fourierer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use this Chinese-language skill to create local LeetCode study notes, solution explanations, and annotated code from a problem number and title. It supports Python by default and can generate C++, Java, JavaScript, Go, or Rust solutions when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes generated files to a user-specified local directory.

Mitigation: Use a normal project or notes directory, avoid sensitive or system paths, and review the resolved destination before allowing writes or overwrites.

Risk: Generated explanations or code may be incomplete or incorrect for the selected LeetCode problem.

Mitigation: Review the problem content, algorithm reasoning, and generated solution before relying on it for study or submission.

## Reference(s):

- [auto-leetcode ClawHub release page](https://clawhub.ai/fourierer/skills/auto-leetcode)
- [Code style guide](references/code-style.md)
- [Output templates](references/output-templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Guidance]

**Output Format:** [Markdown documents and source code files in a local problem folder]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a problem statement file, solution explanation file, and one language-specific code file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
