## Description:

一步步引导学习算法，不直接给答案。适用于学习 LeetCode 算法题，采用苏格拉底式提问教学法，先引导思考暴力解法，再优化到最优解，每道题完成后自动生成题解文档和代码文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaodingyang](https://clawhub.ai/user/xiaodingyang)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and developers use this skill to practice LeetCode-style algorithms through guided questions, progressive solution design, code review, and generated study notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update training notes, progress tracking, README files, and TypeScript solution files in the workspace.

Mitigation: Use it in a workspace where those files are expected, or ask the agent to preview filenames before writing.

Risk: Correctness feedback may be based on code inspection rather than direct test execution.

Mitigation: Run examples or tests separately before relying on a generated solution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaodingyang/skills/algorithm-mentor)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Conversational guidance with Markdown study documents and TypeScript solution files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update an algorithm-training directory, progress.md, per-problem README.md files, and TypeScript solution files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
