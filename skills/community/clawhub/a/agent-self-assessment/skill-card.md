## Description: <br>
Provides a tool-free AI agent security and compliance self-assessment that produces a RED/AMBER/GREEN report from the agent's existing context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roosch269](https://clawhub.ai/user/roosch269) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use this skill to structure a conservative self-assessment against AI security, governance, Zero Trust, supply-chain, inter-agent trust, and compliance-readiness checks. It is intended for risk visibility and remediation planning, not certification or legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The assessment could be mistaken for a formal audit, certification, or legal compliance determination. <br>
Mitigation: Treat the report as advisory risk visibility, verify framework obligations against official sources, and involve qualified security or legal reviewers before making compliance claims. <br>
Risk: Unknown controls may be scored as gaps because the skill only uses information already present in the agent context. <br>
Mitigation: Use RED or Cannot verify results as follow-up prompts for evidence gathering rather than as final proof that a control is absent. <br>
Risk: Optional AGIRAILS package-install references introduce separate dependency and transaction-infrastructure decisions. <br>
Mitigation: Run those install commands only when the transaction infrastructure is independently needed and after reviewing the packages, dependencies, and wallet or payment implications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roosch269/agent-self-assessment) <br>
- [AGIRAILS documentation](https://docs.agirails.io) <br>
- [AGIRAILS Python SDK](https://pypi.org/project/agirails/) <br>
- [AGIRAILS SDK Python repository](https://github.com/agirails/sdk-python) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured RED/AMBER/GREEN assessment report in plain text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory output based only on the agent's current context; the skill itself does not use tools, read files, make network calls, or change state.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
