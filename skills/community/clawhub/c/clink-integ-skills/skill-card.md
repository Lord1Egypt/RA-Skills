## Description: <br>
Design, scaffold, validate, and review Clink standard integrations, new user onboarding, merchant skill for generic agent integrations, merchant skill for OpenClaw integrations, and documentation-backed contracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanclink](https://clawhub.ai/user/dylanclink) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to plan, scaffold, validate, and review Clink payment integrations. It supports standard checkout, onboarding, OpenClaw and generic agent payment paths, documentation-backed API questions, and developer-facing artifacts such as checklists, contracts, and validation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide use of Clink Secret Keys, webhook signing keys, wallet tooling, or payment tooling. <br>
Mitigation: Use environment variables or a secret manager and do not paste real secrets into chat, fixtures, generated source, logs, or public repositories. <br>
Risk: Docs or payment-skill context can be loaded from override URLs or external sources. <br>
Mitigation: Keep the default Clink documentation sources unless the override location is trusted. <br>
Risk: LLM-backed tests can send included context to the configured provider. <br>
Mitigation: Run LLM-backed tests only when the provider and submitted context are acceptable for the release environment. <br>
Risk: Production payment guidance can affect checkout, webhook, and customer verification behavior. <br>
Mitigation: Use sandbox defaults and complete the validation workflow before production rollout guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dylanclink/clink-integ-skills) <br>
- [Clink official docs export](https://docs.clinkbill.com/llms-full.txt) <br>
- [README](README.md) <br>
- [Retrieval protocol](references/retrieval-protocol.md) <br>
- [Standard integration](references/standard-integration.md) <br>
- [Generic agent integration](references/generic-agent-integration.md) <br>
- [OpenClaw agent integration](references/agent-integration.md) <br>
- [Validation workflow](references/validation-workflow.md) <br>
- [Output artifacts](references/output-artifacts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown responses with code blocks, JSON contract skeletons, checklists, validation reports, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May load current Clink documentation or payment-skill context before producing integration-specific guidance] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
