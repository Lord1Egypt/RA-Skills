## Description: <br>
Academic Pipeline Suite is a bundled meta-skill package for installing and using an academic research and writing workflow with literature search, deep research, paper writing, peer review, humanization, IMA knowledge-base, and integrity verification skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric-promax](https://clawhub.ai/user/eric-promax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, students, researchers, and academic writers use this skill to install a bundled academic workflow and guide literature search, research synthesis, drafting, review, revision, integrity checks, and final document preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation workflow can overwrite existing local academic skills. <br>
Mitigation: Review the install script before use and back up existing local skills before installing or reinstalling the suite. <br>
Risk: Some academic search workflows can control a logged-in Chrome session through remote debugging. <br>
Mitigation: Use a dedicated browser profile, avoid enabling remote debugging on an everyday profile, and stop the CDP proxy when the task is complete. <br>
Risk: Humanizer components may be used to conceal AI assistance where disclosure is required. <br>
Mitigation: Use rewriting features only within applicable academic, institutional, and venue disclosure policies. <br>
Risk: Some workflows require user-provided credentials for academic or knowledge-base services. <br>
Mitigation: Use least-privilege credentials where possible and avoid placing secrets in shared prompts, drafts, or generated reports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/eric-promax/academic-pipeline-suite) <br>
- [Publisher profile](https://clawhub.ai/user/eric-promax) <br>
- [Complete usage guide](https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg) <br>
- [Quickstart guide](QUICKSTART.md) <br>
- [Release notes](RELEASE_NOTES.md) <br>
- [Academic pipeline state machine](skills/academic-pipeline/references/pipeline_state_machine.md) <br>
- [Integrity review protocol](skills/academic-pipeline/references/integrity_review_protocol.md) <br>
- [Academic search API cookbook](skills/academic-search/references/api-cookbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with commands, checklists, review reports, drafting and revision artifacts, and document preparation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local installed skills, external academic APIs, user-provided credentials, and browser automation depending on the workflow stage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata references 3.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
