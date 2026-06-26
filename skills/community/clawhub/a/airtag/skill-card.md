## Description: <br>
Give your agent controlled access to all AirTags in your Apple account to locate items, run diagnostics, and recover setup failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to let an agent assist with AirTag and Find My workflows, including item location, account-access setup, connection diagnostics, battery maintenance, and unknown-AirTag safety handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle sensitive location and Apple account workflows. <br>
Mitigation: Require explicit user confirmation before location access, connector actions, or writing local AirTag notes. <br>
Risk: Programmatic API Mode depends on unofficial private-protocol tooling. <br>
Mitigation: Prefer Direct App Control or Shared Link Mode when possible, and use Programmatic API Mode only when the user already trusts and manages the connector outside the skill. <br>
Risk: Unknown-AirTag alerts can indicate a personal safety issue. <br>
Mitigation: Prioritize immediate safety, avoid speculative attribution, and switch to the anti-stalking safety workflow when tracking concerns appear. <br>


## Reference(s): <br>
- [ClawHub AirTag Release](https://clawhub.ai/ivangdavila/airtag) <br>
- [AirTag Skill Homepage](https://clawic.com/skills/airtag) <br>
- [iCloud Find My](https://www.icloud.com/find) <br>
- [Find My Shared Item Access](https://find.apple.com) <br>
- [Access Connectors](artifact/access-connectors.md) <br>
- [Recovery Playbook](artifact/recovery-playbook.md) <br>
- [Anti-Stalking Safety](artifact/anti-stalking-safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with structured checklists, connector setup steps, and local note templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before connector actions, location access, or local logging.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
