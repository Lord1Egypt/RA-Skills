## Description: <br>
Print images and PDFs to CUPS printers while querying printer capabilities and applying PPD-aware paper, margin, resolution, and duplex settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to list CUPS printers, inspect printer options, and submit user-selected PDF or image files to a local macOS or Linux printer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit documents to local or shared printers, which may expose confidential content or print to an unintended device. <br>
Mitigation: Before each print, confirm the file, target printer, and selected options, especially for confidential documents or shared/default printers. <br>
Risk: Custom CUPS options can change trays, media, quality, duplex, or color behavior and produce incorrect or wasteful output. <br>
Mitigation: Review any -o options before printing and use the info or options commands to confirm available printer settings when uncertain. <br>


## Reference(s): <br>
- [Printer on ClawHub](https://clawhub.ai/odrobnik/cups-printer) <br>
- [Setup guide](SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from CUPS printer commands, with shell commands for invoking the skill.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local CUPS tools and can submit print jobs to the selected or default printer.] <br>

## Skill Version(s): <br>
1.2.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
