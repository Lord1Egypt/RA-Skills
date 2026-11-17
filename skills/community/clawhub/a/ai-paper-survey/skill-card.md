## Description:

Conducts structured AI paper surveys using alphaXiv MCP tools, user research interests, recent-paper search, innovation-tier classification, impact analysis, and Markdown report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haataa](https://clawhub.ai/user/haataa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research-focused agent users use this skill to survey recent AI papers, screen candidate papers by relevance and innovation tier, assess top candidates, and produce a structured literature-review report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read matching research-keyword files from the current working directory and create a report file there.

Mitigation: Run it in workspaces where those files are intended for the assistant, and check the generated report filename when overwrite behavior matters.

Risk: Paper screening, tier classification, and impact summaries can be incomplete or misleading if search results, abstracts, full-text retrieval, or impact analysis are incomplete.

Mitigation: Review the selected papers, source links, and final recommendations before using the report for research or business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haataa/skills/ai-paper-survey)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with paper classifications, summaries, impact notes, recommendations, and trend observations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a topic- and date-named Markdown report in the current working directory.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
