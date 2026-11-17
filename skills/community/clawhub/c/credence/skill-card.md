## Description:

Check any MCP server or AI tool against the Credence trust registry before installing it. Scores security, provenance, and behavioral risk on a 0-100 scale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pestafford](https://clawhub.ai/user/pestafford)

### License/Terms of Use:


## Use Case:

Developers and agent users use Credence before installing or connecting MCP servers and AI tools to check registry scores, verdicts, provenance, and behavioral risk guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credence scores are based on mutable registry data and may change after a user checks a package or server.

Mitigation: Treat the score as advisory, review the current registry details, and confirm before installing or connecting an MCP server.

Risk: Loose name, URL, or partial-match lookup can identify the wrong package or repository.

Mitigation: Verify the exact package name, repository URL, publisher, and registry entry before acting on an APPROVED or CONDITIONAL verdict.

## Reference(s):

- [Credence registry](https://credence.securingthesingularity.com/registry.html)
- [Credence registry index](https://raw.githubusercontent.com/pestafford/credence-registry/main/registry/index.json)
- [Credence methodology FAQ](https://credence.securingthesingularity.com/faq.html)
- [Credence skill page](https://clawhub.ai/pestafford/skills/credence)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and concise trust recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports a trust score, verdict, scan timestamp, registry link, and recommended install posture when a registry match is found.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
