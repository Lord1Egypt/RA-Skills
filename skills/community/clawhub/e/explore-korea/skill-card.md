## Description: <br>
Plan Korea travel across Seoul, Busan, Jeju, flights, hotels, tickets, itineraries, visa information, insurance, car rentals, and related booking workflows powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel users and agents use this skill to search real-time Korea trip options, compare flights, hotels, attractions, and related services, and produce booking-oriented travel recommendations from flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and rely on the global @fly-ai/flyai-cli package. <br>
Mitigation: Install only in environments where the package is trusted and global CLI installation is acceptable. <br>
Risk: Travel details may be sent to the flyai or Fliggy-backed service to retrieve real-time results. <br>
Mitigation: Use only when users are comfortable sharing trip details with that service and avoid sending unnecessary sensitive information. <br>
Risk: Local execution logs may retain raw trip requests and command history. <br>
Mitigation: Prevent creation of .flyai-execution-log.json when possible or remove it when retained travel request history is not desired. <br>


## Reference(s): <br>
- [Explore Korea Skill Page](https://clawhub.ai/xiejinsong/explore-korea) <br>
- [Parameter and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Fallback Guidance](references/fallbacks.md) <br>
- [Execution Log Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and occasional inline shell commands for retries or setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output and booking detail URLs; raw JSON is not intended for user-facing output.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
