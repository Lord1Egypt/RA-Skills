## Description:

Generates API test design matrices from OpenAPI or Swagger specifications, combining scripted constraint extraction with agent review of natural-language descriptions for prioritized cases, response assertions, pagination checks, and CRUD lifecycle coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujianyeey-oss](https://clawhub.ai/user/liujianyeey-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and API maintainers use this skill to analyze OpenAPI or Swagger specifications and produce structured test case matrices for interface coverage review. It is aimed at spec-first API testing workflows that need required-field, boundary, enum, authentication, pagination, response assertion, and CRUD-chain coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or untrusted API specification may exploit file-scope weaknesses to read local YAML-like files or write generated YAML outside the selected output directory.

Mitigation: Use the skill only with trusted specifications, run it in a disposable working directory, and review generated file paths before using the outputs.

Risk: Generated LLM review prompts can carry prompt-injection content from API descriptions into later agent workflows.

Mitigation: Inspect generated prompts before reuse and avoid sending them to agents with file, shell, or network tools unless containment and prompt-injection controls have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujianyeey-oss/skills/api-case-gen)
- [Publisher profile](https://clawhub.ai/user/liujianyeey-oss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown test matrices and optional YAML configuration with inline shell and Python command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include P0/P1/P2 priority labels, response assertions, CRUD chain summaries, coverage statistics, fallback review items, and [AI-review] case markers.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter reports 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
