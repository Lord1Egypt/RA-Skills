## Description: <br>
Imports files from a selected local directory into DeepVista as file-type context cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingconan](https://clawhub.ai/user/jingconan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base users use this recipe to bulk import project files into DeepVista so they can search and reuse them as context cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload many local file contents into an external DeepVista knowledge base. <br>
Mitigation: Confirm a narrow directory or extension filter before running, and exclude credentials, customer data, confidential files, dependency folders, and generated files. <br>
Risk: Bulk import can unintentionally duplicate cards or include irrelevant generated content. <br>
Mitigation: Warn before importing more than 50 files and skip common noise directories, lock files, minified files, and source maps by default. <br>


## Reference(s): <br>
- [DeepVista CLI homepage](https://cli.deepvista.ai) <br>
- [ClawHub skill page](https://clawhub.ai/jingconan/deepvista-recipe-import-files) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to create one DeepVista file card per selected text file and report import results.] <br>

## Skill Version(s): <br>
0.1.0-alpha.21 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
