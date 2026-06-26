## Description: <br>
Manages Facebook Page publishing and engagement workflows through the Graph API, including text, photo, carousel, video, Reels, Story, scheduled post, and comment operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcbaivn](https://clawhub.ai/user/mcbaivn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, social media operators, and Page managers use this skill to configure Facebook Page credentials and run Graph API workflows for publishing, scheduling, rescheduling, deleting, and commenting on Page content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, reschedule, delete, and comment on real Facebook Page content. <br>
Mitigation: Manually verify the Page ID, post or comment ID, message, media, and schedule time before allowing an agent to execute an action. <br>
Risk: Facebook Page access tokens grant powerful posting and engagement authority if exposed. <br>
Mitigation: Prefer environment variables or a secret manager over fb_config.json, restrict file permissions, and rotate or revoke the token if it may have been exposed. <br>
Risk: Broad Meta permissions can increase the impact of mistakes or credential misuse. <br>
Mitigation: Grant only the minimum permissions needed for the intended workflow and remove permissions that are not required. <br>


## Reference(s): <br>
- [Get Facebook Page Access Token](references/get-token.md) <br>
- [Facebook Page Manager API Reference](references/api-reference.md) <br>
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/) <br>
- [Meta Graph API Changelog](https://developers.facebook.com/docs/graph-api/changelog) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Facebook Page access token and Page ID; commands can publish, schedule, reschedule, delete, and comment on live Page content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
