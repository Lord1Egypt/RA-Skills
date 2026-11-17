## Description:

Bilibili Comment helps an agent retrieve first-level comments from a Bilibili video or BV ID, summarize sentiment across positive, negative, demand, and competitor dimensions, and generate an offline HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessdy](https://clawhub.ai/user/jessdy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, brand operators, content planners, and product managers use this skill to inspect Bilibili video comments, monitor audience sentiment, identify user needs, and prepare shareable HTML comment reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends queried Bilibili video IDs and comment metadata to yige.zone using a Yige API key.

Mitigation: Use only with data you are comfortable sending to the Yige service, keep the API key in environment configuration, and revoke or rotate the key if exposure is suspected.

Risk: Generated HTML reports may include attacker-influenced source video, API response, or analysis content.

Mitigation: Treat generated reports as untrusted files, avoid sharing or opening reports from untrusted inputs, and review report content before distribution.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/jessdy/yige-skills/tree/main/skills/bilibili-comment)
- [Core workflow](references/core_workflow.md)
- [Yige Hub API keys](https://yige.zone/settings/api-keys?source=github)
- [Yige data platform](https://yige.zone/)
- [ClawHub skill page](https://clawhub.ai/jessdy/skills/bilibili-comment-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with tables and analysis summaries, JSON script output, and generated HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YIGE_API_KEY environment variable; each script call retrieves one page of up to 20 first-level comments.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
