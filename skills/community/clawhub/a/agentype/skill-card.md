## Description:

Agentype analyzes local AI-agent usage metadata, infers a persona from aggregate usage signals, and renders a terminal summary or PNG poster.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyzlmh](https://clawhub.ai/user/cyzlmh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Agentype to understand local AI-agent usage, token patterns, preferred tools, models, and projects through an aggregate persona and usage summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can use an unpinned uvx fallback that fetches and executes agentype-cli from PyPI at runtime.

Mitigation: Prefer a preinstalled or pinned, reviewed agentype-cli version before running the workflow.

Risk: The workflow reads broad local AI-agent usage metadata, including projects, models, tokens, and usage patterns.

Mitigation: Run it only when local usage analysis is intended, and avoid exposing raw session files, prompts, private transcripts, or full JSON unless explicitly needed for debugging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyzlmh/skills/agentype)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Terminal text or Markdown summary, with optional JSON input/output and PNG poster file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes output/agentype.json during the workflow and can optionally write output/agentype.png for chat or gateway environments that display images.]

## Skill Version(s):

0.1.8 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
