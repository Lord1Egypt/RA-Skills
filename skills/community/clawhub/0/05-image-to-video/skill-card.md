## Description:

Converts a static image URL into a short generated video clip by calling a configured image-to-video API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghwyever](https://clawhub.ai/user/ghwyever)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content production teams use this skill to turn static image assets into short video clips for video material creation and short-drama style motion shots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the supplied image URL and API key to the configured external endpoint.

Mitigation: Use an HTTPS API_BASE from the intended provider, scope the API key to this use case, and apply spending or quota limits where possible.

Risk: Image URLs may contain reusable tokens, signed private parameters, or other sensitive access details.

Mitigation: Avoid passing private signed URLs or URLs with reusable tokens unless the endpoint is trusted and the exposure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghwyever/skills/05-image-to-video)

## Skill Output:

**Output Type(s):** [API Calls, Text]

**Output Format:** [JSON object containing a video_url string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API_KEY, API_BASE, and MODEL_NAME environment variables; sends the supplied image URL to the configured provider endpoint.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
