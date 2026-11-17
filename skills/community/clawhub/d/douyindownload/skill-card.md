## Description:

Parses Douyin share links and returns watermark-free video download information while managing free and paid usage quotas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuss228](https://clawhub.ai/user/fuss228)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this MCP server and CLI to parse Douyin video links, retrieve title/author/cover/download URL data, check quota, and activate paid access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool ships privileged database credentials and performs paid-license activation against an external MySQL database.

Mitigation: Remove embedded credentials, rotate exposed secrets, and replace direct database access with a scoped HTTPS activation API before broad deployment.

Risk: License and device data are stored locally and sent to an external activation service.

Mitigation: Document what device and license data is stored or transmitted, and require user/operator approval before installation in managed environments.

Risk: Unsafe URL handling may allow requests beyond the intended Douyin parsing flow.

Mitigation: Harden URL validation to allow only expected Douyin hosts and URL patterns before making network requests.

Risk: The scanner guidance calls for vulnerable dependency updates before broad use.

Mitigation: Update dependencies and rerun security scanning before production rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuss228/skills/douyindownload)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)
- [Purchase and activation page](https://mcppay.fushangsong.cc/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [MCP text responses containing formatted JSON for video parsing, plus plain-text quota and activation status messages; CLI output is terminal text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parse output can include success, title, author, coverUrl, videoUrl, platform, remaining quota, plan, and error fields.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
