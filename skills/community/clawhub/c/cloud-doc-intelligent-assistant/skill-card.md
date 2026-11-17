## Description:

Retrieves, stores, compares, and monitors public documentation from Alibaba Cloud, Tencent Cloud, Baidu Cloud, and Volcengine, returning raw content and diffs for the calling agent to summarize.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrb-aia](https://clawhub.ai/user/mrb-aia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to fetch and cache cloud provider documentation, establish local baselines, compare documents across providers, and detect documentation changes for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activation rules are broad enough to trigger when supported cloud providers are merely mentioned.

Mitigation: Use the skill only for explicit cloud documentation retrieval, comparison, change checks, or monitoring, and ask a clarifying question when the cloud provider or product is ambiguous.

Risk: Webhook notifications and optional .env loading can send change summaries to configured endpoints or import local environment values into the skill process.

Mitigation: Enable webhook URLs and CLOUD_DOC_MONITOR_LOAD_DOTENV only in trusted workspaces, and review configured destinations before sending notifications.

Risk: Outbound requests to public cloud documentation APIs can fail or encounter rate limits.

Mitigation: Use explicit doc_ref retrieval for bounded fetches and keep conservative request delays configured for monitoring runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrb-aia/skills/cloud-doc-intelligent-assistant)
- [ClawHub publisher profile](https://clawhub.ai/user/mrb-aia)
- [OpenClaw integration](references/openclaw-integration.md)
- [Cloud API contracts](references/cloud-api-contracts.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [JSON responses containing structured machine data plus human-readable text or Markdown summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local SQLite data, logs, cache entries, and notification Markdown depending on configuration.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
