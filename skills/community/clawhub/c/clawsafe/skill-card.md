## Description: <br>
Multi-layer security detector for AI agents that blocks prompt injection, jailbreak, XSS, SQL injection, API key leaks, supply chain attacks, and deployment vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SilverTime](https://clawhub.ai/user/SilverTime) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use ClawSafe to scan user input and code-like content before it reaches an AI agent, blocking detected prompt attacks, web payloads, credential leaks, supply chain patterns, and deployment-sensitive disclosures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default whitelist can allow unsafe prompts to bypass detection. <br>
Mitigation: Review or remove the default whitelist entries before installation, especially debug, dev, sandbox, admin, and system entries. <br>
Risk: A pattern-based security filter can miss or misclassify adversarial inputs. <br>
Mitigation: Treat ClawSafe as a defense-in-depth control and keep human review, logging review, and upstream agent safeguards in place for sensitive deployments. <br>


## Reference(s): <br>
- [ClawSafe ClawHub listing](https://clawhub.ai/SilverTime/clawsafe) <br>
- [ClawSafe metadata homepage](https://github.com/openclaw/clawSafe) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Configuration, Guidance] <br>
**Output Format:** [JSON scan results and localized text block messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan results include safe status, detected threats, confidence, and scanned layers.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and _meta.json; SKILL.md and package.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
