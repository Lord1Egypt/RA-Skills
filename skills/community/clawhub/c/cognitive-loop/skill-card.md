## Description: <br>
Cognitive Loop helps an agent plan, execute, reflect on, and test multi-step work such as software development, refactoring, error recovery, and validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[world-peace001](https://clawhub.ai/user/world-peace001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to structure complex tasks into planning, monitored execution, reflection, and testing loops while retaining user confirmation for higher-impact actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be broadly triggered for planning and multi-step work, which may lead an agent to act beyond the current request or make persistent memory changes. <br>
Mitigation: Invoke the skill explicitly for relevant tasks and require confirmation before writing memory, making persistent changes, or acting beyond the current request. <br>
Risk: The artifact recommends installing and reviewing external GitHub and npm resources, while server-resolved provenance is unavailable for this release. <br>
Mitigation: Treat external project links as references only and verify package integrity and source before use. <br>


## Reference(s): <br>
- [Cognitive Agent GitHub repository](https://github.com/World-peace001/cognitive-agent) <br>
- [cognitive-agent npm package](https://www.npmjs.com/package/cognitive-agent) <br>
- [Cognitive Loop on ClawHub](https://clawhub.ai/world-peace001/cognitive-loop) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code and command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent memory updates under memory/ paths and should request confirmation before making persistent changes or acting beyond the current request.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
