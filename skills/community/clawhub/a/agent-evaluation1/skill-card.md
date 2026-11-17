## Description:

Helps developers test and benchmark LLM agents through behavioral testing, capability assessment, reliability metrics, regression testing, and production monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quality engineers use this skill to design agent evaluation workflows, compare benchmark behavior with production reliability, and identify regressions or risky evaluation practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation messages may include customer data, production traces, proprietary prompts, benchmark sets, credentials, or regulated information sent to SkillBoss/heybossai.

Mitigation: Use only data approved for SkillBoss/heybossai processing; redact sensitive material or use a local or otherwise approved endpoint for sensitive evaluations.

Risk: The skill routes evaluation messages to a fixed third-party API without enough privacy or consent guidance.

Mitigation: Review the API integration, privacy expectations, and consent requirements before installation or production evaluation use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline Python examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY when using the documented SkillBoss API Hub integration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
