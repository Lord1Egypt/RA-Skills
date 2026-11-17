## Description:

家庭消费意图识别 - 从家庭聊天文本中识别消费意图，输出结构化JSON

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaichao87](https://clawhub.ai/user/wuhaichao87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to classify household chat text for consumer purchase intent and return a structured result with category, intent stage, strength, keywords, and reason.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional API can expose household chat classification over the network more broadly than expected.

Mitigation: Prefer the CLI or Python function for local use; if the API is used, bind it to 127.0.0.1, restrict CORS, and add authentication for any shared deployment.

Risk: Household chat snippets may contain private family conversations or other sensitive personal context.

Mitigation: Minimize or redact input text before classification and avoid sending private conversations to shared deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhaichao87/skills/family-intent-recognition)
- [Declared homepage](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON object with has_intent, intent_category, intent_stage, intent_strength, keywords, and reason fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports CLI, Python function, and optional HTTP API usage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
