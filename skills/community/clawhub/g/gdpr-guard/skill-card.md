## Description: <br>
GDPR Guardrail detects personal data in AI application inputs and outputs, then masks, reports, or blocks findings based on risk level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwumit](https://clawhub.ai/user/wwumit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as a local runtime guardrail for AI applications that need to detect, mask, or block GDPR-relevant personal data before model input or user-facing output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex and keyword matching can produce false positives, including broad health identifier matches and examples outside the stated GDPR scope. <br>
Mitigation: Review and tune the rule pack for the target jurisdiction and workflow before using block mode. <br>
Risk: The skill is a compliance aid and should not be treated as legal advice or a complete compliance control. <br>
Mitigation: Use it alongside organizational review, legal guidance, and broader data protection controls. <br>
Risk: Strict enforcement can interrupt valid workflows when rule precision is not yet validated for local data. <br>
Mitigation: Start with detect or mask mode and promote to block mode only after reviewing observed findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwumit/skills/gdpr-guard) <br>
- [Publisher profile](https://clawhub.ai/user/wwumit) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON command output from detect, mask, and block modes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include risk level, finding count, masked previews, decision, and masked or blocked output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
