## Description: <br>
加密货币自学系统。每天早上9点自动推送学习内容；每次调用都必须产出小白友好、可直接学习的详细报告（不是只给标题），并通过 web_search 检索并整合最新资料。包含完整学习大纲（小白向、投资向、进阶投资三个阶段），支持进度跟踪、跳过与重置。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmzo](https://clawhub.ai/user/hmzo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External learners use this skill to follow a structured Chinese-language cryptocurrency curriculum with daily lessons, progress tracking, topic skipping, and reset controls. The skill is educational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lesson runs can advance or reset saved local progress. <br>
Mitigation: Review progress.json before use and back it up or reset it intentionally when changing learning state. <br>
Risk: Generated cryptocurrency material may be mistaken for investment advice. <br>
Mitigation: Use the output as educational content only and independently verify any financial, trading, tax, or compliance decisions. <br>


## Reference(s): <br>
- [Crypto Learning ClawHub release](https://clawhub.ai/hmzo/crypto-learning) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown-style lesson reports and command-line text or JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local lesson progress in progress.json and can update that state during lesson runs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
