## Description: <br>
Amazing PsyCoder routes psychology experiment and data-analysis requests through mandatory designer, coder, and reviewer chains for PsychoPy, jsPsych, Psychtoolbox, R, and Python workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soupandpsy](https://clawhub.ai/user/soupandpsy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to design psychology experiments, generate experiment code, plan statistical analyses, generate R or Python analysis scripts, and review outputs before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer behavior may replace existing same-named skill folders. <br>
Mitigation: Install only after reviewing the target skills directory and backing up any same-named local skills that should be preserved. <br>
Risk: Some experiment templates may collect participant IP, location, or browser metadata. <br>
Mitigation: Review generated online experiments for participant privacy and remove IP, location, or user-agent collection unless explicitly consented and required. <br>
Risk: Demo snippets using eval or exec patterns may be unsuitable for production experiments. <br>
Mitigation: Do not copy eval or exec based demo snippets into production experiments; replace them with explicit, reviewed control flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soupandpsy/amazing-psycoder) <br>
- [Publisher profile](https://clawhub.ai/user/soupandpsy) <br>
- [agentskills.io standard](https://agentskills.io) <br>
- [Platform Adapter Reference](artifact/PLATFORMS.md) <br>
- [Experiment Designer references](artifact/psy-exp-designer/references/) <br>
- [Analysis method library](artifact/psy-ana-designer/methods/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration, R/Python/JavaScript/MATLAB code, shell commands, and audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include experiment configs, condition-file guidance, runnable experiment scripts, analysis scripts, reports, and reviewer findings.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence; artifact frontmatter reports 1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
