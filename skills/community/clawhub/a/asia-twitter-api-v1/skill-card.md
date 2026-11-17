## Description:

Search X (Twitter) in real time, monitor trends, extract posts, and analyze social media data—perfect for social listening and intelligence gathering. Safe read-only operations by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renning22](https://clawhub.ai/user/renning22)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to query Twitter/X profiles, posts, followers, trends, and search results through the AIsa API for social listening and intelligence gathering. Write automation is available but should be limited to dedicated automation accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AIsa API keys and search queries are sent to api.aisa.one.

Mitigation: Install only if this third-party service is acceptable for the intended data, keep the API key in a secret-backed environment variable, rotate it regularly, and monitor usage.

Risk: Write operations send Twitter email, password, and proxy credentials to api.aisa.one and may grant account-level control.

Mitigation: Prefer read-only operations; if write automation is necessary, use only disposable or dedicated automation accounts with unique passwords and non-sensitive proxy credentials.

Risk: Passing passwords or TOTP codes on the command line can expose them through shell history, process listings, or logs.

Mitigation: Avoid command-line secrets for real accounts; use secure secret handling and keep write operations limited to low-value test accounts.

Risk: cleanup.sh may remove files if run from a directory containing unrelated work or secrets.

Mitigation: Run cleanup only inside an isolated copy of the skill package after reviewing the target paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renning22/skills/asia-twitter-api-v1)
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa service](https://aisa.one)
- [OpenClaw documentation](https://openclaw.ai)
- [OWASP API Security](https://owasp.org/www-project-api-security/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY for AIsa API access; write operations also require Twitter account and proxy credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
