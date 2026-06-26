## Description: <br>
Prints files uploaded to a Feishu group chat using smart matching by filename, file type, time range, or count, and can also print direct text content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caigang78](https://clawhub.ai/user/caigang78) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees or agents in a Feishu-based workflow use this skill to locate recent or named Feishu chat uploads and send them to a configured local printer. It also supports printer status checks, queue checks, cancellation, and direct text printing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive Feishu documents could be sent to a shared or unintended printer. <br>
Mitigation: Set an explicit trusted PRINTER value and confirm the requested files before printing in shared printer environments. <br>
Risk: The skill depends on shared Feishu helper code that is not included in this artifact. <br>
Mitigation: Install only when the shared helper code is trusted and the Feishu account or chat access scope is understood. <br>
Risk: The cancel-all printer command can remove jobs beyond the current document. <br>
Mitigation: Use cancel -a only when intentionally administering that printer and after checking the queue. <br>
Risk: Downloaded Feishu files may remain in the local inbound media directory. <br>
Mitigation: Periodically remove no-longer-needed files from ~/.openclaw/media/inbound. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caigang78/feishu-print) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment variables such as PRINTER, LIMIT, NAME_PREFIX, NAME_CONTAINS, MINUTES, FILE_TYPE, and INBOUND_DIR.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
