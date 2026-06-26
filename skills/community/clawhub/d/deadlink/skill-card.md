## Description: <br>
Scan websites and files for broken links with HTTP status details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and site owners use this skill to audit URLs in pages and files, check HTTP status details, and generate broken-link reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts URLs discovered in input files or web pages, which can send outbound requests to external sites. <br>
Mitigation: Run it only on files and sites you are authorized to audit and in environments where outbound link-checking traffic is acceptable. <br>
Risk: The report command writes timestamped report files in the current working directory. <br>
Mitigation: Run it from the intended workspace and review generated report files before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub Deadlink Skill Page](https://clawhub.ai/bytesagain3/deadlink) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text CLI output and timestamped text report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and network access; checks use a 10-second per-URL timeout.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
