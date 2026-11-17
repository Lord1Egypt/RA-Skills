## Description:

Meta-skill for iterative, hypothesis-driven deep research using deepresearchwork, tavily-search, literature-search (Semantic Scholar mapping), and perplexity-deep-search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

Developers, analysts, and researchers use this skill to run scoped, multi-round research that combines web, academic, and contradiction analysis. It produces a footnoted, scientific-style Markdown report with explicit methodology, limitations, confidence, and unresolved conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses unpinned ClawHub installer commands and a bulk update that can change unrelated installed skills.

Mitigation: Pin and review the ClawHub CLI and each required skill before installation, avoid `update --all`, and install in an isolated environment when possible.

Risk: The workflow depends on Tavily and Perplexity credentials and external upstream skills, so missing credentials, rate limits, or tool unavailability can stop or narrow research.

Mitigation: Run credential and tool preflight checks before research, use restricted API keys, and disclose incomplete evidence when a required source layer is unavailable.

## Reference(s):

- [Deep Researcher ClawHub page](https://clawhub.ai/h4gen/skills/deep-researcher)
- [ClawHub homepage](https://clawhub.ai)
- [Inspected upstream skills](references/inspected-skills.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Scientific-style Markdown report with footnotes and optional shell commands for setup or evidence retrieval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY and PERPLEXITY_API_KEY plus local installation of the referenced upstream ClawHub skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
