## Description: <br>
Packages and sanitizes an agent workspace's configuration files, submits them for a Claw Score audit, and sends a detailed architecture report by email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonnyfmiller](https://clawhub.ai/user/jonnyfmiller) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to submit selected agent configuration files for an external architecture audit. The report scores identity, memory, security, autonomy, proactive behavior, and learning patterns, then returns recommendations and quick wins by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive workspace and agent-context files to an external audit service. <br>
Mitigation: Review the exact file list and sanitized payload before confirming submission, and avoid use on workspaces containing secrets, private notes, customer data, or internal security instructions. <br>
Risk: Automatic redaction may not catch every sensitive value or context-specific secret. <br>
Mitigation: Manually inspect the previewed payload and remove any remaining sensitive content before submission. <br>
Risk: Fallback manual submission can expose audit materials through email. <br>
Mitigation: Use the fallback only with content you are comfortable sending by email, and keep the recipient and attachments limited to the intended audit package. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jonnyfmiller/claw-score) <br>
- [Atlas Audit Landing Page](https://atlasforge.me/audit) <br>
- [AtlasForgeAI on X](https://x.com/AtlasForgeAI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Terminal status text and an emailed Markdown audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submits selected Markdown configuration files and a workspace file tree after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
