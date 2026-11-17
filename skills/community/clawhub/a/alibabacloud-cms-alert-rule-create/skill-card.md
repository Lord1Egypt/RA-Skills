## Description:

Create and query Alibaba Cloud alert rules through the Alibaba Cloud CLI for CMS 1.0 resource monitoring and CMS 2.0 Prometheus, APM, and UModel workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to create, query, preview, and verify Alibaba Cloud CMS alert rules while selecting the correct CMS 1.0 or CMS 2.0 workflow for the monitored resource.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through authenticated Alibaba Cloud CLI changes that affect monitoring alert rules.

Mitigation: Use a least-privileged RAM identity and review every generated command and JSON body before execution.

Risk: The skill includes runtime CLI plugin update setup, which can change the execution environment.

Mitigation: Avoid runtime plugin updates unless the plugin version can be verified before use.

Risk: Delete, disable, or update examples outside the core create/query flow could affect existing alert coverage if reused carelessly.

Mitigation: Restrict operation to the intended create/query workflow and require explicit human confirmation for any state-changing command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-cms-alert-rule-create)
- [Skill Overview](artifact/SKILL.md)
- [Critical Rules](artifact/references/critical-rules.md)
- [Step 0: Intent Routing](artifact/references/step0-intent-routing.md)
- [Step: Query Alert Rules](artifact/references/step-query.md)
- [Step 1: Context Lock](artifact/references/step1-context-lock.md)
- [Step 2: Query Generation](artifact/references/step2-query-generation.md)
- [Step 3: Detection Config](artifact/references/step3-detection-config.md)
- [Step 4: Notification Config](artifact/references/step4-notification.md)
- [Step 5: Preview and Execute](artifact/references/step5-preview-execute.md)
- [Step 6: Verification](artifact/references/step6-verification.md)
- [CMS 2.0: Query Alert Rules](artifact/references/cms2-step-query.md)
- [CMS 2.0 Step 1: Context Lock](artifact/references/cms2-step1-context-lock.md)
- [CMS 2.0 Step 2: Query Config](artifact/references/cms2-step2-query-config.md)
- [CMS 2.0 Step 3: Detection Config](artifact/references/cms2-step3-detection-config.md)
- [CMS 2.0 Step 5: Preview and Execute](artifact/references/cms2-step5-preview-execute.md)
- [Common Metrics Quick Reference](artifact/references/metrics.md)
- [Prometheus Metrics Reference](artifact/references/prometheus-metrics.md)
- [APM Metrics Reference](artifact/references/apm-metrics.md)
- [RAM Permissions](artifact/references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Alibaba Cloud CLI commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configuration summaries, confirmation prompts, validation guidance, and verification steps for Alibaba Cloud alert rule operations.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
