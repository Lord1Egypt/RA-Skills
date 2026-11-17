## Description:

Core Researcher helps agents search, analyze, summarize, and structure academic research using the CORE API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bivex](https://clawhub.ai/user/bivex)

### License/Terms of Use:


## Use Case:

Developers, researchers, students, and research support agents use this skill to conduct literature reviews, retrieve academic work through CORE, summarize papers, analyze methodologies, identify research gaps, and format scholarly writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Academic search queries or prompts may expose unpublished sensitive research details, secrets, private participant data, or a CORE API key to CORE.

Mitigation: Pass the CORE API key only at runtime, avoid sensitive or private data in queries, and use an environment variable, command-line argument, or secrets store rather than storing keys in source code.

Risk: Generated academic summaries, citations, or paper metadata may be inaccurate or incomplete.

Mitigation: Independently verify citations, metadata, methodology descriptions, and claims against the source papers before relying on scholarly writing.

## Reference(s):

- [CORE API v3](https://api.core.ac.uk/v3/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and citation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CORE API endpoint patterns, structured paper summaries, literature review outlines, citation formats, and academic writing guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
