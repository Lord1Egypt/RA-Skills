## Description:

Fetch HTML or screenshots from known blocked or JavaScript-rendered webpages with Dataify Web Unlocker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve HTML or screenshots from public webpages that are blocked, CAPTCHA-protected, or require JavaScript rendering. It is suited to explicit, single-page fetches where the target URL is known and credentials remain in environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes broader search and business-scraping workflows beyond the advertised Web Unlocker behavior.

Mitigation: Review installed files before use and invoke only the Web Unlocker wrappers unless broader workflows are explicitly approved.

Risk: Requests can pass through caller-supplied headers or cookies, and token setup guidance may encourage persistent shell-profile storage.

Mitigation: Use the skill only for public, non-sensitive webpages; avoid session cookies and private headers; prefer session-scoped DATAIFY_API_TOKEN configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-web-unlocker)
- [Dataify Web Unlocker API endpoint](https://webunlocker.dataify.com/request)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; API responses are returned as text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN and an explicit public HTTP(S) target URL.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
