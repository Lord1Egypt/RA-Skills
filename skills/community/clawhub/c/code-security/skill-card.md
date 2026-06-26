## Description: <br>
Reviews application code in the current workspace for concrete security issues and provides proportionate, actionable fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sf0799](https://clawhub.ai/user/sf0799) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit application code for security issues such as injection, authorization flaws, path traversal, XSS, command execution, and sensitive data leaks, then receive prioritized fixes or code suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to inspect workspace code, which may expose secrets or sensitive code to the agent context. <br>
Mitigation: Use it only on repositories you are comfortable having an agent inspect, and scope reviews to specific files or directories when sensitive material is present. <br>
Risk: Generated security findings and patches may be incomplete or incorrect. <br>
Mitigation: Review and test proposed fixes before merging, and follow up on any residual risks the skill identifies. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown security review with risk levels, impact notes, fixes, and code suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include actionable patches or residual risk notes when a risk cannot be fully closed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
