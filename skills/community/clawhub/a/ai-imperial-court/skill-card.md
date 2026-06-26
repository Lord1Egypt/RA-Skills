## Description: <br>
AI朝廷三省六部 maps the Tang dynasty three-department and six-ministry model into a multi-agent workflow for planning, review, and execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuxNd](https://clawhub.ai/user/kukuxNd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and agent users use this skill to organize complex requests into draft, review, and execution stages with specialized roles for planning, quality review, compliance, documentation, and implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad collaboration or review language may activate the workflow when the user expected a simpler response. <br>
Mitigation: Use the full planning and review process for complex or sensitive work, and use the simplified flow for single-step low-risk tasks. <br>
Risk: The quick-start helper writes local markdown records that may contain task details. <br>
Mitigation: Run the helper only when local records are desired, and avoid putting secrets or sensitive business details into those records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kukuxNd/ai-imperial-court) <br>
- [Six ministries reference](references/six-ministries.md) <br>
- [Execution examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown workflow drafts, review checklists, execution reports, command examples, and optional local markdown record files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The quick-start helper creates local records under a records directory when run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
