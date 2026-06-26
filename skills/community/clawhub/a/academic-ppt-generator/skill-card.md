## Description: <br>
Generates structured academic presentation outlines and PowerPoint files from user-prepared literature analysis JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziyi-z-z](https://clawhub.ai/user/ziyi-z-z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and educators use this skill to turn structured academic paper analysis into presentation-ready outlines and PPTX files for literature reviews, lab meetings, and academic talks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release description overstates automatic PDF-to-PPT behavior, while the artifact scripts expect prepared analysis JSON. <br>
Mitigation: Prepare and review the structured paper-analysis JSON before running the PPT generation scripts. <br>
Risk: Generated academic slides may omit context or misrepresent a paper if the input analysis is incomplete or inaccurate. <br>
Mitigation: Review slide content, speaker notes, and cited findings against the source paper before presenting. <br>


## Reference(s): <br>
- [Analysis Guide](references/analysis_guide.md) <br>
- [Example Analysis JSON](references/example_analysis.json) <br>
- [PPT Template Notes](assets/template_readme.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ziyi-z-z/academic-ppt-generator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, json, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, JSON structures, Python scripts, shell commands, and PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-prepared structured paper-analysis JSON; local PowerPoint export depends on python-pptx.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
