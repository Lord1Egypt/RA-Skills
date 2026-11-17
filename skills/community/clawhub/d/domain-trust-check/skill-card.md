## Description:

Checks URLs and domains for phishing, malware, brand abuse, and scam risk using the Outtake Trust API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesouttake](https://clawhub.ai/user/jamesouttake)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agents use this skill to check whether URLs in emails, messages, or workflows appear safe before visiting or recommending them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs submitted for checking are sent to Outtake's service with API authentication, which can expose sensitive links, internal hostnames, or query parameters.

Mitigation: Avoid submitting password reset links, private documents, internal hostnames, or URLs with sensitive query parameters unless sharing them with Outtake is acceptable.

Risk: The skill depends on an Outtake API key for authenticated requests.

Mitigation: Store OUTTAKE_API_KEY as a secret or environment variable and avoid placing it in prompts, source files, or shared logs.

## Reference(s):

- [Domain Trust Check API Reference](references/api.md)
- [Outtake](https://outtake.ai)
- [Domain Trust Check on ClawHub](https://clawhub.ai/jamesouttake/skills/domain-trust-check)
- [Outtake Bounty Network related skill](https://clawhub.ai/jamesouttake/outtake-bounty-network)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OUTTAKE_API_KEY and curl; batch checks support up to 50 URLs per request.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
