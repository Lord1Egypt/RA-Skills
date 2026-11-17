## Description:

Find academic papers, studies, and research on a user-specified topic using Exa's research paper category search, then synthesize relevant findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

External users and research-focused agents use this skill to search for academic papers, fetch relevant paper content, and summarize findings for a research question.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive research topics or confidential workspace context may be transformed into Exa queries.

Mitigation: Use the skill only with information that may be shared with Exa, and avoid confidential topics or private workspace context unless disclosure is acceptable.

Risk: The artifact tells agents to read product marketing context even for ordinary literature searches.

Mitigation: Limit context reads to material directly needed for the research task, and avoid loading unrelated local files.

Risk: Shell-style examples include user-supplied topics.

Mitigation: Pass user input as separate command arguments when invoking exa.js, and avoid interpolating raw user text into shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-exa-research-papers)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with paper metadata, links, synthesis notes, and inline shell commands for Exa searches.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes title, authors, year, key findings, relevance, URL, synthesis, research gaps, and suggested follow-up searches.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
