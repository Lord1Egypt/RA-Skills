## Description:

Automates login, upload, and publishing of videos to the Douyin Creator Platform, including tag management and login status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gonghaiquan](https://clawhub.ai/user/gonghaiquan)

### License/Terms of Use:


## Use Case:

Creators and account operators use this skill to have an agent prepare and publish videos to Douyin, including titles, descriptions, tags, and login status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables public posting through an external MCP server package that is not pinned in the evidence.

Mitigation: Pin and verify the MCP server package before installation, and review it before granting account access.

Risk: The skill can publish to a Douyin account on the user's behalf.

Mitigation: Confirm the target account, title, description, tags, and final publishing action before each post.

Risk: The workflow persists Douyin login cookies.

Mitigation: Protect saved cookies with least practical local access and delete them when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gonghaiquan/skills/douyin-publish)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and publishing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account status, publishing details, tag lists, and result links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
