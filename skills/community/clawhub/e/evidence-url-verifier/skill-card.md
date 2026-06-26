## Description: <br>
Verify evidence URLs are real and accessible. Check that artifact links resolve to actual content, not placeholders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and reviewers use this skill to verify that evidence URLs and local artifact references resolve to substantive, expected content before completing or auditing a task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checking private tokenized URLs, internal network addresses, or sensitive local paths can disclose limited reachability or existence information. <br>
Mitigation: Only verify sensitive links or paths when that disclosure is acceptable, and avoid logging full URL contents. <br>
Risk: Repeated URL checks can create unnecessary load or violate rate limits. <br>
Mitigation: Respect the skill's rate-limit guidance of no more than one request per second. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Dalomeve/evidence-url-verifier) <br>
- [Dalomeve Publisher Profile](https://clawhub.ai/user/Dalomeve) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown guidance with inline PowerShell examples and verification criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces validation steps, example commands, warnings, and completion criteria for URL and artifact checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
