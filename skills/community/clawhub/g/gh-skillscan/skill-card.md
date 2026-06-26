## Description: <br>
Scan an OpenClaw SKILL.md file for security threats before installing it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Skillscan to run a local safety check on SKILL.md files before installing them. It reports a safety score, detected threat pattern names, a SAFE/CAUTION/DANGEROUS verdict, and the scanned skill name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill starts a local Python web service. <br>
Mitigation: Keep the service bound to local use and stop it when scanning is complete. <br>
Risk: Submitted SKILL.md files may contain secrets or sensitive content. <br>
Mitigation: Avoid scanning files that contain secrets, credentials, or private operational details. <br>
Risk: The scanner's verdicts are heuristic and may miss threats or flag benign patterns. <br>
Mitigation: Use the verdict as review support and perform manual review before installing a skill. <br>


## Reference(s): <br>
- [Skillscan ClawHub listing](https://clawhub.ai/mirni/gh-skillscan) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, guidance, shell commands] <br>
**Output Format:** [JSON scan response with Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns safety_score, findings, verdict, and skill_name; verdicts are heuristic support for manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
