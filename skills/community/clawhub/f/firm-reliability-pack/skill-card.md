## Description: <br>
Reliability probing and documentation sync pack for gateway health probing, documentation sync validation, channel audit, and ADR generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and platform engineers use this skill to probe gateway health, check documentation-code alignment, audit channel configuration, and generate MADR-format Architecture Decision Records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect or probe gateway environments and configuration files selected by the user. <br>
Mitigation: Use it only with gateway environments and configuration paths that the agent is authorized to inspect. <br>
Risk: The skill depends on mcp-openclaw-extensions >= 3.0.0 for its reliability tools. <br>
Mitigation: Install only after trusting and approving that dependency in the target agent environment. <br>
Risk: Generated ADRs and documentation sync findings may be incomplete or require project-specific judgment. <br>
Mitigation: Review generated ADRs and reliability findings before adopting them in engineering records or deployment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-reliability-pack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-oriented guidance for reliability checks and ADR generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect user-provided configuration paths and gateway environments through the required OpenClaw MCP extension.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
