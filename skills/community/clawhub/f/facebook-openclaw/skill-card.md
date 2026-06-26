## Description: <br>
fboc is a CLI skill for managing Facebook Page posts, comments, page information, and scheduled publishing through the Facebook Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phuongsky](https://clawhub.ai/user/phuongsky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to configure Facebook Page credentials, inspect Page content, publish or schedule posts, manage comments, and hide or delete Page content from an agent-accessible CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles powerful Facebook Page credentials. <br>
Mitigation: Review the code before installation, use a non-production Facebook Page first, keep tokens out of shared shells and logs, and rotate any token used with the package. <br>
Risk: Posting and test workflows can affect live Facebook Page content. <br>
Mitigation: Run setup and tests only after confirming the target Page and token scope, and validate content in a non-production Page before using a production Page. <br>
Risk: Hide and delete commands can remove or change public visibility of Page content. <br>
Mitigation: Verify post or comment IDs before execution, avoid force or confirm flags unless the action has been reviewed, and prefer reversible hiding where practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phuongsky/facebook-openclaw) <br>
- [Facebook Developers](https://developers.facebook.com/) <br>
- [Facebook Graph API documentation](https://developers.facebook.com/docs/graph-api) <br>
- [Facebook Page reference](https://developers.facebook.com/docs/graph-api/reference/page) <br>
- [Facebook Page posts reference](https://developers.facebook.com/docs/graph-api/reference/page/posts) <br>
- [Facebook post comments reference](https://developers.facebook.com/docs/graph-api/reference/post/comments) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Facebook Page access token and can create, schedule, hide, or delete live Facebook Page content.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
