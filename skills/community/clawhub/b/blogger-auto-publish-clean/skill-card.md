## Description: <br>
Automatically publish Markdown articles to Google Blogger with batch publishing, draft management, and automatic HTML conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rainco2008](https://clawhub.ai/user/rainco2008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and content operators use this skill to configure OAuth access to a Blogger account, convert Markdown articles to Blogger HTML posts, publish drafts or live posts, and list existing blog posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access to a Blogger account and can publish to a live blog. <br>
Mitigation: Use a test blog first, prefer draft mode for validation, and grant access only to accounts where the user is comfortable allowing Blogger write operations. <br>
Risk: Google credentials and OAuth tokens are sensitive files used by the skill. <br>
Mitigation: Keep credentials.json and token.json private, restrict file permissions, and avoid committing or sharing them. <br>
Risk: The bundled examples include deletion and automation flows that may affect existing blog content. <br>
Mitigation: Avoid deletion examples unless backups exist, and review automation scripts before running them against production blogs. <br>
Risk: The security review flags an unauthenticated publishing webhook example as under-scoped. <br>
Mitigation: Do not deploy webhook publishing without authentication, input limits, and network restrictions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rainco2008/blogger-auto-publish-clean) <br>
- [API Reference](references/REFERENCES.md) <br>
- [Examples](references/EXAMPLES.md) <br>
- [Google Blogger API v3 Reference](https://developers.google.com/blogger/docs/3.0/reference) <br>
- [Google APIs Node.js Client](https://github.com/googleapis/google-api-nodejs-client) <br>
- [OAuth 2.0 for Web Applications](https://developers.google.com/identity/protocols/oauth2/web-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JavaScript configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and commands that can trigger live Blogger API actions when valid OAuth credentials and a blog ID are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
