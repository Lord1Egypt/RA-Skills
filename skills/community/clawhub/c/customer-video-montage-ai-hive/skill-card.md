## Description:

Helps ecommerce brands, community operators, and user-content teams turn authorized customer testimonial footage into reviewable montage plans, editing commands, AI-HIVE generation tasks, subtitles, brand packaging, and multi-length deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, marketing, and content teams use this skill to plan and execute authorized customer-video montage workflows for ads, social content, product showcases, and campaign assets. It emphasizes provenance, source authorization, factual claims review, deterministic local video edits, and optional AI-HIVE media generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles AI-HIVE API credentials and can send them to a configured API endpoint.

Mitigation: Install only when the AI-HIVE endpoint configuration is trusted, keep API keys out of logs and shared configs, and do not override the base URL unless the operator controls and trusts that server.

Risk: Local ffmpeg editing commands can overwrite existing output files.

Mitigation: Use fresh output filenames or backups before running editing helpers, and review generated commands before execution.

Risk: AI-HIVE image or video generation may submit paid asynchronous tasks.

Mitigation: Confirm prompts, model routing, pricing snapshots, and task parameters before submission, and use a small sample before batch generation.

Risk: Customer footage, product claims, likenesses, music, usernames, and order details may carry authorization, privacy, or platform-compliance obligations.

Mitigation: Use only authorized source material, mark unverified claims for review, and keep source, consent, model, parameter, task, and download records with the delivery package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/customer-video-montage-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON records and inline bash or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include video-production briefs, shot lists, prompts, task records, local file paths, model routing choices, and quality checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
