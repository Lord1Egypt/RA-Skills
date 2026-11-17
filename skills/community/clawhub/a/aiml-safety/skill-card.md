## Description:

Classifies submitted text with AIMLAPI guard models to help identify safe or unsafe content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aimlapihello](https://clawhub.ai/user/aimlapihello)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to run AIMLAPI guard-model checks on user input or chatbot responses and receive a safe or unsafe classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text and the AIMLAPI API key are sent to a third-party AIMLAPI endpoint.

Mitigation: Install only when that data-sharing posture is acceptable, avoid submitting sensitive content unnecessarily, and provide the API key through the documented AIMLAPI_API_KEY environment variable.

Risk: Moderation output is advisory because response parsing is weak and may misclassify ambiguous model responses.

Mitigation: Do not use this skill as the sole enforcement gate for moderation decisions without stricter response validation and human or policy review for high-impact cases.

Risk: The release text mentions image moderation, but the artifact behavior only demonstrates text checks.

Mitigation: Treat the skill as text-focused unless image support is separately validated against AIMLAPI behavior and documented inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aimlapihello/skills/aiml-safety)
- [AIMLAPI Safety API Reference](references/safety-categories.md)
- [AIMLAPI chat completions endpoint](https://api.aimlapi.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIMLAPI_API_KEY; verbose mode can print the full API JSON response.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
