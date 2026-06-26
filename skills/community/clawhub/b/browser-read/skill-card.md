## Description: <br>
Extract readable content from browser pages as markdown. Use when web_fetch fails (bot protection, auth-required pages, Twitter/X, LinkedIn) and you already have the page open in the browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill492](https://clawhub.ai/user/bill492) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Browser Read to extract readable markdown from an already-open browser page when normal web fetching fails because of bot protection, authentication, or dynamic content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can return visible text and URLs from logged-in pages selected for extraction. <br>
Mitigation: Avoid using it on private messages, account settings, dashboards, or other sensitive authenticated pages unless that page text and URL may be shared with the agent. <br>
Risk: Extraction may fall back to broad body text when primary readable-content extraction fails. <br>
Mitigation: Review the returned markdown before relying on it for decisions or sharing it further. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bill492/browser-read) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [JSON object containing markdown content and page metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes title, content, excerpt, byline, site name, content length, and URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
