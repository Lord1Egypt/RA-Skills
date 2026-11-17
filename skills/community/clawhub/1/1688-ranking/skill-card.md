## Description:

1688-ranking queries 1688 product ranking lists and category-level hot search keywords through the 1688 Open Platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and commerce operators use this skill to retrieve 1688 category rankings, hot-selling or value product lists, hot search keywords, and top-level category IDs for sourcing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable 1688 OAuth tokens in a shared plaintext cache.

Mitigation: Restrict cache file permissions, keep the runtime workspace private, and revoke or rotate 1688 tokens if the cache may have been exposed.

Risk: Running the authentication helper directly can print a full access token to console output.

Mitigation: Avoid running scripts/auth.py directly in logged environments and redact console output before sharing logs.

Risk: The skill requires a 1688 AppKey, AppSecret, and refresh token to call the API.

Mitigation: Use only credentials scoped for the intended 1688 application and rotate them according to the publisher's operational policy.

## Reference(s):

- [1688-ranking ClawHub release page](https://clawhub.ai/1688aiinfra/skills/1688-ranking)
- [1688 API interface documentation](references/api.md)
- [1688 Open Platform](https://open.1688.com)
- [1688 API invocation guide](https://open.1688.com/doc/apiInvoke.htm)
- [1688 API signature guide](https://open.1688.com/doc/signature.htm)
- [1688 API authorization guide](https://open.1688.com/doc/apiAuth.htm)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON API responses and plain-text category listings; Markdown guidance may include shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns raw 1688 API data, includes item IDs in product results, and reports failures as JSON error objects with exit code 1.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
