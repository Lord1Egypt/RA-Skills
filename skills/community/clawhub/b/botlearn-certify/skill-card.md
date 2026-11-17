## Description:

botlearn-certify compares prior and current BotLearn assessment results and generates capability certificates in HTML and Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to certify an OpenClaw agent's assessed capabilities, compare progress across assessment runs, and produce portable certificate artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install or invoke the botlearn-assessment dependency.

Mitigation: Confirm the dependency source and version before installation or execution.

Risk: The skill reads prior assessment reports and saves certificate files from locally parsed data.

Mitigation: Review assessment report integrity and output locations before relying on generated certificates.

Risk: Generated HTML certificates may reflect manipulated assessment data or unsafe embedded content.

Mitigation: Treat generated HTML as untrusted until assessment inputs and generated output are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvinxhk/skills/botlearn-certify)
- [README](artifact/README.md)
- [Historical assessment retrieval flow](artifact/flows/flow1-historical.md)
- [Fresh assessment flow](artifact/flows/flow2-fresh-exam.md)
- [Certificate generation flow](artifact/flows/flow3-certificate.md)
- [Comparison methodology](artifact/knowledge/comparison-methodology.md)
- [Classification strategy](artifact/strategies/classification.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML and Markdown certificate files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent certificate files based on local assessment results.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
