## Description: <br>
Search Z-Library and send EPUBs to Kindle <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hsin-Lan](https://clawhub.ai/user/Hsin-Lan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local book2kindle CLI for searching Z-Library and sending selected EPUB files to Kindle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local book2kindle CLI and sends user-selected content to Kindle. <br>
Mitigation: Install only when the local CLI is trusted, verify the selected result number before sending, and avoid sensitive account destinations or untrusted files. <br>
Risk: Z-Library search and EPUB delivery can involve copyright or usage-rights concerns. <br>
Mitigation: Confirm the user has the right to download and send the selected book before using the skill. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Conversational text summarizing CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include numbered search results with title, author, format, and file size when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
