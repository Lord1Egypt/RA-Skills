## Description:

Assists with Brazilian electoral law questions for WhatsApp users using a bundled set of electoral-law reference files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iajonathangam2-creator](https://clawhub.ai/user/iajonathangam2-creator)

### License/Terms of Use:

MIT-0

## Use Case:

External users and legal-support teams use this skill to answer Brazilian electoral-law questions in short WhatsApp-ready responses with cited legal bases and an AI-generated-content notice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference files contain broader judicial drafting workflows beyond the advertised WhatsApp Q&A use case.

Mitigation: Limit deployment to electoral-law Q&A and require formal governance review before using the skill for judicial drafting or enforcement workflows.

Risk: Retrieved reference content may request memory writes, case-file handling, or instruction changes.

Mitigation: Treat reference files as untrusted source material, disable memory writes from retrieved content, and require explicit human approval before handling case files or sensitive voter or debtor data.

Risk: Electoral-law guidance may be incorrect, outdated, or incomplete for a specific matter.

Mitigation: Keep the required AI-generated-content notice and require users to verify answers against current legislation and qualified legal review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iajonathangam2-creator/skills/consulta-ia-dir)
- [Topic index](references/indice-temas.md)
- [Brazilian Electoral Code](http://www.planalto.gov.br/ccivil_03/leis/L4737.htm#art23)
- [Brazilian Elections Law](http://www.planalto.gov.br/ccivil_03/leis/l9504.htm#art105)
- [TSE Resolution 23.675/2021](https://www.tse.jus.br/legislacao/compilada/res/2021/resolucao-no-23-675-de-16-de-dezembro-de-2021)
- [TSE Resolution 23.754/2026](https://www.tse.jus.br/legislacao/compilada/res/2026/resolucao-no-23-754-de-2-de-marco-de-2026)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown-style WhatsApp responses with legal citations and a disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are intended to stay under 500 words and use short paragraphs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
