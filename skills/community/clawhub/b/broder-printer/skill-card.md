## Description:

Brother DCP-T426W network printer skill - IPP + driverless (primary), TCP direct (fallback for text-only, no sudo).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yardfarmer](https://clawhub.ai/user/yardfarmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and local automation users use this skill to print text, images, PDFs, test pages, and status checks to a Brother DCP-T426W network printer from CLI-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an unrelated bundled Sonos control skill with a mutable external Go CLI installer.

Mitigation: Review or remove the bundled sonoscli directory before installing this printer skill, and avoid running its installer unless Sonos control is intended.

Risk: CUPS setup uses privileged printer configuration commands and targets a specific printer URI.

Mitigation: Run privileged CUPS setup only on the intended host after confirming the printer name, IP address, and IPP URI.

Risk: Print commands send real output to the configured network printer.

Mitigation: Use test/status commands first and confirm the selected method before sending user documents or raw TCP output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yardfarmer/skills/broder-printer)
- [Sonos CLI homepage](https://sonoscli.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and Python CLI usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces printer setup guidance, print/status commands, and local Python CLI invocations; print commands can send real output to the configured printer.]

## Skill Version(s):

5.0.0 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
