## Description: <br>
Guides an agent through a four-role adversarial review process for diagnosing API failures and selecting a practical resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to structure API troubleshooting, compare candidate fixes, and converge on a recommended action when failures involve keys, endpoints, network behavior, or fallback handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials or private endpoint details could be exposed while troubleshooting. <br>
Mitigation: Redact API keys, secrets, and private identifiers before providing configuration details to the agent. <br>
Risk: The workflow can recommend diagnostic or configuration changes that may not match the live environment. <br>
Mitigation: Review the proposed fix and test changes in a controlled environment before applying them to production systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timo2026/auto-skill-20260404-063632) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with code examples and diagnostic checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured troubleshooting recommendations; users should redact API keys and private credentials before sharing configuration details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
