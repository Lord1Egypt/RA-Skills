## Description: <br>
Multi-platform video auto-publisher. Automatically upload videos to Douyin, WeChat Channels, Xiaohongshu, Bilibili, YouTube and more. Supports batch publishing, scheduled posting, auto-caption generation, and hashtag optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[954215110](https://clawhub.ai/user/954215110) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, operators, and developers use this skill to publish video content across multiple social platforms with generated captions, tags, account configuration guidance, and Playwright-driven upload commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publishing script can post to multiple real social-media accounts without a final confirmation or dry-run safeguard. <br>
Mitigation: Run visibly first, test with specific target platforms, and avoid all-platform, headless, or scheduled operation until the account behavior is confirmed. <br>
Risk: Local account, configuration, cookie, and publish-log files may reveal account setup or posting history. <br>
Mitigation: Protect local configuration and log files, avoid sharing them, and delete stale account data when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/954215110/auto-publisher) <br>
- [Publisher profile](https://clawhub.ai/users/954215110) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local account configuration and publish-log files when the provided publishing script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
