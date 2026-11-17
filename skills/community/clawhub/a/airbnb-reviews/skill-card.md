## Description:

Read normalized Airbnb reviews for a listing, with native rating scales preserved. Use when a user wants ratings or guest feedback for a listing on Airbnb. Powered by StayingAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and interpret listing reviews and guest ratings through StayingAPI, including pagination, async job handling, platform support, and native rating scales.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: StayingAPI keys could be exposed if pasted directly into prompts or committed to files.

Mitigation: Store STAYINGAPI_KEY in a protected agent environment or secret manager, and use sandbox keys for testing.

Risk: Live API calls may use account credits and make network requests to StayingAPI.

Mitigation: Confirm intended live-data use before enabling a live key, and review StayingAPI pricing for credit behavior.

Risk: Review results can be incomplete because endpoint support, pagination, async jobs, and upstream coverage vary by platform and listing.

Mitigation: Check platform support, honor pagination metadata, inspect async job status and warnings, and preserve native rating scales instead of rescaling silently.

Risk: Aggressive polling can trigger rate limiting.

Mitigation: Honor Retry-After headers, back off between polling attempts, and cap retry attempts.

## Reference(s):

- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI pricing](https://stayingapi.com/pricing)
- [Authentication setup](references/auth-setup.md)
- [ClawHub skill listing](https://clawhub.ai/stayingapi/skills/airbnb-reviews)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with REST API parameters, shell commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and internet access to api.stayingapi.com; live API calls may use account credits; sandbox keys return fixtures at zero cost.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
