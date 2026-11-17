## Description:

YouTube search and transcript extraction. No API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[of-arte](https://clawhub.ai/user/of-arte)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use ClawVoyant to search YouTube and retrieve video transcripts inside OpenClaw or MCP-enabled workflows without configuring API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and video IDs are sent to external services.

Mitigation: Avoid submitting sensitive queries or private video identifiers unless external-service sharing is acceptable.

Risk: Dependency and result-volume controls may change runtime behavior or resource use.

Mitigation: Pin dependency versions, review updates before deployment, and bound max_results in production configurations.

Risk: The install command may start the server instead of only installing dependencies.

Mitigation: Review the install command in a test environment before enabling the skill for agents.

## Reference(s):

- [ClawVoyant ClawHub Skill Page](https://clawhub.ai/of-arte/skills/claw-voyant)
- [Publisher Profile](https://clawhub.ai/user/of-arte)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text and Markdown-compatible tool responses containing search results, video URLs, descriptions, transcripts, or error messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and transcript retrieval depend on external YouTube, DuckDuckGo, and transcript-service availability.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
