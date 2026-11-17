## Description:

Work with Immich photo library via MCP (claw2immich) - search photos by people, dates, locations, albums. Download assets via shared links. Handles multi-person search, CLIP smart search, and metadata queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeru](https://clawhub.ai/user/joeru)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an OpenClaw agent search, view, and retrieve photos from an Immich photo library through the claw2immich MCP server. It supports people, date, location, album, and natural-language smart search workflows, plus thumbnail display and asset download guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive personal media through shared links, generated photo URLs, or thumbnail/base64 responses.

Mitigation: Treat returned links and image data as sensitive, share them only with intended recipients, and prefer authenticated Immich links when unauthenticated shared links are not required.

Risk: A broadly configured Immich MCP server can give the agent more photo-library authority than a search or viewing workflow needs.

Mitigation: Use the smallest useful IMMICH_PROFILE, prefer read_only for search and viewing, avoid full_scope unless admin functions are explicitly needed, and check available tools with tool_access_report.

Risk: Example download scripts may handle filenames and JSON arguments unsafely in some environments.

Mitigation: Review and harden the example scripts before running downloads, especially when filenames, search terms, or server URLs may come from untrusted input.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/joeru/skills/claw2immich)
- [claw2immich MCP Server](https://github.com/JoeRu/claw2immich)
- [Immich](https://immich.app)
- [Immich API documentation](https://immich.app/docs/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, MCP call examples, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include short-lived shared-link URLs, direct Immich URLs, or base64 thumbnail data when the configured MCP server returns them.]

## Skill Version(s):

1.0.0 (source: server release, skill.json, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
