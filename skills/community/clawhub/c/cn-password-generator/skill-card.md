## Description: <br>
安全的随机密码生成器。支持自定义长度、字符类型（大小写字母、数字、特殊符号）、排除相似字符、批量生成。纯Python标准库，无需API Key。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill to generate random passwords with configurable length, character classes, similar-character exclusion, and batch count. It is useful when an agent needs local password generation without external APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security evidence marks this release as suspicious and describes privileged maintainer-style behavior. <br>
Mitigation: Install only when the intended use is understood and authorized; prefer dry-run or non-bypass modes where available. <br>
Risk: The release evidence includes a sensitive-credentials capability tag. <br>
Mitigation: Use an authorized account and avoid exposing generated or credential-like values in shared logs, prompts, or transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-password-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [JSON password-generation results and concise usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python script prints count, length, and generated passwords as JSON.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
