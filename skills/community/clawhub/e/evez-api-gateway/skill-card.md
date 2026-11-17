## Description:

Connect to the EVEZ AI API, an OpenAI-compatible API for routing LLM calls through EVEZ models including evez-smart, evez-code, evez-fast, and evez-vision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure agents or applications to call EVEZ as an OpenAI-compatible API gateway for chat, code, fast-response, and vision model workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, outputs, and image URLs may be routed through EVEZ's remote service.

Mitigation: Review EVEZ data handling and compliance terms before use, and avoid sending secrets, regulated data, private customer content, or internal image URLs unless approved.

Risk: The skill configures remote API calls that depend on third-party service availability and behavior.

Mitigation: Validate the target endpoint, API key handling, model behavior, and fallback requirements before using it in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-api-gateway)
- [EVEZ OpenAI-compatible API endpoint](https://evez-api2.fly.dev/v1)
- [EVEZ signup](https://evez-api2.fly.dev/signup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API configuration values, model names, client wrapper guidance, and remote API call examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
