## Description: <br>
CLI for AI agents to look up country information using the REST Countries API without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and their users use this skill to answer country reference questions, search countries by name, capital, code, or region, and produce formatted country summaries from public REST Countries data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Country lookup queries are sent to restcountries.com. <br>
Mitigation: Use the skill only for public country reference lookups and avoid entering sensitive or private text as search input. <br>
Risk: Installation guidance involves cloning or symlinking an external CLI. <br>
Mitigation: Verify the external repository and local script contents before installing, cloning, or symlinking the CLI. <br>


## Reference(s): <br>
- [Countries on ClawHub](https://clawhub.ai/jeffaf/countries) <br>
- [REST Countries API](https://restcountries.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output with country summaries and detailed records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public REST Countries API responses; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
