## Description:

This skill helps ecommerce merchants, category operators, and live-commerce selection teams turn candidate product data into Chinese decision workflows, scoring tables, risks, content difficulty assessments, validation plans, runnable AI-HIVE commands, and deliverable content while avoiding unsupported real-time market claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and marketing teams use this skill to evaluate candidate SKUs from user-provided facts, plan platform-ready product content, and create reviewable image or video generation tasks. Developers and operators can also use its scripts to create briefs, upload authorized media, query AI-HIVE model configuration and pricing snapshots, submit generation jobs, poll task status, and download outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses a persistent local AI-HIVE API key for workflows that may incur generation charges.

Mitigation: Use trusted installations only, keep API keys out of files, logs, screenshots, and version control, and require review of prompts, routing, model choice, and pricing snapshots before submitting generation jobs.

Risk: The scripts can upload local media and download generated outputs.

Mitigation: Upload only media the user has rights to use, avoid sensitive or unauthorized content, and review downloaded outputs before publication or deployment.

Risk: Endpoint scoping is weak if AI_HIVE_BASE_URL or --base-url is changed from the default official endpoint.

Mitigation: Keep the default official AI-HIVE endpoint unless the alternate server is fully trusted and approved.

Risk: Generated ecommerce guidance or content could include unsupported claims, copied protected material, or misleading endorsements.

Mitigation: Base decisions only on user-provided facts, verify claims and source rights, avoid unauthorized copying or fake testimonials, and run human review before commercial use.

## Reference(s):

- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ecommerce-product-selector-ai-hive)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON files or downloaded media outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use AI-HIVE API calls for media upload, model and pricing lookup, billable image or video generation, asynchronous task polling, and downloads after user review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
