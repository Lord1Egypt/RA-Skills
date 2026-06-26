## Description: <br>
Briefing-pro turns URLs, uploaded files, images, or pasted text into a one-page briefing slide that can be exported as PNG, PDF, or HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nonlinearHuman](https://clawhub.ai/user/nonlinearHuman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers can use this skill to convert supplied source material into a compact visual briefing for sharing, archiving, or presentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch supplied URLs and parse uploaded files to create briefing output. <br>
Mitigation: Avoid using sensitive documents unless the user is comfortable with that content being parsed and rendered. <br>
Risk: The generic trigger term "摘要" may activate the skill when a user only intended a basic summary. <br>
Mitigation: Consider narrowing the trigger phrase before deployment in environments where accidental activation would be disruptive. <br>
Risk: Generated briefing slides may omit nuance from the source material because the skill uses fast rule-based extraction. <br>
Mitigation: Review the generated briefing before sharing, archiving, or presenting it. <br>


## Reference(s): <br>
- [frontend-slides](https://clawhub.com/skill/frontend-slides) <br>
- [Briefing-pro ClawHub release](https://clawhub.ai/nonlinearHuman/briefing-jianbao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance, files] <br>
**Output Format:** [Briefing slide content rendered as HTML, PNG image, or PDF with agent-facing guidance as text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports A4 portrait and 16:9 widescreen slide sizes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
