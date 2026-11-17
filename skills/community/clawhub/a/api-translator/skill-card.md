## Description:

Translates API documentation from URLs, HTML, JSON responses, or Markdown into Traditional Chinese using Taiwan terminology while preserving code and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dolphins1123](https://clawhub.ai/user/dolphins1123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to translate public or approved API documentation into Traditional Chinese for Taiwan audiences while preserving Markdown structure and code samples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary API documentation URLs and place fetched content into an LLM context.

Mitigation: Use only public or explicitly approved API documentation URLs, and avoid internal, authenticated, or sensitive documentation unless the user accepts that exposure.

Risk: The release evidence reports incomplete helper scripts rather than full translators.

Mitigation: Review helper script behavior before installing or relying on automation, and treat script output as translation prompts or helper output rather than a complete production workflow.

Risk: Server-resolved provenance is unavailable for this version.

Mitigation: Do not infer GitHub or package provenance from the skill text; verify the publisher and source through ClawHub before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dolphins1123/skills/api-translator)
- [OpenAI API reference example](https://platform.openai.com/docs/api-reference/introduction)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or text translation guidance with preserved code blocks and optional helper command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process fetched API documentation content up to the helper script fetch limit; output format options include markdown, json, and txt.]

## Skill Version(s):

1.1.0 (source: frontmatter, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
