## Description:

Provides troubleshooting guidance for ossbrowser and ossutil client failures using catalog-based diagnoses and optional official documentation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Support staff and developers use this skill to diagnose ossbrowser and ossutil errors and provide troubleshooting steps, configuration guidance, and policy templates for users to review and apply themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Despite claims of no network or write behavior, some questions can trigger online documentation requests and a local documentation cache.

Mitigation: Install only if access to help.aliyun.com and a cache under the user's home directory are acceptable.

Risk: Shared AccessKeys, secrets, or STS tokens could expose cloud credentials.

Mitigation: Do not paste credentials into chat; provide only the tool name and relevant error details.

Risk: Generated RAM policy templates may include write or delete permissions.

Mitigation: Review proposed policies before applying them and remove unnecessary PutObject and DeleteObject actions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-client-tools-diagnosis)
- [Scope and limitations](artifact/references/scope-and-limitations.md)
- [Client tool troubleshooting](artifact/references/tool-troubleshooting.md)
- [OSS configuration documentation](https://help.aliyun.com/zh/oss/developer-reference/config-create-configuration-file)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with optional command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports a diagnosis or asks for more error details; users execute suggested steps themselves.]

## Skill Version(s):

0.0.1 (source: server-resolved release, artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
