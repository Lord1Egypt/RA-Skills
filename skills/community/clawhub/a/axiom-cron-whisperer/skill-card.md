## Description: <br>
Cron expression explainer that translates standard 5-field cron syntax into English or French and helps users document or validate cron expressions without an LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps practitioners, and no-code users use this skill to understand, document, and validate standard cron expressions before relying on scheduled jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill explains and validates standard 5-field cron expressions but does not calculate next run times or support Quartz and other extended cron syntax. <br>
Mitigation: Use it for documentation and basic validation, and use scheduler-specific tooling when next-run timing or extended syntax support is required. <br>
Risk: High-volume or untrusted input could still consume local processing time even though the skill has no network access or credential handling. <br>
Mitigation: Apply normal input length and timeout limits before exposing the helper to untrusted or high-volume use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiom-cron-whisperer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Plain text or JSON cron explanation and validation result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [English or French output; supports standard 5-field cron syntax only.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
