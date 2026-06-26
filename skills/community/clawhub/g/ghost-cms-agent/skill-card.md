## Description: <br>
Manage Ghost CMS content via the REST API. Create and publish posts, manage tags, and fetch site analytics. Supports both the Content API (public data) and Admin API (authenticated management). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to manage Ghost CMS content from an agent workflow, including listing posts, creating or publishing posts, managing tags, and reading site statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Ghost Admin API key that can create, update, publish, and tag live CMS content. <br>
Mitigation: Use a dedicated integration key with the minimum practical access, store it in environment variables or a secret manager, test against staging first, and review commands before using --publish or --id against production content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kryzl19/ghost-cms-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kryzl19) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with bash commands; scripts return JSON by default and table text where supported.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GHOST_URL and GHOST_ADMIN_API_KEY; GHOST_CONTENT_API_KEY is optional for public data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
