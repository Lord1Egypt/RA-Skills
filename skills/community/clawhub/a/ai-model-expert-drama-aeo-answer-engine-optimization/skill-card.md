## Description:

AI大模型专家｜AEO 答案引擎优化 helps brand, content, short-drama, e-commerce, marketing, and AI-search teams turn goals into actionable plans, evidence fields, generation tasks, and AI-HIVE media workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, short-drama and comic-drama creators, e-commerce teams, marketing teams, and AI-search operators use this skill to plan AEO-ready answer structures, source fields, production blueprints, and AI-HIVE image or video generation tasks. It supports repeatable media and answer-engine workflows while reminding users not to assume third-party model indexing, ranking, or citation outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API keys can be read from command-line arguments, environment variables, or a local config file, and bearer tokens can be sent to a configured base URL.

Mitigation: Use a dedicated low-privilege AI-HIVE API key, keep it out of public files and screenshots, avoid overriding the default base URL unless the endpoint is trusted, and rotate the key if exposed.

Risk: The scripts can upload local media and download generated outputs through AI-HIVE workflows.

Mitigation: Review upload and download commands before running them, confirm that source media is authorized for use, and inspect generated outputs for factual accuracy, identity, copyright, and platform-safety issues.

Risk: AEO and AI-search outputs can be mistaken for guaranteed ranking, indexing, or citation results.

Mitigation: Treat generated answer structures and visibility records as planning artifacts, validate claims against user-confirmed sources, and retest across models over time.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-aeo-answer-engine-optimization)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON blueprints and AI-HIVE media generation tasks when the user runs the included scripts.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
