## Description:

Helps e-commerce merchants, brand teams, and ad teams turn authorized avatar and product references into reviewable product-holding video plans, prompts, AI-HIVE generation commands, task records, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce merchants, brand teams, and advertising producers use this skill to plan and generate avatar product-holding videos from authorized people, product, and brand assets. The skill supports production briefs, storyboard prompts, AI-HIVE media upload and video generation commands, task tracking, downloads, and quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API keys could be exposed or routed to an untrusted endpoint if users pass credentials on shared machines or configure an untrusted base URL.

Mitigation: Treat API keys like passwords, avoid --api-key on shared machines, keep config files private, and use only trusted AI-HIVE endpoints.

Risk: Generation commands may upload user media or incur charges.

Mitigation: Review final prompts, model choice, routing mode, pricing snapshot, media paths, and task parameters before execution; use a small sample before batch generation.

Risk: Avatar product videos can misrepresent likeness rights, brand authorization, product claims, or endorsements.

Mitigation: Confirm rights to all reference assets, mark unverified claims as pending review, and require human review for likeness, product accuracy, brand use, and platform compliance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/avatar-holding-product-video-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON blueprints, downloaded media files, AI-HIVE task IDs, and acceptance checklists when the user confirms potentially billable generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
