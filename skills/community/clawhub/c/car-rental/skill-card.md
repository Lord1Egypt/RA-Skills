## Description: <br>
Find the best car rental deals with price comparison, alerts, and lease vs rent analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to compare car rental, lease, subscription, and buy options, including total-cost factors such as insurance, fees, mileage, fuel policy, location, and duration. It can also help track local preferences, saved searches, and optional price or availability alerts when the user permits local storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may keep local preferences, saved searches, and alert history under ~/car-rental/. <br>
Mitigation: Approve local storage only when personalization is desired, review or delete the files when no longer needed, and keep alerts disabled unless explicitly requested. <br>
Risk: Broad activation could cause general travel conversations to trigger car-rental assistance. <br>
Mitigation: Choose narrow activation for explicit car-rental requests during setup. <br>
Risk: Rental price comparisons and alerts may send search parameters such as location, dates, and car type to rental sites. <br>
Mitigation: Avoid sharing payment information or personal identifiers through this skill; use it for comparison guidance and complete bookings directly with chosen providers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/car-rental) <br>
- [Skill Homepage](https://clawic.com/skills/car-rental) <br>
- [Setup](artifact/setup.md) <br>
- [Sites and Sources](artifact/sites.md) <br>
- [Rent vs Lease vs Buy](artifact/comparison.md) <br>
- [Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional local markdown memory and search configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local files under ~/car-rental/ only after user permission; does not make bookings or store payment information.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
