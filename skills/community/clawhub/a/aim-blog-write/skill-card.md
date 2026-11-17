## Description:

Generates SEO-optimized blog content from a theme, industry, and language, then packages the result as structured JSON and a Word document with downloaded images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[focus-aim](https://clawhub.ai/user/focus-aim)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to request SEO blog drafts by providing a topic, industry, and target language. The skill returns generated blog content, keyword data, downloaded image assets, and a Word document for editing or publication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide an aim-secret-key through chat and stores it in a local .env file.

Mitigation: Use a safer secret store or another out-of-band credential entry flow, and do not paste real secrets into chat.

Risk: The security summary reports plaintext HTTP service calls carrying the API key.

Mitigation: Use the skill only after the provider switches credential-bearing service calls to HTTPS.

Risk: The skill downloads images returned by the external service, including possible HTTP or internal-host URLs.

Mitigation: Restrict image downloads to trusted HTTPS hosts and enforce size and content-type checks before embedding files.

Risk: Broad activation could send general blog-writing requests to the external service unexpectedly.

Mitigation: Confirm user intent before execution and require explicit theme, industry, and language inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/focus-aim/skills/aim-blog-write)
- [Publisher profile](https://clawhub.ai/user/focus-aim)
- [aim-secret-key registration](https://tools.mentarc.cn/aim-skills/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown content, JSON status/data objects, and .docx files with embedded images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires theme, industry, language, and an aim-secret-key; image download failures are logged and do not block Word document generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
