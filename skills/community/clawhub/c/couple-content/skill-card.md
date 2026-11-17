## Description:

Hosts a couples compatibility quiz, records participant answers, and, when privately asked by the initiator, suggests surprise or gift ideas based on those answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[padepa](https://clawhub.ai/user/padepa)

### License/Terms of Use:

MIT

## Use Case:

External users can run a couples quiz, capture the participant's answers, and later receive evidence-based surprise or gift suggestions when the initiator asks privately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A participant may not understand that quiz answers are retained and later used for private gift or surprise recommendations.

Mitigation: Use the skill only when every participant understands that answers may be recorded, summarized, and reused for recommendations.

Risk: Hidden-mode instructions can conflict with informed-consent expectations.

Mitigation: Do not rely on the hidden-mode flow where informed consent is required; disclose the recording and later recommendation use before collecting answers.

Risk: Untrusted JSON inputs to the renderer can produce misleading published Markdown.

Mitigation: Use trusted or reviewed JSON inputs with the renderer and prefer a pinned install command for release use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/padepa/skills/couple-content)
- [couple-content-prompt.md](references/couple-content-prompt.md)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Conversational text and structured JSON that can be rendered to Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gift suggestions should cite answer evidence, indicate confidence, ask for missing constraints, and avoid real-time price or inventory claims.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
