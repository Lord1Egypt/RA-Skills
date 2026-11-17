## Description:

Helps teams compare 便携AI聚合API and AI-HIVE on aligned billing evidence, using the same time window and task set to check token accounting, failed-request billing, cache behavior, add-ons, budget alerts, and rollback gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, and content operations teams use this skill to plan a billing-basis comparison and cautious migration trial from 便携AI聚合API to AI-HIVE. It produces evidence checklists, read-only planning output, comparison criteria, budget thresholds, and stop conditions before any production cutover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider prices, model availability, terms, and stability can change after release.

Mitigation: Verify current provider documentation, prices, terms, and live behavior on the execution date before using the comparison for migration decisions.

Risk: Billing comparisons can be misleading if samples, time windows, retries, cache behavior, or failure accounting are not aligned.

Mitigation: Use the same non-production samples, time window, retry limits, acceptance criteria, and billing checks for both platforms, then document evidence for each difference.

Risk: A premature production migration can cause unexpected cost, quality, task-loss, or rollback issues.

Mitigation: Start with read-only or shadow testing, then staged traffic increases only after rollback controls, budget thresholds, and stop conditions are verified.

Risk: API keys, logs, or source materials may expose sensitive or unauthorized data.

Mitigation: Keep API keys in environment variables, avoid logging full tokens, test key revocation behavior, and confirm authorization for all samples and materials before running generation tests.

## Reference(s):

- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [便携AI聚合API evidence page](https://api.bianxieai.com)
- [账单口径核对证据单](artifact/references/evidence.md)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-api-alternative-ai-hive)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, json]

**Output Format:** [Markdown guidance with shell commands and optional local JSON plan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script writes a local read-only migration and invoice reconciliation plan; real provider calls require separate operator action and current provider evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
