## Description:

Wrapper skill for the Ezer audit backend API that runs financial audit tasks by code, period, year, and language and returns structured final audit output from the Ezer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mx-222](https://clawhub.ai/user/mx-222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and audit operators use this skill to submit Ezer financial audit tasks with a stock code, reporting period, year, and language, then retrieve the completed structured audit result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send audit request data and an optional bearer token to any URL configured in EZER_API_BASE_URL, including plaintext HTTP endpoints.

Mitigation: Use only a controlled Ezer endpoint, prefer HTTPS for non-local endpoints, and keep EZER_API_BASE_URL fixed to the intended server.

Risk: Bearer tokens used with untrusted or plaintext endpoints may be exposed.

Mitigation: Avoid broad or long-lived bearer tokens and rotate any token that was used with an untrusted or plaintext endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mx-222/skills/ezer-multiagent-auditor)
- [Publisher profile](https://clawhub.ai/user/mx-222)

## Skill Output:

**Output Type(s):** [json, shell commands, guidance]

**Output Format:** [JSON result payload on stdout, with JSON error payloads on stderr for failed API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and EZER_API_BASE_URL; may use EZER_BEARER_TOKEN when the Ezer API requires authentication.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
