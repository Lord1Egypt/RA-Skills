## Description: <br>
Helps users with flexible travel dates compare FlyAI flight prices across a date range and produce a low-price calendar with recommended departure options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find cheaper flight departure dates by scanning route prices, comparing round-trip combinations, and presenting calendar-style recommendations with booking links when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow installs or upgrades a global FlyAI CLI from npm with an unpinned @latest version. <br>
Mitigation: Review the package before use, prefer a pinned version, and avoid sudo or global installation when a local or sandboxed install is available. <br>
Risk: The workflow instructs agents to bypass TLS certificate verification with NODE_TLS_REJECT_UNAUTHORIZED=0. <br>
Mitigation: Do not disable TLS verification in normal use; investigate certificate failures and use trusted network and certificate settings instead. <br>
Risk: The skill may save personal travel preferences in Qoder Memory or ~/.flyai/user-profile.md. <br>
Mitigation: Ask for user confirmation before saving preferences, store only necessary travel profile details, and allow the user to review or decline persistence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-flight-calendar) <br>
- [Core workflow](reference/core-workflow.md) <br>
- [Flight search reference](reference/search-flight.md) <br>
- [Examples](reference/examples.md) <br>
- [User profile storage](reference/user-profile-storage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with calendar blocks, recommendation tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight prices are time-sensitive and should be presented as reference prices with the retrieval time when possible.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
