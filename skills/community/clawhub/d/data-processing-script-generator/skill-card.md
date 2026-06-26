## Description: <br>
Generates Python data-processing scripts from user-provided Excel templates and ERP export data to automate report creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangxiao971208-star](https://clawhub.ai/user/yangxiao971208-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations users use this skill to turn confirmed spreadsheet templates, ERP exports, mappings, paths, and naming rules into runnable Python automation for recurring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scripts may process sensitive business or personal spreadsheet data. <br>
Mitigation: Provide only the files needed for the task and inspect samples for sensitive data before sharing them. <br>
Risk: Generated Python code may write, overwrite, or delete local files if paths or logic are wrong. <br>
Mitigation: Review generated scripts for file operations and test them first on copies or non-production data. <br>
Risk: Incorrect paths, mappings, file names, or encoding assumptions can produce inaccurate reports. <br>
Mitigation: Confirm paths, naming conventions, sheet mappings, processing rules, and encodings before running the script. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and usage instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated scripts should use user-confirmed paths, mappings, naming rules, and encoding assumptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
