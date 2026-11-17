## Description:

Upload files to 123pan (123云盘) and generate shareable links, including short share links and direct download links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solarise94](https://clawhub.ai/user/solarise94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to upload selected local files to 123pan and return shareable links for downstream sharing or download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local files leave the machine and are stored on 123pan, and generated links may make those files accessible to others.

Mitigation: Use the skill only for files intended for 123pan storage, review generated links before sharing, and prefer the least-exposing link type for the use case.

Risk: 123pan API, WebDAV, and rclone credentials are sensitive and may expose broader account access if reused or stored unsafely.

Mitigation: Use a dedicated low-privilege 123pan token, keep credentials in environment variables or ignored local files, and avoid committing credentials.

Risk: The optional rclone/WebDAV paths may read existing rclone configuration that contains unrelated cloud service credentials.

Mitigation: Set an isolated RCLONE_CONFIG for 123pan and avoid running WebDAV/rclone paths with unrelated secrets in the environment.

Risk: Subprocess and network upload paths broaden dependency and execution risk.

Mitigation: Pin dependencies in a virtual environment and review the selected upload path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solarise94/skills/123pan-upload)
- [123pan developer dashboard](https://www.123pan.com/dashboard/dev)
- [123pan website](https://www.123pan.com)
- [123pan OpenAPI endpoint](https://open-api.123pan.com)
- [123pan WebDAV endpoint](https://webdav.123pan.cn/webdav)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON upload results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns upload status, file metadata, and a short, direct, or share link when upload succeeds.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
