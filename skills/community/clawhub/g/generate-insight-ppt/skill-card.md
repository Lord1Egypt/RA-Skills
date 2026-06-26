## Description: <br>
Generates technology insight PowerPoint reports through a workflow for web collection, insight extraction, slide content generation, optimization, and PPTX output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xieyuantao7](https://clawhub.ai/user/xieyuantao7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and technical teams use this skill to research a technology topic, extract supporting insights, structure a slide outline, and generate a PPTX report with consistent styling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches the web, downloads pages or PDFs, and turns collected material into report files. <br>
Mitigation: Run it in a limited workspace and review collected sources and generated slides before relying on the report. <br>
Risk: The artifact uses hard-coded Windows output paths under D:\techinsight\reports. <br>
Mitigation: Review or adjust the configured output path before execution so generated files stay within the intended workspace. <br>
Risk: The security guidance notes quality and path-scope caveats in the included PPT generator scripts. <br>
Mitigation: Treat the PPT generation scripts as needing repair or validation before production use, and confirm the generated PPTX opens correctly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xieyuantao7/generate-insight-ppt) <br>
- [README.md](README.md) <br>
- [scripts/README.md](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, JSON, Shell commands] <br>
**Output Format:** [PPTX presentation files with intermediate JSON and Markdown artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes session output folders under D:\techinsight\reports by default.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
