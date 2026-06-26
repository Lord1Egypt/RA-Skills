## Description: <br>
Validates AI prompts for injection, role overrides, data leaks, or jailbreaks, then decides whether an agent should pass, block, or quarantine the prompt before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jongartmann](https://clawhub.ai/user/jongartmann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill as a prompt-security checkpoint before task execution, sending prompts to Aegis Gate for pass, block, or quarantine decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Every user prompt is sent to the external Aegis Gate service, which may expose secrets, personal data, internal documents, or regulated information included in prompts. <br>
Mitigation: Use the skill only when the Aegis Gate service is trusted for the prompt contents, and avoid sending sensitive or regulated information unless that transfer is approved. <br>
Risk: The external service or network/API errors can block normal agent work through block, quarantine, or fail-secure outcomes. <br>
Mitigation: Plan for human review and fallback procedures when the API blocks, quarantines, or fails during important workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jongartmann/aegis-gate) <br>
- [Aegis Gate live API](https://tower.x-loop3.com) <br>
- [Aegis Gate demo](https://clawtower.x-loop3.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces pass, block, quarantine, or fail-secure guidance based on the external Aegis Gate API response.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
