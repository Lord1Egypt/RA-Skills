## Description: <br>
AI 投毒内容过滤助手。检测和识别 GEO 投毒内容，验证信息来源可信度，标记潜在虚假信息，保护用户免受 AI 投毒攻击。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[testmtcode](https://clawhub.ai/user/testmtcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a lightweight local heuristic scan for suspicious promotional or AI-manipulation wording, receive risk scores, and get filtering guidance before trusting or reusing content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation overstates source and domain verification compared with the current local keyword-checking behavior. <br>
Mitigation: Use the skill as a heuristic text scanner and independently verify websites, domain age, source reputation, and misinformation claims with reviewed tools. <br>
Risk: Optional packages are described for possible future expansion but are not required by the current local detection implementation. <br>
Mitigation: Avoid installing optional packages unless a reviewed feature specifically requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/testmtcode/ai-poison-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, shell commands, guidance] <br>
**Output Format:** [Console text reports, optional JSON results, and markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Current behavior is local heuristic text and file scanning; source and domain verification claims require independent review before relying on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
