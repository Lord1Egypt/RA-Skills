## Description:

Entry skill of the chatMOSP system that parses Chinese and English natural-language requests, recognizes MSR, KMC, and parameter-query tasks, extracts simulation parameters, and dispatches companion ChatMOSP skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanyangye](https://clawhub.ai/user/sanyangye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and simulation engineers use this skill as the entry coordinator for ChatMOSP workflows. It turns Chinese or English requests for metal-cluster structure generation, kinetic Monte Carlo simulation, or parameter lookup into confirmed task routing and parameter handoff steps for companion skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The coordinator delegates real simulation and file-generation work to companion ChatMOSP skills.

Mitigation: Review and install the required companion skills separately before using this coordinator for production workflows.

Risk: Server security evidence notes bilingual language-routing and documentation mistakes.

Mitigation: Verify Chinese and English routing behavior before relying on the skill in multilingual workflows.

Risk: The artifact states that EKMC, slab KMC, Stepwise EKMC, server submission, and job monitoring are unsupported in this release.

Mitigation: Ask users to choose the supported MSR, KMC, or parameter-query workflows, and do not route unsupported requests to missing skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanyangye/skills/chatmosp-input-coordinator)
- [English skill instructions](artifact/SKILL.md)
- [Chinese skill instructions](artifact/SKILL_cn.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Natural-language responses with task confirmations, clarification prompts, routing guidance, and parameter summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates companion skills for file generation and simulation execution; complete operation depends on those companion skills being installed]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
