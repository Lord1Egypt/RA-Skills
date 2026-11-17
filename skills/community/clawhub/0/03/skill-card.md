## Description:

Analyzes images in local or API mode for content descriptions, object identification, text extraction, and batch review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect individual images or selected image directories, returning descriptions, detected content, and text-like visual details while choosing between local processing and API-backed analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API mode can upload image contents to a third-party model provider.

Mitigation: Use local mode for sensitive images, or use API mode only when third-party upload is acceptable.

Risk: The skill relies on an unbundled parent-directory llm_config module that can affect API key handling and upload destinations.

Mitigation: Bundle or replace llm_config with inert, validated configuration before trusting API keys or uploads.

Risk: Batch mode recursively analyzes images under the selected directory.

Mitigation: Run batch mode only on directories that were intentionally selected and reviewed.

Risk: Dependency ranges can resolve to different package versions over time.

Mitigation: Install in a virtual environment and pin dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/03)
- [Publisher profile](https://clawhub.ai/user/nidhov01)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON-like analysis results, CLI text, and Markdown/Python usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-image analysis returns file metadata and a description; batch mode returns one result per validated image.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
