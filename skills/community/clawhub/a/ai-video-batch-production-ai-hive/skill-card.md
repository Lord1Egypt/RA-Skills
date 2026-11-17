## Description:

Turns batch short-video production requests into auditable AI-HIVE workflows, runnable commands, production briefs, scripts, prompt sets, task records, and acceptance checklists for ecommerce, advertising, marketing, short-drama, and social content teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, operators, and developers use this skill to plan and run batch short-video production for multi-SKU commerce, agency operations, and content-center workflows. It helps convert project inputs into reviewable production plans, storyboard scripts, prompts, AI-HIVE generation commands, task logs, retry strategy, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can persist an AI-HIVE API key locally and send credentials to a configurable API host.

Mitigation: Use a limited and revocable API key, prefer the default AI-HIVE host, avoid untrusted custom base URLs, and review ~/.ai-hive/config.json for unexpected base_url changes.

Risk: The workflow can upload selected media and submit generation tasks that may incur costs.

Mitigation: Confirm source-media authorization, final prompts, generation mode, routing, and expected cost before submitting jobs; start batch work with a small sample.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-video-batch-production-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include production briefs, storyboard scripts, per-shot prompts, model or routing choices, price snapshots, task IDs, local output paths, retry guidance, and acceptance results.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
