## Description:

A character-index based string-processing protocol server for test-code generation and data-processing workflows that need precise character positioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find character or substring positions, split text, insert or delete ranges, replace indexed spans, locate regex matches, extract marker-delimited content, count characters, and extract substrings by index ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processed strings are sent to the external Xiaobenyang MCP service.

Mitigation: Use the skill only with non-sensitive text unless the publisher provides acceptable data-handling assurances for secrets, proprietary data, personal data, and regulated content.

Risk: The API key may be stored in a plaintext .env file in the working directory.

Mitigation: Use a scoped or disposable key where possible, restrict local file access, remove the key after use, and rotate it if exposure is suspected.

Risk: The server-side security verdict is suspicious and calls for review before use.

Mitigation: Review the skill, dependencies, and network behavior before deployment, and allow outbound access only to expected Xiaobenyang service endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/char-index)
- [Xiaobenyang API key and service site](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON results summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY credential and sends processed strings to an external authenticated API.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
