## Description: <br>
Routes agent file exchange through Qiniu Kodo using qshell commands for authenticated download and upload workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents that exchange files with users use this skill to receive file_input:// links, download the referenced Qiniu Kodo object into the workspace, and upload outbound files to a Qiniu Kodo bucket with timestamped names. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files and Qiniu credentials are involved in normal operation, so broad credentials or unreviewed uploads can expose data. <br>
Mitigation: Use scoped Qiniu credentials, review each file before upload, and periodically remove objects or buckets that are no longer needed. <br>
Risk: The workflow depends on qshell binaries downloaded from external links. <br>
Mitigation: Verify the qshell download source before use and keep the download parameters from the documented Qiniu links. <br>


## Reference(s): <br>
- [Qiniu qshell documentation](https://developer.qiniu.com/kodo/1302/qshell) <br>
- [ClawHub skill page](https://clawhub.ai/kadbbz/file-exchange-via-qiniu-kodo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline command examples and file URI messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outbound file transfer completes with a standalone file_output:// URI after upload succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
