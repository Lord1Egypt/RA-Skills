## Description:

Refreshes the Alibaba Cloud Model Studio models crawl and regenerates derived summaries and skills under `skills/ai/**`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to crawl the Alibaba Cloud Model Studio models page, rebuild structured model summaries, scan skill coverage, and refresh generated AI skills and related documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned remote npm crawler can execute changing third-party code with broad local workspace access.

Mitigation: Review before installing, run only in a constrained workspace, and pin or vendor the crawler dependency before use.

Risk: The release evidence says the skill overstates skill-generation behavior.

Mitigation: Do not rely on generated skill modifications unless that behavior is separately implemented, reviewed, and validated.

## Reference(s):

- [Alibaba Cloud Model Studio Models](https://help.aliyun.com/zh/model-studio/models)
- [Source list](artifact/references/sources.md)
- [ClawHub release page](https://clawhub.ai/cinience/skills/aliyun-modelstudio-crawl-and-skill)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands; generated artifacts include Markdown reports, JSON model lists, and skill files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to Alibaba Cloud documentation and local Node.js/Python tooling; outputs are written under `output/` and `skills/ai/**`.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
