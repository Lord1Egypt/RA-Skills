## Description:

This skill helps clothing brands, cross-border apparel sellers, and AI model content teams turn virtual try-on video requests into Chinese production workflows, prompts, runnable AI-HIVE commands, task records, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams, ecommerce operators, and developers use this skill to plan and run virtual apparel try-on videos with authorized product and person references. It produces a reviewable brief first, then can help submit AI-HIVE video generation tasks, poll results, download outputs, and check platform-ready edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send an AI-HIVE API key to a custom API endpoint when --base-url or AI_HIVE_BASE_URL is set.

Mitigation: Use the default AI-HIVE endpoint unless the destination is fully trusted, and use a spend-limited or revocable API key.

Risk: Video and image generation tasks may be billable.

Mitigation: Confirm prompts, mode, routing, and generation parameters before submitting tasks, and start with small samples for batch work.

Risk: Generated try-on visuals may overstate fit, fabric behavior, product facts, endorsements, or platform performance.

Mitigation: Require human review of product facts, authorization, claims, and final media before publication.

Risk: Installing and running the helper scripts adds local Python dependencies and invokes external services.

Mitigation: Install dependencies in an isolated environment with pinned packages where possible and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/avatar-try-on-video-ai-hive)
- [AI-HIVE chat and API key page](https://ai-hive.iclip.cn/chat)
- [AI-HIVE default API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, JSON task records, and checklist text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local generated files such as blueprint JSON, downloaded media paths, task IDs, model routing mode, and price snapshots.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
