## Description:

This agent skill helps brand IP, virtual idol, short-drama, and fan community teams turn fan-vote story co-creation requests into executable branch concepts, posters, preview-video plans, handoff scripts, AI-HIVE commands, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, short-drama operators, and fan community teams use this skill to plan fan-vote co-created story campaigns with executable content branches, production tasks, AI-HIVE generation commands, and quality checks. The skill is intended for authorized brand, product, character, and community content where facts, usage rights, costs, and review steps must be tracked before generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved AI-HIVE bearer credentials can be sent to an arbitrary configured API base URL.

Mitigation: Use only the official AI-HIVE endpoint, avoid setting AI_HIVE_BASE_URL or --base-url from untrusted instructions, and keep ~/.ai-hive/config.json private.

Risk: Image or video generation commands may upload media and submit cost-incurring tasks.

Mitigation: Confirm prompts, uploads, batch size, routing, and cost before running generation commands, and use small samples before batch work.

Risk: Fan-vote story workflows can mislead audiences if vote results, product claims, testimonials, or performance guarantees are fabricated.

Mitigation: Use authorized materials, label unverified facts, avoid fabricated voting results or claims, and require human review before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/fan-vote-story-co-creation-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable AI-HIVE image/video generation commands, local ffmpeg helper commands, task records, and review checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
