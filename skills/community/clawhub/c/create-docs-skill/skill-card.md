## Description:

Use when creating an LLM skill from a documentation website URL -- component libraries, API references, framework guides, or when asked to "create a skill from docs", "scrape docs into a skill", "build a skill for this library".

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufengsheng](https://clawhub.ai/user/wufengsheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn documentation websites into reusable LLM skills. It guides site exploration, scraping fallback handling, reference splitting, SKILL.md slimming, llms.txt generation, directory flattening, and packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can generate files, package skills, and modify or merge with existing same-topic skills.

Mitigation: Review the target directory and approve changes before cleanup, merge, or packaging steps are executed.

Risk: Documentation scraping and fallback collection can pull in incomplete, stale, or irrelevant source material.

Mitigation: Validate scraped content, generated references, llms.txt coverage, and final package quality before deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wufengsheng/skills/create-docs-skill)
- [Publisher profile](https://clawhub.ai/user/wufengsheng)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, directory layouts, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance for creating, optimizing, and packaging documentation-derived agent skills.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
