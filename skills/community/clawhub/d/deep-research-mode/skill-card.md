## Description: <br>
Deep Research Mode coordinates 10-50 specialized agents to discuss, challenge, decide, and produce detailed research reports for difficult scientific research questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and technical teams use this skill to structure long-running, multi-agent analysis of complex research questions and produce staged research artifacts and a final detailed report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can trigger expensive, long-running multi-agent research sessions. <br>
Mitigation: Invoke it explicitly, confirm before launching large runs, and set practical limits for agent count, runtime, model choice, and budget. <br>
Risk: Separately obtained helper scripts referenced by the skill may affect the runtime behavior if used. <br>
Mitigation: Review and scan any helper scripts before deployment or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jirboy/deep-research-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research reports, progress summaries, review notes, decision reports, and task assignments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce long-form reports and intermediate process documents; users should set practical agent, runtime, model, and budget limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
