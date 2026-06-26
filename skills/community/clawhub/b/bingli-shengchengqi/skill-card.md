## Description: <br>
Helps draft structured admission records through a three-step flow that collects, confirms, and formats patient-provided details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gshatw](https://clawhub.ai/user/gshatw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users preparing draft admission records can use this skill to collect core patient details, confirm the inputs, and produce a formatted admission-record draft. It is not a substitute for clinical judgment or final medical documentation review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle sensitive health information. <br>
Mitigation: Use only with explicit user intent and avoid entering real patient-identifying information unless the environment is approved for it. <br>
Risk: Generated records may include unprovided or defaulted clinical details. <br>
Mitigation: Treat outputs as drafts, mark missing facts as unknown or pending, and require clinician review before use. <br>


## Reference(s): <br>
- [Bingli Shengchengqi on ClawHub](https://clawhub.ai/gshatw/bingli-shengchengqi) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-formatted admission record draft with conversational prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated records are drafts and may include default values for missing clinical facts; clinician review is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, _meta.json, INDEX.md, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
