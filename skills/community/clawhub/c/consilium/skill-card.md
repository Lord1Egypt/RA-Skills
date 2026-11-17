## Description:

Consilium helps an agent route hard questions to a 3-5 model advisory panel, collect independent analyses, and synthesize consensus, disagreements, minority opinions, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morozsm](https://clawhub.ai/user/morozsm)

### License/Terms of Use:


## Use Case:

Developers and other agent users use this skill when they want multi-model analysis of complex decisions, architecture choices, strategy, disputes, or other questions where independent perspectives can expose blind spots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User questions are sent to several configured model providers and may be stored according to normal OpenClaw session settings.

Mitigation: Use only trusted providers in the panel and rerun model selection with --models when controlling which models receive the question matters.

Risk: Independent model advice can still be incomplete, inconsistent, or misleading for high-impact decisions.

Mitigation: Treat the synthesis as advisory input and review the consensus, disagreements, and minority opinions before acting.

## Reference(s):

- [Council Protocol Details](references/PROTOCOL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown synthesis with structured sections, attributed panelist summaries, consensus, disagreements, minority opinions, and action items; may also maintain a JSON panel configuration file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Panelist prompts cap individual responses at 800 words and optional debate rebuttals at 400 words.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
