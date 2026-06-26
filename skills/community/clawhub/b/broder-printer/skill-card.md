## Description: <br>
Brother DCP-T426W network printer skill -- IPP plus driverless printing as the primary path, with TCP direct printing as a text-only fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yardfarmer](https://clawhub.ai/user/yardfarmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local device operators use this skill to print text, images, and PDFs to a Brother DCP-T426W on a local network, check printer status, and use a text-only TCP fallback when CUPS is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package bundles an unrelated Sonos speaker-control skill that users would not expect in a printer package. <br>
Mitigation: Review or remove skills/sonoscli before installing, and disclose any retained speaker-control behavior and external tool installation. <br>
Risk: The printer script targets the hardcoded local IP address 192.168.50.232, which could send sensitive files to the wrong device if the network differs. <br>
Mitigation: Confirm the printer address belongs to the intended Brother DCP-T426W or update the script and CUPS queue before printing sensitive content. <br>
Risk: The CUPS setup commands make persistent printer configuration changes and use sudo. <br>
Mitigation: Run the CUPS setup only on intended hosts after reviewing the lpadmin commands and printer queue name. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yardfarmer/broder-printer) <br>
- [Publisher profile](https://clawhub.ai/user/yardfarmer) <br>
- [Sonos CLI homepage](https://sonoscli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local CUPS commands or send TCP print jobs to the configured printer IP.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG released 2026-04-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
