## Description: <br>
Helps an agent use the AnyGen CLI to request server-side deep research and comprehensive analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logictortoise](https://clawhub.ai/user/logictortoise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research analysts use this skill when they need an agent to produce industry analysis, competitive landscape mapping, market sizing, technology reviews, due diligence, regulatory analysis, or academic surveys through AnyGen. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to install the related anygen-workflow-generate skill automatically. <br>
Mitigation: Review the referenced workflow skill before installation and require explicit approval before using the automatic '-y' install path. <br>
Risk: Research prompts and source material are sent to AnyGen server-side services. <br>
Mitigation: Use a dedicated AnyGen API key and do not submit secrets, regulated data, or confidential research material unless AnyGen is approved for that data. <br>


## Reference(s): <br>
- [Deep Research on ClawHub](https://clawhub.ai/logictortoise/anygen-deep-research) <br>
- [AnyGen](https://www.anygen.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the AnyGen CLI, an ANYGEN_API_KEY or browser login, and the anygen-workflow-generate skill for deep_research execution.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
