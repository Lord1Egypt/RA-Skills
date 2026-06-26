## Description: <br>
用大白话帮助零编程基础用户分析代码报错、定位连锁问题，并给出可复制的修复代码。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuxin-bit](https://clawhub.ai/user/qiuxin-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Programming beginners and non-developers use this skill to turn code errors, local snippets, and related file context into plain-language explanations and repair suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local code files or logs can contain secrets such as API keys, passwords, or tokens. <br>
Mitigation: Provide only the specific files or snippets needed for the error and remove secrets before sharing. <br>
Risk: Debugging may require reading local files. <br>
Mitigation: Have the agent state which files it plans to inspect before reading them and keep inspection limited to the relevant code. <br>
Risk: Suggested repair code may be incomplete or unsuitable for the full project context. <br>
Mitigation: Review and test any proposed code before applying it; the skill is instructed not to modify files directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiuxin-bit/code-error-explainer) <br>
- [Common errors reference](references/common_errors.md) <br>
- [Chain reaction patterns reference](references/chain_reaction_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown report with plain-language explanations and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file references, causal debugging notes, replacement code, and prevention guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
