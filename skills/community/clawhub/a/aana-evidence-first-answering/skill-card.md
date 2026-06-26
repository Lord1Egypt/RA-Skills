## Description: <br>
Guides agents to separate known facts, assumptions, missing evidence, and retrieval steps before answering evidence-sensitive tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this instruction-only skill to review draft answers, recommendations, summaries, and high-impact claims before presenting them. It helps the agent identify known facts, assumptions, unsupported claims, missing evidence, and next retrieval or deferral steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat an evidence review as proof that an answer is correct. <br>
Mitigation: Use the skill as a process aid and verify blocking claims with user-approved tools, records, sources, or human review before relying on the answer. <br>
Risk: Review payloads may include secrets, private records, full logs, private messages, or unrelated private data. <br>
Mitigation: Send only minimal redacted summaries and exclude raw sensitive records whenever a summary is sufficient. <br>
Risk: High-impact decisions may be made from assumptions or unsupported claims. <br>
Mitigation: Ask, retrieve, defer, or refuse unsafe certainty when missing evidence controls legal, medical, financial, purchase, policy, or other high-impact conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-evidence-first-answering) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Review payload schema](artifact/schemas/evidence-first-review.schema.json) <br>
- [Redacted review example](artifact/examples/redacted-evidence-first-review.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with optional JSON review payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it does not execute commands, install dependencies, call services, persist memory, or retrieve evidence by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
