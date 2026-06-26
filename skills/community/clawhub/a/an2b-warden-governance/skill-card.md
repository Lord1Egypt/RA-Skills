## Description: <br>
War/Den Governance evaluates OpenClaw bot actions against local or enterprise policies before execution and records decisions in governed audit and memory stores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to add policy checks, review gates, and audit trails to OpenClaw agents before actions such as deletion, code execution, API calls, and payments proceed. It supports local community mode and optional enterprise integrations for cloud governance and memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records action context and errors in local audit and memory stores. <br>
Mitigation: Review the data passed to OpenClaw actions and configure retention, storage paths, and access controls for the local SQLite audit and memory databases. <br>
Risk: Enterprise mode can transmit action details, memory content, metadata, and errors to Sentinel_OS or EngramPort when API keys are configured. <br>
Mitigation: Use enterprise keys only when cloud processing is intended, treat keys as secrets, and confirm that transmitted data is appropriate for those services. <br>
Risk: Fail-open behavior can allow actions when the governance engine fails. <br>
Mitigation: Keep WARDEN_FAIL_OPEN=false unless an operator explicitly accepts fail-open behavior for the deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jcools1977/an2b-warden-governance) <br>
- [AN2B Technologies](https://an2b.com) <br>
- [War/Den Documentation](https://warden.an2b.com/docs) <br>
- [Sentinel_OS](https://getsentinelos.com) <br>
- [EngramPort](https://engram.eideticlab.com) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance, shell commands, text] <br>
**Output Format:** [Python hook responses, audit records, governed memory entries, and Markdown documentation with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns allow, deny, or review decisions before actions execute; local mode writes SQLite-backed audit and memory records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, pyproject.toml, clawhub.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
