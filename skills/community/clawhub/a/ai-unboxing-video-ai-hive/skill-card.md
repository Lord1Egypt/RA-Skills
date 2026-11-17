## Description:

Turns AI unboxing video requests into a reviewable production workflow with unboxing steps, packaging details, shot scripts, AI-HIVE generation commands, video task records, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, e-commerce teams, and developers use this skill to plan and produce product unboxing videos from authorized product and packaging inputs. It produces scripts, prompts, runnable AI-HIVE commands, generated-video task records, and quality checks that help reviewers verify package accuracy and platform fit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API credentials and can store an API key for later CLI use.

Mitigation: Use environment variables or the generated config file with restricted permissions, never paste real keys into prompts or logs, and rotate keys if exposure is suspected.

Risk: The skill can upload selected media to AI-HIVE and submit potentially billable generation jobs.

Mitigation: Review media paths, prompts, model choices, routing mode, and pricing snapshots before generation; start with a small sample before batch work.

Risk: Custom base URLs can route credentials and media to an unintended endpoint.

Mitigation: Keep AI_HIVE_BASE_URL unset unless the endpoint is controlled and trusted, and prefer the documented AI-HIVE API base URL.

Risk: Generated unboxing content may contain inaccurate product, packaging, accessory, price, performance, or endorsement claims.

Mitigation: Require source facts and authorized assets, mark uncertain claims for verification, and compare final frames against the real product and platform requirements before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-unboxing-video-ai-hive)
- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON briefs, AI-HIVE task identifiers, downloaded media file paths, and ffmpeg inspection or editing command output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
