## Description:

REST API calling helper that guides agents through authenticated HTTP requests, retry and timeout handling, rate limits, pagination, response parsing, and API error categorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call external or internal REST APIs, including APIs that require bearer tokens, API keys, basic authentication, pagination, retry handling, and structured response capture. It is suited for pulling API data, integrating open platforms, and generating reusable request commands or scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens or sensitive request details may be exposed through command history, logs, output previews, or generated files.

Mitigation: Use environment variables for credentials, avoid highly privileged tokens, review output files before sharing them, and avoid placing secrets in notes or logs.

Risk: The learner stores local usage notes and error details in plaintext.

Mitigation: Run the learner only against the intended skill directory and do not record secrets, private API payloads, or sensitive endpoint details.

Risk: Calls to inappropriate or non-HTTPS endpoints may expose data or violate API access expectations.

Mitigation: Use HTTPS-only API URLs, authorized credentials, conservative rate limits, and endpoint-specific review before running large or automated calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qq435912743/skills/api-caller)
- [Publisher Profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, request configuration details, and optional JSON or file outputs from API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API call results depend on the target endpoint, credentials, rate limits, timeout settings, and optional local learner notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
