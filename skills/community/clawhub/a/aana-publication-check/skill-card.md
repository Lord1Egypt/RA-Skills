## Description: <br>
Checks public-facing content for approval, evidence, privacy, asset permissions, quality, and publication risk before an agent publishes or shares it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users apply this skill before publishing posts, reports, documentation, release notes, marketplace copy, or other external content. It helps the agent decide whether to publish, revise, retrieve evidence, ask for approval, route to review, or block publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent could treat draft approval as permission to publish external content. <br>
Mitigation: Require explicit publication approval and route unclear or high-impact cases to review before publishing. <br>
Risk: Sensitive data, private records, secrets, or unapproved third-party material could be included in public content. <br>
Mitigation: Use redacted summaries, check privacy and asset permissions, and block publication when sensitive or unapproved material remains. <br>
Risk: Unsupported claims about products, benchmarks, safety, compliance, medical, legal, or financial topics could mislead readers. <br>
Mitigation: Require evidence for material claims and revise, retrieve sources, or route to domain review when support is missing or stale. <br>
Risk: Connecting the checklist to real publishing tools could create accidental external actions. <br>
Mitigation: Keep final publishing actions explicitly user-approved and send only minimal redacted payloads to trusted configured review systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-publication-check) <br>
- [Publisher profile](https://clawhub.ai/user/mindbomber) <br>
- [Publication check schema](artifact/schemas/publication-check.schema.json) <br>
- [Redacted publication check example](artifact/examples/redacted-publication-check.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain-text publication review with structured status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not execute code, call services, write files, or approve publication by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
