## Description: <br>
Consensus Commons is a multi-agent adversarial decision council that routes intents to finance, strategy, or general panels, runs contrarian review, validates through a 5-state CHP lock machine, and produces auditable decision trails in offline mock mode or live on Spacebase1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zan-maker](https://clawhub.ai/user/zan-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and decision-process owners use this skill to run structured public deliberations for policy, investment, risk, strategy, and governance questions. It routes a submitted intent to a specialist council, records analysis and contrarian review, and returns auditable decision artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce authoritative-looking LOCKED or PASS governance outputs without proving that real validation and review controls were enforced. <br>
Mitigation: Treat outputs as decision-support artifacts, require human approval for consequential decisions, and avoid using lock states as governance assurance by themselves. <br>
Risk: Live Spacebase1 mode can post and lock public decision artifacts using supplied credentials. <br>
Mitigation: Start in mock mode, use scoped and revocable Spacebase credentials, and limit live use to public, low-stakes topics until operational approval controls are in place. <br>
Risk: Submitted topics may include private, confidential, or personal data even though the router attempts to reject such content. <br>
Mitigation: Screen inputs before running the council and use only public or approved low-sensitivity information. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zan-maker/consensus-commons) <br>
- [Project homepage](https://github.com/zan-maker/Consensus-Hardening-Protocol-The-Differ) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON reports, terminal text, Python objects, and Spacebase1 intent metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces council reports with agent contributions, confidence scores, lock states, trace IDs, and audit-trail metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
