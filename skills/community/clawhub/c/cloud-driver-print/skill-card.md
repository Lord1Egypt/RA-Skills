## Description: <br>
用于局域网打印机场景的客户端技能。打印 DOCX/EXCEL/PPT/PDF/图片等类型文件 到网络打印机（9100端口），支持发现、驱动搜索、云端上传、云端转打印数据并通过 9100 下发。Agent 自动化场景下一行命令搞定。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimsoft](https://clawhub.ai/user/zimsoft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to discover LAN printers, select cloud printer drivers, upload printable documents for conversion, and submit rendered print data to network printers. It is intended for DOCX, spreadsheet, presentation, PDF, and image printing workflows where cloud-assisted driver rendering is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads documents and printer metadata to any.webprinter.cn for cloud-assisted conversion and rendering. <br>
Mitigation: Use it only with files and printer metadata that are approved for that provider, and avoid confidential or regulated documents unless the provider's handling, retention, and access controls have been reviewed. <br>
Risk: The skill can use CDF_PRINT_API_KEY or other sensitive credentials for cloud print requests. <br>
Mitigation: Scope credentials to the minimum required access, store them in the environment rather than source files, and rotate or revoke them if they are exposed. <br>
Risk: The skill can submit real print jobs to LAN printers over TCP/9100. <br>
Mitigation: Require the operator or calling agent to confirm target printer, file, copies, color, and duplex settings before running print commands in shared or production environments. <br>
Risk: Raw TCP/9100 fallback behavior can send binary data directly to printers and may disrupt devices if used incorrectly. <br>
Mitigation: Use the documented cloud rendering path and reserve raw TCP/9100 fallback testing for trusted test printers only. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zimsoft/cloud-driver-print) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zimsoft) <br>
- [EPSON L6270 Series access reference](artifact/references/epson-l6270-experience.md) <br>
- [_pfs empty fileUrl debug notes](artifact/references/pfs-empty-fileurl-debug.md) <br>
- [Printer identification with ipptool](artifact/references/printer-identification-ipptool.md) <br>
- [Cloud print API troubleshooting notes](artifact/references/session-20260515-pfs-cvturl.md) <br>
- [Cloud print service](https://any.webprinter.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local printer records and may submit real print jobs to a target network printer.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
