## Description: <br>
设计框架自动生成套件（确认处理器）：处理用户对设计框架预览的回复，支持确认/取消/重新生成 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[807209066](https://clawhub.ai/user/807209066) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Design automation users use this suite helper to handle confirmation, cancellation, regeneration, timeout, and duplicate-trigger replies after a design framework preview is sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic chat replies could accidentally confirm or regenerate a pending design workflow. <br>
Mitigation: Prefer explicit commands or structured replies and bind replies to the originating user or session. <br>
Risk: Cancellation cleanup could affect unrelated temporary files if the suite scope is not respected. <br>
Mitigation: Keep cleanup limited to the design-framework suite's own /tmp files. <br>
Risk: This helper depends on the surrounding design-framework suite behavior. <br>
Mitigation: Install it only with the intended suite and review the referenced sender skill and external scripts under $SK. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/807209066/design-framework-confirm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only helper for reply handling in a larger design-framework suite.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
