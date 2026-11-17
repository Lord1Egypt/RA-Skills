## Description:

Queries a 1688 distribution knowledge base for shipping workflows, product listing operations, order management, and related channel-specific distribution guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Chinese-language 1688 distribution documentation, filtered by sales channel and distribution tool, and receive step-by-step operational guidance with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a reusable 1688 Access Key and may store it in OpenClaw configuration.

Mitigation: Configure the key through a protected secrets mechanism where possible, avoid sharing it in chat or shell history, and review permissions on ~/.openclaw/openclaw.json.

Risk: The skill can send configuration updates through OPENCLAW_GATEWAY_URL when that environment variable is set.

Mitigation: Use only a trusted local or managed gateway endpoint and do not point OPENCLAW_GATEWAY_URL at untrusted hosts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/skills/1688-distribution-knowledge-newton)
- [ClawHub Publisher Profile](https://clawhub.ai/user/1688aiinfra)
- [1688 Access Key Portal](https://clawhub.1688.com)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Chinese Markdown summaries with ranked document excerpts, source URLs, relevance scores, and image links when present]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and an ALI_1688_AK access key; queries may be filtered by channel and distribution tool.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
