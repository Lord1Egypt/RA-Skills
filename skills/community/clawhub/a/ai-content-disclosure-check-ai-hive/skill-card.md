## Description:

This skill helps advertising, platform, legal, brand, and AI creation teams review AI-generated content disclosure needs and produce disclosure elements, labeling placement, metadata records, pre-release checklists, and optional AI-HIVE media-generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, brand legal teams, content platforms, advertisers, and AI creation teams use this skill to turn AI-generated content disclosure requirements into reviewable workflows, checklists, metadata records, and remediation plans. When media generation is needed, it can prepare AI-HIVE commands for model configuration lookup, upload, routing, task polling, and download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines disclosure checking with broad AI media generation, transfer, credential storage, and download behavior.

Mitigation: Install it only when an AI-HIVE media-generation workflow is intended, and review generated commands and task parameters before running them.

Risk: API credentials and custom service endpoints can expand exposure if reused broadly or pointed at untrusted infrastructure.

Mitigation: Use a dedicated AI-HIVE API key and avoid custom base URLs unless they are fully trusted.

Risk: Media uploads may expose sensitive, private, copyrighted, or otherwise unauthorized assets.

Mitigation: Upload only authorized, non-sensitive media and keep human review for legal, privacy, brand, and platform-rule questions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-content-disclosure-check-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files, runnable Python and shell command examples, and optional media-generation task records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE routing mode, model, pricing snapshot, taskId, task status, file locations, and review checklist details when generation tasks are used.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
