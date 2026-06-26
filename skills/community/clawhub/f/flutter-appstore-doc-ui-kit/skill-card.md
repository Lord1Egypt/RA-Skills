## Description: <br>
Generate a launch-ready App Store package for a Flutter app, including bilingual Markdown feature documents, Apple-style UI design images, and a square-corner app icon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chentuan7963-afk](https://clawhub.ai/user/chentuan7963-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product designers, and app teams use this skill to draft App Store-oriented Flutter v1.0.0 feature documentation and companion visual assets before implementation or submission review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional image-generation step can send prompt-level app design details to OpenAI. <br>
Mitigation: Avoid the OpenAI image step for confidential plans, or review and minimize prompt content before using it. <br>
Risk: Generated App Store copy or visual assets may still need product, legal, and platform review. <br>
Mitigation: Use the built-in approval gates and review the included App Store safety checklist before relying on the outputs. <br>
Risk: Generated files are written into the selected output directory and can mix with prior drafts. <br>
Mitigation: Run the skill with a dedicated output directory for each app package. <br>


## Reference(s): <br>
- [App Store Review Safety Checklist](references/review-safety-checklist.md) <br>
- [ClawHub skill page](https://clawhub.ai/chentuan7963-afk/flutter-appstore-doc-ui-kit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Image files, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown documents, PNG/SVG image assets, shell commands, and prompt guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses staged approval gates; optional OpenAI image generation requires OPENAI_API_KEY; generated files are written to a user-selected output directory.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
