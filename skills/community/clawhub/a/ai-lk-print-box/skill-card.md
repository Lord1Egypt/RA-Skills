## Description: <br>
Lianke Print Box helps agents use the lk-print CLI to authenticate with a Lianke cloud print box, check printer and task status, submit print jobs, and scan documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NullYing](https://clawhub.ai/user/NullYing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Lianke cloud print box devices through lk-print, including printer discovery, print submission, print job status checks, scan task creation, and scan result checks. It is not intended for local directly connected printers or non-Lianke devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud printing and scanning can expose sensitive credentials, printed files, scanned documents, printer IDs, scanner IDs, and task IDs. <br>
Mitigation: Treat ApiKey, DeviceId, DeviceKey, document contents, device identifiers, and task identifiers as sensitive, and use the skill only with a trusted Lianke lk-print source and Lianke cloud service. <br>
Risk: A print, scan, cancel, or delete command can affect a real device or task. <br>
Mitigation: Confirm the exact file, printer or scanner, copy count, task ID, and intended action before running lk-print commands. <br>


## Reference(s): <br>
- [Lianke Print Box ClawHub listing](https://clawhub.ai/NullYing/ai-lk-print-box) <br>
- [NullYing publisher profile](https://clawhub.ai/user/NullYing) <br>
- [lk-print install package from ClawHub metadata](https://github.com/liankenet/ai-lk-print-box.git) <br>
- [Lianke Open Platform](https://open.liankenet.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON output from lk-print commands when status or device details are requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
