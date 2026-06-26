## Description: <br>
Avenir Web runs and improves autonomous web tasks end-to-end with mode selection, instruction validation, single or batch execution, and next-step recommendations. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[yiliu-li](https://clawhub.ai/user/yiliu-li) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and researchers use this skill to run, inspect, and improve Avenir-Web autonomous browser tasks on live websites. It supports single-task runs, batch experiments, atomic browser actions, page screenshot inspection, and concise outcome reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act autonomously on arbitrary live websites. <br>
Mitigation: Use it on low-risk or test sites by default, constrain task scope and maximum operations, and require explicit human confirmation before login, payment, account-management, healthcare, banking, or private-dashboard actions. <br>
Risk: Page screenshots, visible content, task text, and action history may be sent to OpenRouter and saved in local logs or screenshots. <br>
Mitigation: Avoid sensitive pages unless redaction, retention limits, access controls, and review of stored run artifacts are in place. <br>
Risk: Browser instrumentation may conflict with website automation policies. <br>
Mitigation: Review the browser automation behavior before deployment and remove, disable, or gate stealth-style instrumentation where compliance with site terms is required. <br>


## Reference(s): <br>
- [Avenir-Web arXiv Paper](https://arxiv.org/abs/2602.02468) <br>
- [Avenir-Web PDF](https://arxiv.org/pdf/2602.02468.pdf) <br>
- [Avenir-Web Demo Video](https://www.youtube.com/watch?v=X38CH0xc_sg&t=16s) <br>
- [Avenir Web on ClawHub](https://clawhub.ai/yiliu-li/avenir-web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured run summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Run summaries should include execution metadata, status, evidence, diagnosis, and one recommended next action.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
