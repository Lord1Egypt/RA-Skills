## Description: <br>
Checks for the March 2026 axios supply chain attack, including malicious axios versions, the plain-crypto-js dropper, RAT artifacts, and recommended remediation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vjumpkung](https://clawhub.ai/user/vjumpkung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and incident responders use this skill to check projects and systems for indicators tied to the March 2026 axios supply-chain compromise and to choose appropriate remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands that can modify packages, remove directories, edit hosts files, or change firewall rules. <br>
Mitigation: Run read-only checks first and require explicit approval before sudo, firewall, hosts-file, npm install, or rm -rf actions. <br>
Risk: Credential rotation and rebuild guidance can disrupt systems if applied without confirming incident scope. <br>
Mitigation: Follow the organization's incident-response process before rotating credentials or rebuilding systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vjumpkung/axios-security-check) <br>
- [StepSecurity Harden-Runner](https://github.com/step-security/harden-runner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with checklists, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an axios security check report with findings, verdict, and recommended actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
