## Description:

Spanish conversational skill that guides FÓRMULA 100K students through building a complete content strategy using structured intake questions, public trend research, and a final Markdown strategy document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External Spanish-speaking FÓRMULA 100K students use this skill to turn avatar, offer, content pillars, and public trend research into a complete content strategy and weekly publishing plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share private client data or sensitive business details while answering avatar, offer, account-handle, or research questions.

Mitigation: Avoid providing private client data or sensitive business details unless the user is comfortable sharing the relevant search terms, avatar summary, links, and public account handles with configured providers.

Risk: Research output may depend on connected services, public account availability, and authentication for tools such as web search, Apify, Supadata, or vidIQ.

Mitigation: Disclose unavailable research services, avoid fabricating findings, and generate strategy recommendations from provided avatar and offer inputs when research tools are unavailable.

Risk: Generated content strategy advice can be too generic or misaligned with the student's actual industry if the workflow assumes a marketing niche.

Mitigation: Confirm the student's real industry, preserve domain-specific vocabulary, and use explicit placeholders when business data is missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/creador-estrategia-contenido-formula100k)
- [Fórmula 100K publisher profile](https://clawhub.ai/user/formula100k)
- [Skill definition](artifact/SKILL.md)
- [Cuestionario por Bloques](artifact/cuestionario.md)
- [Frameworks de Referencia](artifact/frameworks.md)
- [Template del Output](artifact/output-template.md)
- [Prompts de Investigación con MCPs](artifact/prompts-investigacion.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Spanish conversational guidance plus a structured Markdown strategy document.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use connected public research services and may save or send a generated strategy file when the host environment supports those actions.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
