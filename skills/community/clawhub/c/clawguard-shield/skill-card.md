## Description: <br>
ClawGuard Shield v3 provides active defense for prompt injection detection, intent validation, zero-width character detection, and intent integrity verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stardreaming](https://clawhub.ai/user/stardreaming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review user text for prompt injection, role hijacking, jailbreak attempts, hidden encoding, and intent drift before continuing an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may cause the skill to be invoked for ordinary content review when a focused security check was not intended. <br>
Mitigation: Use explicit requests such as security check or prompt-injection analysis, and keep normal proofreading or general content review separate unless that behavior is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stardreaming/clawguard-shield) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown or terminal-style text reports, with optional JSON configuration output for hardening workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes risk scores, threat categories, and recommended handling actions.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
