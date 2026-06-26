## Description: <br>
Fetch blocked and dynamic web content via Dataify Web Unlocker API. Automatically identify and bypass CAPTCHA challenges, execute full-page JavaScript rendering, and return complete raw HTML source code or PNG webpage screenshots. Applicable for complex crawling scenarios including dynamic loading pages and SPA single-page applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to fetch blocked, CAPTCHA-protected, or JavaScript-heavy web pages through Dataify's Web Unlocker API and receive raw HTML or PNG screenshots. The skill is intended for crawling workflows where the target URL is explicitly provided or confirmed by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target URLs, optional headers or cookies, and fetched page content are sent to Dataify. <br>
Mitigation: Avoid private internal URLs, session cookies, Authorization headers, bearer tokens, and personal data unless sharing them with Dataify is approved and intended. <br>
Risk: The skill depends on DATAIFY_API_TOKEN for live API calls. <br>
Mitigation: Store DATAIFY_API_TOKEN like any other API credential and use dry-run mode when previewing request payloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-web-unlocker) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify Web Unlocker API endpoint](https://webunlocker.dataify.com/request) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and direct API response text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return raw HTML source, JSON response bodies, or PNG screenshot data depending on the requested API response type.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
