## Description: <br>
Markdown-first guidance that helps coding agents handle repeated failures, evidence requests, scoped edits, silent delays, confusion, and closeout by loading the relevant playbook reference and applying safer response behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongyu0918-debug](https://clawhub.ai/user/gongyu0918-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make coding agents respond more reliably during debugging, review, scoped editing, stalled work, and post-fix closeout. It provides routing guidance, response constraints, prompt snippets, examples, integration notes, and forward-test scenarios for Markdown-first behavior overlays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad implicit invocation may shape coding-agent behavior in conversations where the user did not explicitly request this skill. <br>
Mitigation: Use the routing playbook to apply only the relevant behavior pattern, keep scope explicit, and make evidence, boundaries, and closeout checks visible to the user. <br>
Risk: The playbook changes agent response behavior but cannot prove by itself that a fresh agent will follow the intended route correctly. <br>
Mitigation: Use the subagent forward-test protocol and score behavior against route accuracy, reference selection, soft-constraint handling, and verification honesty before relying on the skill in sensitive workflows. <br>


## Reference(s): <br>
- [Routing Playbook](references/routing-playbook.md) <br>
- [Response Constraints](references/response-constraints.md) <br>
- [Real Scenarios](references/real-scenarios.md) <br>
- [Subagent Forward Tests](references/subagent-forward-tests.md) <br>
- [Model Prompt Snippets](references/model-prompts.md) <br>
- [Integration Notes For OpenClaw And Hermes](references/integration-openclaw-hermes.md) <br>
- [Examples](references/examples.md) <br>
- [Emotion Value Model](references/emotion-value-model.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with optional prompt snippets and YAML agent configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only behavior playbook; no runtime classifier or hidden script execution is required for normal use.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
