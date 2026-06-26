## Description: <br>
建筑学长AI工作流 helps interior-design teams coordinate an AI-assisted workflow for collecting references, generating design outputs, preparing PPT proposals, estimating budgets, and packaging deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[137984917-cyber](https://clawhub.ai/user/137984917-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Interior designers and design studio operators use this skill to coordinate early-stage residential, villa, small commercial, and concept proposal workflows. It helps an agent organize project briefs, reference collection, AI image outputs, budget estimates, proposal decks, and final delivery packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad browser, download, and file automation could write to the wrong location or collect unintended files. <br>
Mitigation: Require confirmation of the project folder, download sources, desktop writes, browser automation, file renaming, and packaging before execution. <br>
Risk: A daily scheduled downloader could continue running unexpectedly. <br>
Mitigation: Do not enable scheduled downloading unless the user explicitly requests it and knows how to stop and remove the schedule. <br>
Risk: Generated design proposals, images, and budget estimates may be inaccurate for a real client project. <br>
Mitigation: Review generated images, PPT content, and budget CSV files before using them for client delivery or commercial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/137984917-cyber/architect-ai-workflow) <br>
- [建筑学长 AI绘图创作](https://www.jianzhuxuezhang.com/ai/draw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with workflow steps, automation instructions, and generated project artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the workflow may create folders, download and rename images, generate PPT and CSV files, and package deliverables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
