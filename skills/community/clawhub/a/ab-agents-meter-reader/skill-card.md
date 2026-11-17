## Description:

Read meter readings from photos for electricity day/night tariffs and water meters, save reading history, and generate landlord messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexburrstudio](https://clawhub.ai/user/alexburrstudio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and household utility managers use this skill to extract electricity and water meter readings from photos, keep local reading history, and prepare a landlord-ready message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meter photos, tenant name, apartment address, readings, and the MiniMax API key are sensitive data handled by the skill.

Mitigation: Install only if comfortable sending meter photos to MiniMax, treat ~/.meter-readings and the API key as sensitive, and run the skill under a low-privilege account.

Risk: The skill executes an unpinned third-party MCP package at runtime.

Mitigation: Pin and review the MCP package version before use, and review the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexburrstudio/skills/ab-agents-meter-reader)
- [Skill homepage](https://github.com/alexburrstudio/ab-agents-meter-reader)
- [AB Agents Vision (MiniMax)](https://github.com/alexburrstudio/ab-agents-vision)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Plain text and JSON files with shell command usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores configuration and reading history locally under ~/.meter-readings]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
