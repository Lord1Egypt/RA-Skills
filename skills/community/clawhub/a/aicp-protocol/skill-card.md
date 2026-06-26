## Description: <br>
AI Compact Protocol (AICP) - Token-efficient wire format for AI-to-AI communication with glossary compression. Reduces token usage by 50-65% for agent chatter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krischristen-hash](https://clawhub.ai/user/krischristen-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to encode, parse, and demonstrate compact AI-to-AI messages for multi-agent workflows. It is useful when agents need a lightweight wire format with glossary compression instead of verbose JSON-like chatter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AICP messages could trigger unintended create, update, delete, or query actions if connected directly to real agent operations. <br>
Mitigation: Require sender validation and explicit approval before using parsed AICP messages for impactful operations. <br>
Risk: Compact glossary terms can obscure intent when humans review an agent message. <br>
Mitigation: Expand glossary terms into human-readable form before approval or audit. <br>


## Reference(s): <br>
- [AICP Protocol homepage](https://github.com/christen-family/aicp-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; runtime helpers output wire-format text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; no external Python dependencies are listed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
