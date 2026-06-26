## Description: <br>
Automatically generates and posts optimized social media content promoting GitHub bounty campaigns using repository data and custom messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vut08905](https://clawhub.ai/user/vut08905) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to promote GitHub bounty campaigns by generating call-to-action social posts from repository metadata and an optional custom message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post externally from connected social accounts. <br>
Mitigation: Use accounts and credentials intended for this workflow, review generated posts and target platforms before posting, and prefer revocable least-privilege tokens. <br>
Risk: Generated campaign content may be incomplete, misleading, or unsuitable for the target audience. <br>
Mitigation: Preview and approve post text before publishing or scheduling it. <br>
Risk: The release depends on axios and may need dependency maintenance before production use. <br>
Mitigation: Update or pin dependencies, especially axios, before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vut08905/autopost-github-bounty) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown and command-line examples with generated social post text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub and social-platform credentials for live posting workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
