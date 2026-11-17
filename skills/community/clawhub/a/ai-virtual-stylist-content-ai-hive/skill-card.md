## Description:

This skill helps apparel brands, buyer shops, stylists, creators, and private-domain operators turn real SKU inputs, product images, audience details, scenarios, seasons, and price ranges into virtual-stylist outfit concepts, lookbook image tasks, short-video scripts, promotional copy, runnable AI-HIVE commands, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External apparel marketers, ecommerce operators, stylists, and content teams use this skill to plan and generate AI-assisted virtual-buyer outfit content from authorized real product inputs. It supports production briefs, platform-ready scripts and prompts, AI-HIVE image or video generation commands, task records, and acceptance checks before paid generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can send an AI-HIVE API key to a configurable server.

Mitigation: Use only a trusted AI-HIVE endpoint, avoid custom base URLs unless the endpoint is fully trusted, and store only an API key that is acceptable for local use.

Risk: Generated media and uploaded reference assets may leave the local machine during AI-HIVE API workflows.

Mitigation: Use non-sensitive, authorized product and reference assets, and review prompts and uploads before submitting generation tasks.

Risk: The workflow advertises real-SKU boundaries, but the security evidence says the scripts do not enforce those limits.

Mitigation: Manually verify that prompts, task records, and outputs use only authorized real products and do not make unsupported claims before publishing or paid generation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/ai-virtual-stylist-content-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON, image, or video files produced by the helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task IDs, model and pricing snapshots, downloaded media file paths, and verification checklists.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
