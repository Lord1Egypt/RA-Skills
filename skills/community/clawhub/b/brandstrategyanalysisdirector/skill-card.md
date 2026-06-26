## Description: <br>
BD-1 helps brand designers structure case analysis, design logic, industry trend tracking, and large research-material digests, then package the result as a presentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnwong1003](https://clawhub.ai/user/johnwong1003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Brand designers and research assistants use this skill to turn brand cases, competitive references, scattered strategy notes, industry keywords, or large document sets into structured analysis and next-step guidance. It is designed to support designer judgment rather than replace it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a PowerPoint file to a hardcoded Lenovo desktop path that may not exist or may be inappropriate on the user's machine. <br>
Mitigation: Confirm the save location before generation and use a path that matches the user's environment. <br>
Risk: Brand research inputs and generated presentation files may contain confidential business material. <br>
Mitigation: Only provide material approved for local presentation generation, and review or redact sensitive content before sharing the output. <br>
Risk: The skill may require installing pptxgenjs to generate PPTX files. <br>
Mitigation: Install dependencies only from trusted npm sources and review generated files before relying on them. <br>


## Reference(s): <br>
- [Module A: Case Analysis](references/module-a-case-analysis.md) <br>
- [Module B: Design Logic](references/module-b-design-logic.md) <br>
- [Module C: Industry Tracking](references/module-c-industry-tracking.md) <br>
- [Module D: Data Digest](references/module-d-data-digest.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Structured markdown analysis plus a generated PPTX presentation file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Presentation output should be saved to a user-confirmed desktop path; pptxgenjs may be required to generate slides.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
