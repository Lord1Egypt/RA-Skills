## Description: <br>
LeetCode刷题辅助技能。当用户提供LeetCode题目序号+名称时，自动获取题目内容、生成解题思路和带注释的代码，并在指定目录下创建题目文件夹。支持用户指定编程语言（默认Python）。当用户提到LeetCode刷题、做LeetCode题目、LeetCode题解、刷算法题等场景时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fourierer](https://clawhub.ai/user/fourierer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and students use this skill to turn a LeetCode problem number and title into a local study package with problem notes, solution reasoning, and commented code in a selected programming language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent writes files to a user-provided local directory. <br>
Mitigation: Use a dedicated LeetCode folder and review the target path before allowing generation. <br>
Risk: Generated solution code or explanations may be incorrect or unsuitable to run without review. <br>
Mitigation: Review generated code and reasoning before executing or relying on it. <br>
Risk: The workflow searches and reads LeetCode-related web pages. <br>
Mitigation: Install only if this web access is acceptable for the agent's environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fourierer/auto-leetcode) <br>
- [Code Style Guide](references/code-style.md) <br>
- [Output Templates](references/output-templates.md) <br>
- [LeetCode China](https://leetcode.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [Markdown study notes plus language-specific source files with Chinese explanations and comments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a problem directory under a user-provided path; language defaults to Python when not specified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
