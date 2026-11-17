## Description:

多轮深度思考技能。借鉴OpenMythos循环推理架构，每次循环都注入新输入，逐轮深化理解。适用于重要决策、复杂问题、创意生成、问题发现。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaxint](https://clawhub.ai/user/jaxint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, researchers, entrepreneurs, and agents use this skill to structure multi-round reasoning for important decisions, complex problems, creative generation, and risk discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to record user identity, feedback, and future needs after use, which can capture sensitive or identifying information.

Mitigation: Configure the agent to avoid storing identity, sensitive problem details, or future needs unless the user explicitly consents and a retention and deletion policy is defined.

Risk: The skill is primarily Chinese-language, which may reduce reviewability for teams that cannot assess Chinese prompts and outputs.

Mitigation: Have a Chinese-capable reviewer inspect outputs and feedback records before deployment in workflows that affect users or business decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese-language reasoning report with staged prompts, action planning, risk review, and self-reflection.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script can print a local console report for one to six reasoning rounds.]

## Skill Version(s):

2.1.0 (source: server release metadata and skill title)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
