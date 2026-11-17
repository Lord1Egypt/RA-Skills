## Description:

Query Apple Developer Documentation, APIs, and WWDC videos (2014-2025). Search SwiftUI, UIKit, Objective-C, Swift frameworks and watch sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to find Apple platform documentation, inspect framework symbols and API relationships, check platform compatibility, browse sample code, and locate WWDC session material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The doc command can fetch arbitrary web URLs, which may expose sensitive network locations when run in privileged or internal environments.

Mitigation: Run the skill in a restricted network context and allow only Apple documentation paths or trusted Apple hosts for documentation fetches.

Risk: Fetched documentation and transcript content may be incomplete, outdated, or unavailable from upstream sources.

Mitigation: Verify important API guidance against Apple Developer Documentation before using it for release-critical decisions.

## Reference(s):

- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [Apple Developer](https://developer.apple.com/)
- [Apple Docs MCP Server](https://github.com/kimsungwhee/apple-docs-mcp)
- [ClawHub Skill Page](https://clawhub.ai/thesethrose/skills/apple-docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-formatted CLI text and JSON for data-oriented commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include documentation links, framework names, platform compatibility summaries, WWDC metadata, transcript excerpts, and sample-code references.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
