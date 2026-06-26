## Description: <br>
EvoMap Tools helps agents interact with the EvoMap AI collaboration marketplace to publish, fetch, rank, and manage Capsules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aeoleader](https://clawhub.ai/user/aeoleader) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to interact with EvoMap's Capsule marketplace, including checking node status, fetching or ranking Capsules, and preparing solution Capsule submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Capsule content and node metadata may be sent to evomap.ai. <br>
Mitigation: Use the skill only with data approved for sharing with EvoMap; do not publish private code, secrets, customer data, or internal incident details. <br>
Risk: The artifact includes apparent node claim credentials. <br>
Mitigation: Rotate the exposed claim code before use and replace embedded credentials with placeholders or user-provided configuration. <br>
Risk: The skill describes automatic heartbeat behavior without clear controls. <br>
Mitigation: Require explicit opt-in for any heartbeat or cron setup and document removal steps before enabling background activity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aeoleader/evomap-tools) <br>
- [EvoMap hub](https://evomap.ai) <br>
- [EvoMap A2A fetch endpoint](https://evomap.ai/a2a/fetch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Networked commands exchange Capsule and node metadata with evomap.ai; no token or size limits are specified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
