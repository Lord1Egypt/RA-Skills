## Description: <br>
Agent-Selector selects and loads an appropriate expert persona from a bundled library of 146+ agent prompts based on the user's task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Krislu1221](https://clawhub.ai/user/Krislu1221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route tasks to a more specialized persona, load the matching prompt, and return to a default identity after the task is complete. It is suited for local prompt selection and persona guidance, including coding, design, marketing, testing, project management, and other specialist workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled personas may suggest sensitive actions such as payments, production deployments, social posting, analytics export, or customer-data handling without enough approval detail. <br>
Mitigation: Keep sensitive tools disabled by default and require explicit human approval, privacy/legal review, audit logging, and least-privilege tool scopes before granting those capabilities. <br>
Risk: Prompt loading may fail or load an unexpected set of prompts because scanner guidance notes a possible mismatch between the selector's expected bundled-agent path and the package contents. <br>
Mitigation: Verify prompt loading in the target runtime before deployment and confirm the selector points only to the intended bundled prompt directory. <br>
Risk: The broad persona library can produce domain-specific guidance that appears authoritative outside the user's expertise. <br>
Mitigation: Use the selected persona output as draft guidance and require domain-owner review for legal, compliance, security, medical, finance, deployment, or public-communications decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Krislu1221/agent-selector) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Release README](artifact/README.md) <br>
- [ClawHub package metadata](artifact/clawhub.json) <br>
- [Bundled agent library README](artifact/agency-agents/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, selected agent identifiers, and prompt text with occasional code or shell examples from bundled personas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local bundled prompt files, uses keyword-based selection, and caches loaded prompts; no external API use is declared.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
