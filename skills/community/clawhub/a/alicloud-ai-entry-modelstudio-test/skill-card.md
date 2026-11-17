## Description:

Run a minimal test matrix for the Model Studio skills that exist in this repo, including image/video/audio, realtime speech, omni, visual reasoning, embedding, rerank, and edit variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run small, bounded validation requests across Alibaba Cloud Model Studio capabilities and record model, request, response, duration, and status results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires third-party SDK installation and Alibaba Cloud API credentials.

Mitigation: Use a controlled environment with a reviewed or pinned dashscope dependency and a limited-scope Alibaba Cloud API key.

Risk: Minimal tests may send prompts, media, or voice samples to Alibaba Cloud and store local evidence files.

Mitigation: Use synthetic or non-sensitive test data; avoid confidential prompts, customer files, regulated data, and real voice samples unless that transfer and retention are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-entry-modelstudio-test)
- [Source list](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and saved evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records capability, sub-skill, model, request summary, result summary, status, and notes for each test.]

## Skill Version(s):

1.0.3 (source: release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
