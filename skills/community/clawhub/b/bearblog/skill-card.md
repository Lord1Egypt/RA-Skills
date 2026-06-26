## Description: <br>
Create and manage blog posts on Bear Blog (bearblog.dev). Supports extended Markdown, custom attributes, and browser-based publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azade-c](https://clawhub.ai/user/azade-c) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Writers, developers, and site maintainers use this skill to draft, publish, edit, and manage Bear Blog posts through an authenticated browser session. It helps prepare Bear Blog header attributes, Markdown content, post templates, and browser actions for common publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated browser access can publish, unpublish, edit, or delete Bear Blog content. <br>
Mitigation: Require explicit user confirmation before publish, unpublish, edit, or delete actions, and verify the exact post title or URL before proceeding. <br>
Risk: Deletion examples include bypassing a browser confirmation dialog. <br>
Mitigation: Do not bypass delete confirmations unless the user has clearly requested deletion and confirmed the specific post to remove. <br>
Risk: Login flows may expose Bear Blog credentials if secrets are pasted into ordinary chat. <br>
Mitigation: Use protected secret handling where available and avoid placing passwords or sensitive account details in normal conversation. <br>


## Reference(s): <br>
- [Bear Blog](https://bearblog.dev) <br>
- [Bearblog ClawHub Listing](https://clawhub.ai/azade-c/bearblog) <br>
- [Publisher Profile](https://clawhub.ai/user/azade-c) <br>
- [Mistune](https://github.com/lepture/mistune) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with browser command snippets and Bear Blog post templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated Bear Blog browser session and browser.enabled configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
