## Description: <br>
Diagnoses Alibaba Cloud ApsaraVideo Live recording issues, including missing recordings, file generation problems, unexpected recording behavior, and callback issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to investigate Alibaba Cloud Live recording failures by confirming parameters, running read-only Aliyun CLI diagnostics, reviewing recording and callback evidence, and producing a diagnostic report with next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Alibaba Cloud credentials and can expose sensitive access information if users paste keys into chats, command lines, or transcripts. <br>
Mitigation: Use a dedicated read-only RAM user or role, configure credentials outside the agent chat, and verify credential presence with non-secret status commands only. <br>
Risk: Aliyun CLI plugin and AI-mode settings may persist after diagnostic use if not returned to the expected state. <br>
Mitigation: Check Aliyun CLI AI mode and plugin settings after use, and disable AI mode at every workflow exit point. <br>
Risk: Diagnostic commands query Alibaba Cloud account resources and may need permissions broader than a user initially expects. <br>
Mitigation: Grant only the documented read-only RAM actions needed for Live recording diagnostics and pause on permission failures until access is explicitly approved. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/sdk-team/alibabacloud-liverecord-diagnosis) <br>
- [Publisher Profile](https://clawhub.ai/user/sdk-team) <br>
- [RAM Policies for Live Recording Diagnostic Skill](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Recording Error Codes and Resolutions](references/error-codes.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [API Response Examples](references/api-response-examples.md) <br>
- [Diagnostic Report Template](references/diagnostic-report-template.md) <br>
- [ApsaraVideo Live Recording Documentation](https://help.aliyun.com/live/user-guide/live-stream-recording) <br>
- [Recording Callback Documentation](https://help.aliyun.com/live/user-guide/manage-callbacks) <br>
- [Live Streaming Best Practices](https://help.aliyun.com/live/user-guide/live-stream-ingest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown diagnostic guidance with inline shell commands and structured report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostic workflow for one live stream context at a time; requires confirmed user parameters before CLI calls.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
