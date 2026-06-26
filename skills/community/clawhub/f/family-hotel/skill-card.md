## Description: <br>
Finds family-friendly hotels with multi-bed rooms, kid-friendly amenities, nearby playgrounds, and family-oriented services using flyai CLI and Fliggy travel data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search for family-oriented hotels, collect destination and date parameters, run flyai hotel searches, and format real-time results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run a third-party npm CLI package on the local system. <br>
Mitigation: Review the flyai CLI package and run it only in a trusted environment before allowing global installation or command execution. <br>
Risk: Travel-search details may be sent to an external travel booking service. <br>
Mitigation: Avoid entering sensitive personal information and confirm the user is comfortable sharing destination, date, budget, and preference details with the travel service. <br>
Risk: Local execution logs may retain raw travel queries. <br>
Mitigation: Limit or disable log persistence where possible, avoid sensitive query content, and review or delete local execution logs after use. <br>
Risk: The skill can produce misleading travel guidance if it answers without live CLI results. <br>
Mitigation: Require successful flyai CLI execution and verify that each displayed hotel result includes a Book link sourced from detailUrl. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/family-hotel) <br>
- [Parameter and Output Templates](artifact/references/templates.md) <br>
- [Hotel Search Playbooks](artifact/references/playbooks.md) <br>
- [Hotel Fallbacks](artifact/references/fallbacks.md) <br>
- [Execution Log Runbook](artifact/references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with hotel comparison tables, booking links, and inline shell commands for CLI execution or fallback steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; hotel results should include Book links from detailUrl and should not expose raw JSON.] <br>

## Skill Version(s): <br>
v3.2.3 (source: ClawHub release metadata; artifact frontmatter states 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
