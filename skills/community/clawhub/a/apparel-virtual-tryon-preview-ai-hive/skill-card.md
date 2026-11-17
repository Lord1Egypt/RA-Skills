## Description:

Turns virtual apparel try-on requests into a Chinese production workflow for generating preview images of authorized people wearing specified garments, including prompts, reference-image strategy, runnable AI-HIVE commands, routing, polling, and delivery checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External apparel merchants, consumer content tools, and outfit operations teams use this skill to create virtual try-on previews, scene and pose variants, prompts, scripts, and quality checklists for ecommerce, advertising, marketing, livestream commerce, and social content. The workflow emphasizes authorized source images, verifiable product facts, price and model checks before paid generation, and reviewable small-batch outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be sent to an arbitrary configured endpoint if AI_HIVE_BASE_URL, --base-url, or ~/.ai-hive/config.json points to an untrusted host.

Mitigation: Use only the default AI-HIVE endpoint, avoid untrusted base-url overrides, inspect ~/.ai-hive/config.json before running, and rotate the API key if it was ever used with an untrusted endpoint.

Risk: Person and garment reference images can contain sensitive or unauthorized material.

Mitigation: Confirm authorization before upload, treat reference images as sensitive, and avoid using the skill for unauthorized impersonation, protected-content replication, or misleading endorsements.

Risk: Generation tasks may incur costs or create misleading commercial claims if submitted without review.

Mitigation: Review prompts, routing mode, model configuration, pricing snapshot, and factual claims before any paid generation; start with a small batch.

## Reference(s):

- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/apparel-virtual-tryon-preview-ai-hive)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline shell commands and generated JSON or image files from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE OpenAPI, upload reference media, submit asynchronous generation tasks, poll task status, and download generated assets after user confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
