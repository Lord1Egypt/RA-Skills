## Description:

Turns e-commerce UGC ad requests into Chinese creative angles, human-style scripts, storyboards, product keyframes, AI-HIVE image or video generation tasks, runnable commands, and review checklists grounded in verified product facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce merchants, media buyers, brand content teams, and UGC ad producers use this skill to turn product facts, audience pain points, authorized assets, platform constraints, and budget priorities into production-ready Chinese UGC ad plans and AI-HIVE generation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API client can send the user's bearer token to a custom base URL.

Mitigation: Use the default AI-HIVE endpoint unless the custom endpoint is fully trusted and controlled; keep the API key scoped, rotatable, and out of committed files.

Risk: The skill can upload selected media, submit potentially billable generation tasks, and download generated outputs.

Mitigation: Review prompts, routing mode, model choice, pricing snapshot, media authorization, and generated shell commands before executing tasks, especially batch jobs.

Risk: UGC ad content can become misleading if product claims, testimonials, platform rules, or synthetic-person disclosures are not verified.

Mitigation: Ground claims in provided evidence, mark uncertain facts for review, confirm rights to reference assets, and disclose synthetic people according to platform rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ugc-ad-generator-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files and download generated image or video outputs after user-approved AI-HIVE tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
