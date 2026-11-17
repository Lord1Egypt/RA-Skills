## Description:

Geo Citability analyzes web page content to estimate how likely AI systems are to cite or quote passages and produces a 0-100 citability score with rewrite suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content strategists, and SEO/GEO practitioners use this skill to analyze a web page's structure, fact density, self-containment, and answer-first formatting. The skill produces a markdown report with section scores and concrete rewrite recommendations for improving AI citability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches web page content from a user-specified target URL.

Mitigation: Confirm the URL before analysis and avoid sending private, sensitive, or access-controlled page content unless that access is intended.

Risk: The skill writes a local GEO-CITABILITY-SCORE.md report that could overwrite an existing file with the same name.

Mitigation: Ask the agent to confirm the output path and check for an existing report before writing.

Risk: The artifact includes optional Bash examples for an installed seogeo CLI.

Mitigation: Allow Bash only when CLI execution is intentionally requested; otherwise use the skill for guidance and markdown report generation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with scoring tables, prioritized rewrite suggestions, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local GEO-CITABILITY-SCORE.md report for the analyzed page.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
