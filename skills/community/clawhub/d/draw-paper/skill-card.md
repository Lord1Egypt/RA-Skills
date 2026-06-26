## Description: <br>
Reads paper figure prompts, sends them to Gemini through browser automation, and saves generated scientific diagram images to a fixed local folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m1ss-cell](https://clawhub.ai/user/m1ss-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to automate generation of scientific figure drafts from prompts extracted from paper parsing files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends extracted figure prompts to Gemini. <br>
Mitigation: Avoid sensitive paper content in prompts unless sharing it with Gemini is acceptable. <br>
Risk: The skill relies on fixed local input and output paths. <br>
Mitigation: Install only in an environment where those paths are intended and accessible. <br>
Risk: Repeated runs may overwrite figure files in the output folder. <br>
Mitigation: Use simple intended filenames and check the output folder before rerunning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/m1ss-cell/draw-paper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, API Calls] <br>
**Output Format:** [STATE status messages and PNG image files saved locally] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses fixed local input and output directories and processes figures sequentially.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
