## Description: <br>
Extract the main X/Twitter post or article content from a page that is already open in the browser (using browser act evaluate). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill492](https://clawhub.ai/user/bill492) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract cleaned main text from an already open X/Twitter post or article when direct web fetching is blocked, noisy, or not focused on the main content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extractor can read and return text from the currently open browser page, including sensitive content if run on the wrong page. <br>
Mitigation: Run it only on the intended public X/Twitter post or article, and avoid private messages, email, account settings, internal tools, and other sensitive pages. <br>
Risk: X/Twitter page structure changes or non-X fallback behavior may return incomplete or noisy text. <br>
Mitigation: Review the returned title, URL, status, and content before relying on the extracted text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bill492/browser-read-x) <br>
- [Publisher profile](https://clawhub.ai/user/bill492) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [JSON object containing title, content, excerpt, byline, siteName, length, url, and status fields; content is cleaned markdown-like text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs against the currently open browser page and may use a generic fallback on non-X pages or extraction errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
