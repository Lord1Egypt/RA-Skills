## Description:

Create LLCs for AI agents with human sponsor oversight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clabasky](https://clawhub.ai/user/clabasky)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to discover Clawprint API products, register users, create AI-agent business entities, and check business status through CLI, HTTP API, or Node.js helper calls.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill handles credentials for business-formation API calls.

Mitigation: Use only trusted Clawprint endpoints, keep secret keys in protected environment variables, and avoid passing secret keys on the command line.

Risk: Business-creation calls can have legal and account-level consequences.

Mitigation: Require human sponsor oversight and explicit review before executing formation or account-related API calls.

Risk: Untrusted or HTTP API URL overrides can redirect sensitive requests.

Mitigation: Validate CLAWPRINT_API_URL and CLAWPRINT_SITE_URL before use and prefer HTTPS production endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clabasky/skills/clawprint-skill)
- [Clawprint Website](https://clawprintai.com)
- [Clawprint API](https://clawprintai.com/api)
- [README.md](README.md)
- [SETUP.md](SETUP.md)
- [REFERENCE.md](REFERENCE.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash, JSON, curl, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces API-discovery and business-formation guidance; authenticated calls depend on Clawprint public and secret key environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
