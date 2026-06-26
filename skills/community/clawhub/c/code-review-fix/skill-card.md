## Description: <br>
Automatically review code for bugs, security, style, and performance issues, provide fix suggestions, and optionally apply repairs with explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[landyun](https://clawhub.ai/user/landyun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to inspect source files for common bugs, security issues, style problems, and performance concerns. It can produce an explanatory review report and, when requested, apply simple code fixes to the target file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports under-disclosed billing and tracking behavior. <br>
Mitigation: Review billing behavior before installation, rotate or remove embedded billing credentials, and confirm charges and user tracking are acceptable. <br>
Risk: The release evidence reports external code transmission behavior. <br>
Mitigation: Do not submit proprietary code or secrets unless the third-party LLM data flow and retention terms are acceptable. <br>
Risk: The skill can automatically modify files when fix mode is enabled. <br>
Mitigation: Require reviewable diffs or explicit approval before accepting file changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/landyun/code-review-fix) <br>
- [Publisher profile](https://clawhub.ai/user/landyun) <br>
- [SkillPay billing site](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Console-oriented Markdown text with optional source-file modifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write fixes to the reviewed file when fix mode is enabled; billing commands can return balances and payment links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, config/rules.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
