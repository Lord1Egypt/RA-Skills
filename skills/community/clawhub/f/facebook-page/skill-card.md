## Description: <br>
Facebook Page manager for posting, scheduling, replying, moderation, insights, and other Meta Graph API actions using local Page credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seph1709](https://clawhub.ai/user/seph1709) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, page operators, and automation agents use this skill to manage a Facebook Page through Meta Graph API calls, including content publishing, comment handling, event operations, and insights lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post, schedule, delete, hide, publish, and moderate public Facebook Page content. <br>
Mitigation: Manually confirm any action that changes public content or moderation state before execution. <br>
Risk: The skill uses long-lived local Page credentials stored in ~/.config/fb-page/credentials.json. <br>
Mitigation: Restrict the credentials file, avoid synced or shared folders, remove FB_APP_SECRET after setup, and rotate the Page token if exposed or the host is compromised. <br>
Risk: Broad Meta permissions can expand the impact of a mistaken or unauthorized action. <br>
Mitigation: Grant only the minimum Meta permissions required for the intended workflow. <br>


## Reference(s): <br>
- [Published ClawHub Skill](https://clawhub.ai/seph1709/facebook-page) <br>
- [Meta for Developers](https://developers.facebook.com/apps/) <br>
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline PowerShell commands and Meta Graph API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces inline API-call guidance; the artifact includes no standalone scripts.] <br>

## Skill Version(s): <br>
1.0.16 (source: server release metadata, published 2026-03-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
