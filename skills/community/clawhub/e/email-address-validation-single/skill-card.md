## Description: <br>
Email Address Validation Single helps agents validate one email address through AgentPMT-hosted remote calls, checking syntax, DNS/MX records, SMTP mailbox status, disposable or role-based addresses, spam traps, and typo suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to validate individual email addresses before signups, contact imports, marketing sends, CRM updates, lead qualification, or checkout workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email addresses are sent to AgentPMT for validation, and each validation may consume account credits. <br>
Mitigation: Configure agents to use the skill only when the user clearly requests email validation or an established workflow requires it. <br>
Risk: Broad trigger terms could cause unintended validation requests if an agent routes too aggressively. <br>
Mitigation: Restrict activation to explicit single-address validation tasks and review routing behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/email-address-validation-single) <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/email-address-validation-single) <br>
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown instructions with JSON call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to submit a single email address and optional validation settings, then handle JSON validation results from AgentPMT.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
