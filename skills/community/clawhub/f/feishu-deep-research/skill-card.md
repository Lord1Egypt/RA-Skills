## Description:

Generates a structured deep-research report from a user-provided topic and imports it as a Feishu document in a specified cloud-space folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henryjing96](https://clawhub.ai/user/henryjing96)

### License/Terms of Use:


## Use Case:

Analysts, researchers, and business users use this skill to run multi-step research on a topic, prepare a structured Markdown report, and deliver it as a Feishu document. It is suited to investment research, industry analysis, competitive research, and technical research workflows that require documented sources and a cloud document handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal output and error messages may expose Feishu access tokens or app secrets.

Mitigation: Redact tokens and secrets from progress logs, transcripts, and diagnostics; rotate any credentials that may have been exposed.

Risk: The workflow performs Feishu document upload and import actions using app credentials.

Mitigation: Use a least-privileged Feishu app with only the required permissions and verify the destination folder token before execution.

Risk: Generated reports include a fixed watermark that may be inappropriate for some organizations.

Mitigation: Make the watermark optional or configurable before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/henryjing96/skills/feishu-deep-research)
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu media upload API endpoint](https://open.feishu.cn/open-apis/drive/v1/medias/upload_all)
- [Feishu import tasks API endpoint](https://open.feishu.cn/open-apis/drive/v1/import_tasks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with progress text and JSON-style completion details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a research topic, a Feishu folder token, and Feishu app credentials; successful runs return document, file, ticket, and import status details.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
