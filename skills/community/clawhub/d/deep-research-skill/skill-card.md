## Description: <br>
Deep Research orchestrates multi-agent research by decomposing a goal into parallel subgoals, running Claude Code child processes for evidence collection, aggregating the results, and delivering a structured report file with key findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiskyer](https://clawhub.ai/user/feiskyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, analysts, developers, and other external users use this skill to run systematic web or material research, competitive and industry analysis, bulk link or dataset retrieval, and long-form evidence-integrated report writing through a supervised multi-agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated child agents can receive broad shell, file, web, and data-collection authority. <br>
Mitigation: Review the proposed plan before execution, use a dedicated workspace, and narrow child allowed tools whenever possible. <br>
Risk: Research work may create retained intermediate files, logs, cached source data, and final reports under .research/. <br>
Mitigation: Periodically delete research artifacts that should not be retained and avoid running confidential topics unless retention is acceptable. <br>
Risk: Networked research may send task context to external providers or services. <br>
Mitigation: Avoid confidential topics unless the relevant external providers are approved for the data involved. <br>


## Reference(s): <br>
- [Deep Research on ClawHub](https://clawhub.ai/feiskyer/deep-research-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and status summaries saved as workspace files, with supporting shell scripts, prompts, logs, and cached source data when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The final response provides the report path and a concise findings summary; full reports are saved to files rather than pasted in chat.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
