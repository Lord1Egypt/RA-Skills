## Description: <br>
A reasoning and coaching skill that helps agents investigate why an existing rule, process, code path, or institution exists before recommending removal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, policy reviewers, and organizational decision makers use this skill when a rule, process, code path, or practice is proposed for removal. It guides the agent to identify the fence, investigate its origin, judge whether the original problem still applies, and document a remove, modify, keep, or replace decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may slow or challenge removal proposals even when stakeholders are under time pressure. <br>
Mitigation: Use the skill to document the investigation path and decision criteria, then proceed once the original purpose and current applicability are explicit. <br>
Risk: If history is unavailable, a confident removal recommendation could miss a load-bearing purpose. <br>
Mitigation: Prefer a small reversible experiment with monitoring, removal notes, and rebuild criteria when the original rationale cannot be recovered. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/chestertons-fence) <br>
- [Sources - chestertons-fence](artifact/references/sources.md) <br>
- [Method in Action: Chesterton 1929 and the Modern Software / Regulatory Application](artifact/examples/chesterton-1929-and-the-modern-software-regulatory-application.md) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance and structured investigation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask step-by-step questions before producing a final investigation summary and decision record.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
