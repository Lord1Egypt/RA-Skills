## Description: <br>
Publish social media posts to LinkedIn and Twitter/X via Buffer GraphQL API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to publish or schedule approved posts to Nissan's connected LinkedIn and Twitter/X channels through Buffer. Users should confirm the exact post text, channel, and schedule before creating a post. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish publicly through Buffer-connected social accounts. <br>
Mitigation: Confirm the exact post text, target channel, and schedule before any createPost call. <br>
Risk: The Buffer API key authorizes actions on behalf of the account owner. <br>
Mitigation: Keep the Buffer key restricted and use account or channel lookup only when channel discovery is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nissan/buffer-publisher) <br>
- [Buffer GraphQL API](https://api.buffer.com/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with Python, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Buffer GraphQL createPost and channel lookup guidance for immediate or scheduled publishing.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
