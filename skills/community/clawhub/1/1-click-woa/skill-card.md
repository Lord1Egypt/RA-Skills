## Description: <br>
Publishes WeChat Official Account draft articles from Markdown or text by retrieving a token, uploading images, creating the draft payload, and falling back to an HTML file when API publishing fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanbo00701](https://clawhub.ai/user/yanbo00701) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to prepare WeChat Official Account drafts from article text and a configured image directory. It is intended for workflows where an agent can execute the provided configuration checks and publishing script with user-provided WeChat credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a WeChat AppSecret in a local credentials file. <br>
Mitigation: Create the credentials file only in the documented local path, avoid committing it, and rotate the AppSecret if exposure is suspected. <br>
Risk: Unpublished article text and selected images are sent to WeChat APIs. <br>
Mitigation: Review article content and the configured image_dir before running the publish script. <br>
Risk: The fallback HTML file may contain sensitive unpublished article content. <br>
Mitigation: Treat article_fallback.html as unpublished content and share it only through approved channels. <br>


## Reference(s): <br>
- [1-Click WOA ClawHub listing](https://clawhub.ai/yanbo00701/1-click-woa) <br>
- [SETUP.md](references/SETUP.md) <br>
- [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown or terminal text, with JSON configuration and optional generated HTML fallback file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a WeChat draft through WeChat APIs and may write article_fallback.html when draft submission fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
