## Description: <br>
Data Labeling Studio is a scaffolded data annotation toolkit for image, text, audio, and video workflows with example active learning, quality checking, and export commands. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data teams can use this skill to draft annotation workflows, CLI commands, and example code for dataset labeling and quality review. It is best suited for demonstrations or scaffolding, not for accepting labels or quality scores without replacing the mock logic and validating outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated annotations and quality scores may be random or synthetic while appearing production-ready. <br>
Mitigation: Replace the mock annotation and scoring logic before use, and manually validate generated labels and reports against trusted ground truth. <br>
Risk: Running the scripts on unauthorized or sensitive datasets could create governance and privacy issues. <br>
Mitigation: Use a virtual environment and run the skill only on datasets the operator is authorized to process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/data-labeling-studio) <br>
- [Publisher profile](https://clawhub.ai/user/kaiyuelv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; scripts may produce JSON annotation and quality report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated annotations and quality scores should be treated as demo outputs until the mock logic is replaced and results are manually validated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
