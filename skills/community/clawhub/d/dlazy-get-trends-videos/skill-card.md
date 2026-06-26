## Description: <br>
Fetches trending videos from YouTube or TikTok via Apify and returns up to N items as metadata such as title, author, views, thumbnail, and page URL filtered by keyword, time window, and sort order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query trending YouTube or TikTok video metadata through the dLazy CLI, including source, keyword, result count, time-window, and sort-order controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports inconsistent documentation about whether the skill returns metadata only or can download or return hosted media by default. <br>
Mitigation: Review the real dLazy CLI behavior before use and explicitly set video-download options according to the intended workflow. <br>
Risk: The skill requires sensitive credentials and sends requests to third-party services. <br>
Mitigation: Use scoped dLazy API keys, prefer per-invocation environment variables when appropriate, and rotate or revoke keys from the dLazy dashboard when access changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-get-trends-videos) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx and a dLazy API key; outputs may include asynchronous task identifiers or hosted media URLs depending on CLI behavior.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
