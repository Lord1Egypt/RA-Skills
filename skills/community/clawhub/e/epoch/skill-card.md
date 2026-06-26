## Description: <br>
Convert Unix timestamps, compare epochs, and do time arithmetic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Epoch to convert Unix timestamps, parse date strings, compare epochs, and perform simple time arithmetic while debugging logs or checking timezone offsets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Bash helper and depends on standard Unix date and awk behavior. <br>
Mitigation: Install and run it only in environments where Bash 4+, date, and awk are available and acceptable for local timestamp work. <br>
Risk: Date parsing and timezone output can vary across Unix date implementations and local timezone settings. <br>
Mitigation: Review converted timestamps against the intended local or UTC timezone before using results in operational decisions. <br>


## Reference(s): <br>
- [ClawHub Epoch release page](https://clawhub.ai/bytesagain3/epoch) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Bash output from date and awk; no API keys or external services are required.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
