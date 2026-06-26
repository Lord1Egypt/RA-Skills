## Description: <br>
Validate JSON syntax and structure using the Expanso Edge pipeline in CLI or MCP server modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to validate JSON strings or files locally, including API responses, pre-commit checks, CI/CD validation, and data ingestion checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MCP mode starts an HTTP endpoint that listens on all interfaces by default and has no artifact-level authentication. <br>
Mitigation: Run MCP mode only on trusted machines, or restrict the bind address and firewall access before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-json-validate) <br>
- [Publisher profile](https://clawhub.ai/user/aronchick) <br>
- [Expanso](https://expanso.io) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON validation result with validity, error, parsed content, stats, and metadata fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally without API calls; MCP mode can expose an HTTP validation endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
