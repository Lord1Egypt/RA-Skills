## Description: <br>
Publishes reviewed text, image, link-in-comment, and scheduled posts to a Facebook Page through the Meta Graph API, with optional Chinese/English translation before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AAAZZZR](https://clawhub.ai/user/AAAZZZR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Social media operators and developers use this skill to draft, translate, preview, and publish content to a configured Facebook Page. It supports text posts, image posts, first-comment links, and scheduled publishing after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An unreviewed or incorrect post could be published to the configured Facebook Page. <br>
Mitigation: Require the user to confirm the destination Page, text, image, link, and schedule before approving any post. <br>
Risk: Meta Page tokens and app secrets could expose publishing access if stored insecurely. <br>
Mitigation: Store credentials securely, avoid committing them to repositories or logs, restrict local configuration access, and rotate or revoke credentials after suspected exposure. <br>
Risk: A valid request can still publish to the wrong Page or at the wrong scheduled time if the inputs are mistaken. <br>
Mitigation: Preview the Page target and scheduled time before execution and ask for edits when intent is ambiguous. <br>


## Reference(s): <br>
- [Facebook Page Access Token Setup](references/token-setup-guide.md) <br>
- [Meta for Developers](https://developers.facebook.com) <br>
- [Meta Developer Apps](https://developers.facebook.com/apps/) <br>
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown preview and command guidance, with JSON status output from the publishing script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Meta credentials in LONG_META_page_TOKEN, META_PAGE_ID, and META_APP_SECRET.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
