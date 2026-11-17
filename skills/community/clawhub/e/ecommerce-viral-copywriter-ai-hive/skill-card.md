## Description:

Generates Chinese ecommerce campaign briefs, selling-point hierarchies, titles, short-video scripts, image prompts, detail-page copy, CTAs, runnable AI-HIVE commands, and review checklists from product facts, audience needs, platform constraints, and authorized assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, ad buyers, livestream teams, and content editors use this skill to turn product facts and campaign constraints into Chinese marketing copy, media-generation tasks, runnable AI-HIVE commands, and acceptance checks. It is suited for product pages, ads, social commerce, short videos, and seeding workflows where claims, assets, costs, and platform fit need review before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send an AI-HIVE API key to an arbitrary configured endpoint if AI_HIVE_BASE_URL or --base-url is changed.

Mitigation: Use only trusted AI-HIVE endpoints, avoid custom base URLs unless they are fully trusted, and rotate credentials if a key may have been exposed.

Risk: Generation commands can upload prompts or media and may incur costs.

Mitigation: Confirm prompts, media authorization, routing mode, model selection, and expected costs before submitting generation tasks; use small samples before batch runs.

Risk: Ecommerce copy can make unsupported claims or reuse protected reference material too closely.

Mitigation: Keep a fact base for claims, verify product evidence and asset rights, and transform references at the abstract structure level instead of copying protected expression.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ecommerce-viral-copywriter-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON briefs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task identifiers, routing choices, pricing snapshots, downloaded file paths, and human review checklists when generation commands are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
