## Description: <br>
Converts template strings containing @parameter@ placeholders into concrete smart access-control parameter values for Future Window door-system workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberwin](https://clawhub.ai/user/cyberwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn access-control text templates into populated strings using supplied device, permission, area, or similar parameter values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied templates and parameter values are inserted directly into the output text. <br>
Mitigation: Use trusted templates and validated parameter values before applying generated text in real access-control workflows. <br>


## Reference(s): <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>
- [ClawHub skill page](https://clawhub.ai/cyberwin/future-window-access-param-convert) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON object containing success, message, and data fields, where data is the converted text string.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Unmatched placeholders are preserved in the output text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
