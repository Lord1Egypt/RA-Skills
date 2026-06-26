## Description: <br>
Azure Data Studio is a local Bash-based data utility for querying, importing, exporting, transforming, validating, and summarizing flat-file records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to run lightweight local data operations from an agent-assisted shell workflow, including quick queries, file import/export, schema checks, and simple record summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command arguments may be written to a local history log. <br>
Mitigation: Avoid passing secrets, tokens, sensitive queries, or private filenames as command arguments, and remove the local history log if sensitive data is entered. <br>
Risk: The executed azuredatastudio command may not be the intended local script. <br>
Mitigation: Verify which azuredatastudio executable is on PATH before relying on command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/azuredatastudio) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output is written to stdout; the bundled scripts can create local data and history files under the configured data directory.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
