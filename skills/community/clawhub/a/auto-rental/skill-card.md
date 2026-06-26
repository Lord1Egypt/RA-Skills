## Description: <br>
Finds and compares real-time car rental options, including sedans, SUVs, luxury vehicles, insurance options, pickup locations, and booking links through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel users and agents use this skill to search for car rental options, compare available offers, and present bookable results with real-time pricing links. It is intended for rental scenarios such as city pickup, airport pickup, and SUV rentals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run a global flyai CLI dependency. <br>
Mitigation: Install the CLI only from a trusted source and require explicit user approval before installing or executing it. <br>
Risk: Live travel searches may send user trip details to the flyai provider. <br>
Mitigation: Tell users when live lookup is required and avoid submitting sensitive travel details unless they approve. <br>
Risk: The artifact describes persisting raw execution logs locally without clear retention controls. <br>
Mitigation: Disable, delete, or rotate local execution logs unless they are intentionally needed for debugging. <br>


## Reference(s): <br>
- [Auto Rental on ClawHub](https://clawhub.ai/xiejinsong/auto-rental) <br>
- [Parameter and output templates](artifact/references/templates.md) <br>
- [Car rental playbooks](artifact/references/playbooks.md) <br>
- [Fallback handling](artifact/references/fallbacks.md) <br>
- [Execution log schema](artifact/references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and comparison tables with booking links, plus shell commands for flyai CLI execution when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must be based on flyai CLI output and should include bookable detailUrl links when rental options are shown.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
