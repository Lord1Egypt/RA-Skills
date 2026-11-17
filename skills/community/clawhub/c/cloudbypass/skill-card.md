## Description:

Use Cloudbypass API (穿云API/穿云) to fetch pages protected by Cloudflare/Turnstile/JS challenge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuanchuan007](https://clawhub.ai/user/chuanchuan007)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to retrieve pages that return Cloudflare, Turnstile, JavaScript challenge, or 403 responses when ordinary HTTP requests fail. It is intended for authorized protected-page retrieval using Cloudbypass credentials and, for V2/V2S or downloads, a configured proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive request data, cookies, authorization headers, API keys, proxy credentials, internal URLs, or request bodies may be sent through a third-party bypass service.

Mitigation: Use the skill only for authorized targets, avoid sending sensitive data through it unless the data-sharing and billing implications have been reviewed, and rotate or monitor keys used by autonomous agents.

Risk: The skill can be used to bypass site protections, which may create legal, ethical, or terms-of-service risk.

Mitigation: Confirm authorization before retrieving protected pages, scope target domains explicitly, and review autonomous usage before execution.

Risk: Custom apiBaseUrl values can redirect real credentials and request content to an unexpected endpoint.

Mitigation: Use the default Cloudbypass API endpoint for real credentials and avoid custom endpoints unless they have been reviewed and approved.

Risk: Cloudbypass API requests may incur billing.

Mitigation: Monitor usage, restrict who can supply credentials, and set operational limits appropriate for automated runs.

## Reference(s):

- [Cloudbypass API Quick Reference](https://docs.cloudbypass.com/api-quick-reference.md)
- [Cloudbypass Website](https://www.cloudbypass.com/)
- [ClawHub Skill Page](https://clawhub.ai/chuanchuan007/skills/cloudbypass)

## Skill Output:

**Output Type(s):** [API Calls, Code, Configuration instructions]

**Output Format:** [JavaScript response objects with status, headers, data, cookies, or a readable stream for downloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLOUDBYPASS_APIKEY; V2/V2S and download flows require CLOUDBYPASS_PROXY.]

## Skill Version(s):

0.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
