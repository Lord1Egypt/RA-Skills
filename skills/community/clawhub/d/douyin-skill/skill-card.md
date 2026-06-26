## Description: <br>
Douyin-skill helps agents log in to Douyin Creator Platform, reuse a local browser session, upload videos, and optionally publish or save drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lancelin111](https://clawhub.ai/user/lancelin111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and automation developers use this skill to manage Douyin Creator Platform login sessions, upload video files with metadata, and choose between publishing or saving a draft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Douyin login cookies and browser session data locally. <br>
Mitigation: Protect the skill directory, avoid sharing its contents, and run node scripts/manage.js clear when the saved session is no longer needed. <br>
Risk: The upload command can publish through the logged-in Douyin Creator account. <br>
Mitigation: Use --no-publish for tests or drafts and review the title, description, tags, and account context before allowing publication. <br>
Risk: The first upload after login may require SMS verification. <br>
Mitigation: Keep the account owner available for the first upload and enter the verification code only in the official Douyin browser flow. <br>


## Reference(s): <br>
- [Douyin-skill on ClawHub](https://clawhub.ai/lancelin111/douyin-skill) <br>
- [Project homepage from ClawHub metadata](https://github.com/lancelin111/douyin-mcp-server) <br>
- [Douyin Creator Platform](https://creator.douyin.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Node.js command examples and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Douyin cookie and Chromium profile files inside the skill directory.] <br>

## Skill Version(s): <br>
0.7.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
