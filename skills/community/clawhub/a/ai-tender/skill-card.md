## Description:

AI-Tender automates bid-document parsing from document ingestion through tender requirement extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengcheng8632](https://clawhub.ai/user/chengcheng8632)

### License/Terms of Use:

MIT-0

## Use Case:

External users and proposal teams use this skill to parse tender documents, classify the relevant industry template, extract bid requirements, check completeness and compliance, and produce a previewable PDF result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start an unauthenticated preview server and leave it running.

Mitigation: Use it in a trusted, isolated environment, or change the preview server to bind to loopback only or disable it.

Risk: Real API keys stored in scripts/env_config.md may be exposed if the skill directory is served for preview.

Mitigation: Do not store production API keys in the served skill directory; prefer environment variables or a local secret store and rotate keys regularly.

Risk: Bid content is sent to the user-configured LLM provider, and vendor promotional links or QR content may appear in generated outputs.

Mitigation: Use only approved LLM endpoints for sensitive bid documents and review generated PDF output before sharing it.

## Reference(s):

- [AI-Tender on ClawHub](https://clawhub.ai/chengcheng8632/skills/ai-tender)
- [Publisher Profile](https://clawhub.ai/user/chengcheng8632)
- [Biaoshu Mofang Website](https://biaoshu.supcon.com/?scene=01010040)
- [Security Statement](SECURITY.md)
- [Runtime Configuration](scripts/env_config.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown/text instructions with bash commands plus a generated PDF preview file and local preview URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided bid document and OpenAI-compatible LLM API configuration; may start an unauthenticated preview server.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
