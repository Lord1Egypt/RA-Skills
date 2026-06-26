## Description: <br>
Manage Blinko notes and blinkos from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pigd0g](https://clawhub.ai/user/pigd0g) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users with a Blinko instance use this skill to list, create, update, delete, and promote notes or blinkos from an agent-driven command line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, create, update, promote, and delete Blinko notes through a configured API token. <br>
Mitigation: Install it only for agents that should manage Blinko notes, and confirm note IDs before update, promote, or delete actions. <br>
Risk: The Blinko API token grants access to the configured Blinko instance. <br>
Mitigation: Protect BLINKO_TOKEN like a password and set BLINKO_HOST only to a trusted Blinko instance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pigd0g/blinko-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API responses are printed to stdout; errors are printed to stderr with non-zero exit codes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
