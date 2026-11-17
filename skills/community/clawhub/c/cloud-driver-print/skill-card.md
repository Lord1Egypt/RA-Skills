## Description:

A client-side printing skill for LAN printers that helps agents discover printers, search drivers, upload DOCX, Excel, PPT, PDF, and image files to a cloud rendering service, and send rendered print data to network printers on port 9100.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimsoft](https://clawhub.ai/user/zimsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to automate document printing to known or newly discovered LAN printers, including driver lookup, cloud conversion, print rendering, and delivery of rendered data to the printer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user documents to a cloud print service.

Mitigation: Use only with non-sensitive documents until explicit upload and print confirmation is added.

Risk: The skill sends live print jobs to network printers.

Mitigation: Run it only against trusted printers and require users or operators to confirm target printer IP, driver, and print settings before execution.

Risk: A cloud-returned fileUrl could expose the API token if the URL scheme or host is not validated before download.

Mitigation: Validate the fileUrl scheme and trusted host before attaching Authorization headers or downloading rendered print data.

Risk: Rendered print downloads may be unexpectedly large or empty.

Mitigation: Bound download sizes and fail closed when rendered data is empty before sending anything to the printer.

Risk: Local document conversion uses a shared temporary directory.

Mitigation: Use a private temporary directory for conversions and clean converted files after printing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zimsoft/skills/cloud-driver-print)
- [Printer identification with ipptool](references/printer-identification-ipptool.md)
- [EPSON L6270 Series integration notes](references/epson-l6270-experience.md)
- [_pfs empty fileUrl troubleshooting](references/pfs-empty-fileurl-debug.md)
- [Cloud print API troubleshooting log](references/session-20260515-pfs-cvturl.md)
- [Cloud print service](https://any.webprinter.cn)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload source documents to a cloud print service, download rendered print data, and send rendered data to a LAN printer.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
