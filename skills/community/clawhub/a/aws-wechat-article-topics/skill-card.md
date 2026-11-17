## Description:

This skill helps WeChat public-account editors and content operators research article topics, generate title candidates and summaries, plan series, and prepare topic handoff files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiworkskills](https://clawhub.ai/user/aiworkskills)

### License/Terms of Use:

MIT-0

## Use Case:

External content editors and operations teams use this skill to select WeChat article topics, research current angles, create title and outline options, and hand selected topics to a writing workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web research may surface stale, incomplete, or misleading material for article planning.

Mitigation: Review cited sources and factual claims before publishing topic cards, summaries, or outlines.

Risk: The skill can read and update article project files such as topic-card.md, research.md, and article.yaml.

Mitigation: Run it only in the intended article workspace and review proposed file changes before accepting them.

Risk: Some workflows depend on companion aws-wechat-article skills and Python helper scripts.

Mitigation: Install the full suite for cross-skill steps and review the helper dependency before running shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiworkskills/skills/aws-wechat-article-topics)
- [AIWorkSkills homepage](https://aiworkskills.cn)
- [wechat-article-skills repository](https://github.com/aiworkskills/wechat-article-skills)
- [Output format](references/output-format.md)
- [Research strategy](references/research-strategy.md)
- [Title presets](references/title-presets.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses and Markdown/YAML project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update topic-card.md, research.md, and article.yaml after user confirmation; requires python3 for helper-script workflows.]

## Skill Version(s):

1.0.25 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
