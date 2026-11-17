## Description:

Extracts the first post text from a provided Facebook URL using simple server-side HTML scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duylori](https://clawhub.ai/user/duylori)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to attempt extraction of visible post text from a supplied Facebook page or post URL. It is best suited for public, static HTML content and will return an error when content requires login, JavaScript rendering, or other unsupported access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary user-supplied URLs from the runtime environment.

Mitigation: Restrict use to approved public domains, block private and metadata IP ranges including redirects, and review before installation in environments with access to internal services.

Risk: Fetched pages may be large, unexpected, or controlled by third parties.

Mitigation: Cap response size, keep network timeouts, and pin dependencies before production use.

Risk: Facebook or other modern pages may require login or JavaScript, causing incomplete or failed extraction.

Mitigation: Use the returned error status as a failure signal and avoid treating missing content as proof that no post exists.

## Reference(s):

- [Query Examples](references/queries.md)
- [Post Schema](references/schema.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON status object printed to stdout, with concise Markdown guidance from the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns either extracted content or an error message; does not handle authenticated pages or JavaScript-rendered content.]

## Skill Version(s):

1.0.0 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
