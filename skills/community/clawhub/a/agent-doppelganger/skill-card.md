## Description: <br>
Constrained autonomous delegate for identity-proxied communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sieershafilone](https://clawhub.ai/user/sieershafilone) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users and developers use this skill to draft, block, or send bounded communication responses across channels such as email, Discord, Slack, and WhatsApp while applying user-defined authority and confidence policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles identity-proxied communications and stores local copies of communications, audit data, and writing-style profiles. <br>
Mitigation: Use it only after reviewing local storage under ~/.openclaw/adg/ and confirming audit logs and retained data can be redacted or deleted as needed. <br>
Risk: Watermarking or provenance behavior may be unclear to message recipients or reviewers. <br>
Mitigation: Confirm watermarking is disabled or clearly disclosed before using the skill for real communications. <br>
Risk: The final safety check may be incomplete or stubbed. <br>
Mitigation: Confirm the verifier is implemented and tested before allowing the skill to send or draft real messages. <br>


## Reference(s): <br>
- [Agent Doppelganger specification](references/specification.md) <br>
- [ClawHub skill page](https://clawhub.ai/sieershafilone/agent-doppelganger) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sieershafilone) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, text responses, Python code, YAML configuration, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May draft, block, or notify based on configured authority, confidence, and escalation policies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
