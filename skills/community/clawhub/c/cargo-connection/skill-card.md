## Description: <br>
Manage connectors and integrations using the Cargo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cargo-ai](https://clawhub.ai/user/cargo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to list, create, update, remove, and inspect Cargo connectors and integrations, including discovering integration actions for workflow nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide Cargo CLI operations that use account access and third-party integration credentials. <br>
Mitigation: Use it only when managing Cargo connectors intentionally, prefer OAuth or protected configuration over pasted API keys, and verify the authenticated Cargo session before running commands. <br>
Risk: Connector updates or removals can affect workflows that depend on those connectors. <br>
Mitigation: Review connector usage counts and dependent workflows before changing or removing connector instances. <br>


## Reference(s): <br>
- [Cargo Skills Repository](https://github.com/getcargohq/cargo-skills) <br>
- [Connector examples](references/examples/connectors.md) <br>
- [Integration examples](references/examples/integrations.md) <br>
- [Response shapes](references/response-shapes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated Cargo CLI operations that affect connectors and third-party integration credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
