## Description:

Guides an agent through an 18-step, multi-week reflective journey around Amsterdam’s winter canal light festival.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to guide people through a reflective, multi-week Amsterdam Light Festival experience, track journey progress, and collect optional reflections for a closing postcard.

### Deployment Geography for Use:

Global; the guided experience is set in Amsterdam, Netherlands.

## Known Risks and Mitigations:

Risk: The security assessment reports requests to drifts.bot involving account and profile activity whose relevance to the festival experience is unclear.

Mitigation: Before using the skill, verify why the service needs these requests and what information they submit; provide only the optional profile details needed for the experience.

Risk: The service returns an API token used for authenticated account and journey changes.

Mitigation: Keep the token private and store it securely; do not include it in logs or shared prompts.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liveneon/skills/experience-amsterdam-light-festival-canals)
- [Drifts experience page](https://drifts.bot/experience/amsterdam-light-festival-canals)

## Skill Output:

**Output Type(s):** [Text, Guidance, API calls, Shell commands]

**Output Format:** [Reflective text and Markdown guidance, with inline curl examples and JSON request/response data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [An 18-step journey; a token is required for actions that change account or journey state.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
