## Description: <br>
Manage Booking.com properties by downloading reservations, listing and replying to guest messages, and updating rates through a Python CLI that automates the Booking.com extranet in Chrome. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matsei-ruka](https://clawhub.ai/user/matsei-ruka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hospitality operators and property managers use this skill to help an agent run Booking.com extranet workflows such as checking properties, reviewing guest conversations, downloading reservation data, and preparing rate updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with live Booking.com partner account access and may send guest messages or change rates. <br>
Mitigation: Require manual review before sending guest messages or changing rates, and confirm each target property, conversation, and rate update before execution. <br>
Risk: The scanned package wraps external automation code that is not included in the scanned artifact. <br>
Mitigation: Install only after reviewing the external bot code and confirming it matches the expected Booking.com automation behavior. <br>
Risk: The workflow uses Booking.com credentials, optional TOTP automation, and a persistent Chrome session. <br>
Mitigation: Protect the .env and .chrome-data directories, restrict local access to the host, and confirm the automation is allowed for the Booking.com account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matsei-ruka/booking-extranet-manager) <br>
- [Publisher profile](https://clawhub.ai/user/matsei-ruka) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce JSON responses or Excel reservation exports through the external Booking.com automation CLI.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
