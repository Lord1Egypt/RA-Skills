## Description:

Redesign and beautify PowerPoint/PDF presentation decks into polished, on-brand slides using Deckly's AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmymelbj](https://clawhub.ai/user/jimmymelbj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an AI agent through Deckly-powered presentation analysis, style selection, preview, fine-tuning, rendering, and download for PowerPoint or PDF decks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation content is uploaded to Deckly for analysis and redesign.

Mitigation: Do not use the skill on confidential decks without data-handling approval.

Risk: The workflow can handle Deckly passwords, verification codes, and long-lived API keys.

Mitigation: Prefer a pre-created Deckly API token, avoid entering passwords or verification codes directly in chat when possible, and review or revoke saved API keys after use.

Risk: Full redesign and fine-tuning actions can spend Deckly credits.

Mitigation: Check balance and free-preview status before paid actions, use quote before redesigning, and confirm the credit cost with the user before continuing a paid render.

Risk: Changing DECKLY_API_BASE can send presentation files and credentials to a different service.

Mitigation: Use the default Deckly endpoint unless the alternate API base is explicitly trusted.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/jimmymelbj/deckly-redesign-skill)
- [ClawHub skill page](https://clawhub.ai/jimmymelbj/skills/deckly-redesign-skill)
- [Deckly service](https://deckly.art)
- [Deckly API reference](reference.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload presentation files to Deckly, persist an API key locally, and download a redesigned PPTX file.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
