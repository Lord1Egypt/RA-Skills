## Description:

This skill helps App, SaaS, education, software, and growth teams turn real UI screenshots or recordings into Chinese-language app demo ad plans, scripts, prompts, AI-HIVE video tasks, and acceptance checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing, ecommerce, product, and growth teams use this skill to plan and produce app interface demonstration ads from authorized product facts, UI captures, platform requirements, budget constraints, and CTAs. It supports reviewable briefs, storyboards, prompts, runnable AI-HIVE commands, task records, and final video checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media selected for generation or reference workflows can contain private, copyrighted, or unauthorized material and may be uploaded to AI-HIVE.

Mitigation: Confirm the user has rights to each asset and review exactly which files will be uploaded before running upload or generate commands.

Risk: Generation and upload commands can consume paid credits or trigger billable asynchronous jobs.

Mitigation: Show the final prompt, mode, routing choice, model configuration, and price snapshot before execution, and start with a small sample for batch work.

Risk: API keys can be exposed through logs, files, screenshots, repository commits, or an untrusted custom base URL.

Mitigation: Use placeholders in examples, keep real keys in environment variables or a permission-restricted config file, avoid echoing keys, and rotate any key sent to an endpoint the user does not control.

Risk: Generated ad claims, UI states, performance outcomes, or endorsements can mislead viewers if they are not grounded in verified product facts.

Mitigation: Require real UI captures for key operations, mark unconfirmed claims as pending verification, and reject requests to fabricate product performance, user testimony, rankings, or review outcomes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/app-ui-demo-ad-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, generated JSON files, task records, and checklist text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task IDs, routing choices, model and price snapshots, download locations, and acceptance results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
