## Description: <br>
Check any MCP server or AI tool against the Credence trust registry before installing it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pestafford](https://clawhub.ai/user/pestafford) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use Credence before installing MCP servers or AI tools to check public trust-registry scores, verdicts, and recommended next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a third-party public registry when evaluating MCP servers or AI tools. <br>
Mitigation: Use it only when third-party registry lookups are acceptable for the environment. <br>
Risk: Partial name or repository matches and changing registry data can lead to the wrong trust result being used. <br>
Mitigation: Verify the exact server name or repository URL before acting on an approved, conditional, flagged, or rejected verdict. <br>


## Reference(s): <br>
- [Credence Registry](https://credence.securingthesingularity.com/registry.html) <br>
- [Credence Registry Index](https://raw.githubusercontent.com/pestafford/credence-registry/main/registry/index.json) <br>
- [Credence Methodology FAQ](https://credence.securingthesingularity.com/faq.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and trust verdict summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports a 0-100 score, verdict, scan timestamp, registry link, and installation recommendation when a registry match is found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
