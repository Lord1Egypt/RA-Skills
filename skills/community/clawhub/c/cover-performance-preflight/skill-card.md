## Description:

Reviews an existing video, social, article, or podcast cover and provides practical improvements, with optional topic benchmarks and visual candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content teams use this skill to review an existing cover before publication and get practical revision directions. They can optionally compare it with public results on supported platforms and request visual candidates after paid confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because it reports broad shared account permissions and automatic installation data reporting beyond the cover-review purpose; the verdict does not establish malicious intent.

Mitigation: Consider not installing until the permissions and reporting are narrowed or clearly disclosed, and review the account access and installation data involved.

Risk: The security scan is partial because some referenced service operations could not be resolved to bundled files, leaving the evidence incomplete.

Mitigation: Review the unresolved operations and obtain a complete security assessment before relying on the scan.

Risk: The optional update command may not be pinned to a reviewed version.

Mitigation: Keep updates optional and update only to a version that has been reviewed.

## Reference(s):

- [Cover Improvement Preflight on ClawHub](https://clawhub.ai/beatra-ai/skills/cover-performance-preflight)
- [Beatra skill information](https://beatra.ai/skills/cover-performance-preflight)
- [Cover preflight workflow](artifact/references/workflow.md)
- [Same-topic baseline lookup](artifact/references/baseline-lookup.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Bundled MCP client diagnostics](artifact/references/mcp-connection.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance, Image files]

**Output Format:** [Qualitative review card and revision guidance; optional benchmark findings and visual candidate images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No numerical performance score, CTR forecast, or click guarantee. Optional baseline lookup and image generation require separate paid confirmations.]

## Skill Version(s):

0.2.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
