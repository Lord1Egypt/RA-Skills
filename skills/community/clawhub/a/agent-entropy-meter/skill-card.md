## Description: <br>
Measure information entropy and redundancy in agent group communications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roamer-remote](https://clawhub.ai/user/roamer-remote) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to quantify communication efficiency, redundancy, mutual information, and knowledge overlap across multi-agent systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent message categories or topic labels passed into reports may contain sensitive operational information. <br>
Mitigation: Minimize, anonymize, or aggregate input labels before analysis, especially when sharing generated reports. <br>
Risk: Metric interpretation depends on the quality and consistency of user-provided categories, topics, and paired message arrays. <br>
Mitigation: Review category definitions and input alignment before using entropy or redundancy scores to make decisions about multi-agent system health. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roamer-remote/agent-entropy-meter) <br>
- [Publisher profile](https://clawhub.ai/user/roamer-remote) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [JavaScript API results and human-readable text reports with ASCII bar charts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Computes entropy, redundancy, mutual information, and knowledge-overlap metrics from user-provided agent message categories and topics.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
