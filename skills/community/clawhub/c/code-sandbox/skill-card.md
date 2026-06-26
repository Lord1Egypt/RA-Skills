## Description: <br>
Code Sandbox guides agents in assessing untrusted AI-generated code with sandboxing policies, static risk checks, and execution-result reporting templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and coding agents use this skill to reason about safer handling of untrusted AI-generated code, including resource limits, network and filesystem isolation, static detection of risky patterns, and sandbox execution reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes sandbox behavior but is not itself an enforced sandbox runtime. <br>
Mitigation: Use an actual isolated environment with enforced resource, network, and filesystem controls before running untrusted code. <br>
Risk: Static pattern checks may miss unsafe behavior or reject benign code. <br>
Mitigation: Treat the checks as guidance and review results before execution or deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/534422530/code-sandbox) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable installer is present; outputs are documentation and templates for sandbox review workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
