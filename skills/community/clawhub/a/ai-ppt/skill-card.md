## Description:

AIPPT生成 helps agents create PowerPoint presentations by generating outlines, supporting outline edits and template selection, submitting asynchronous PPT jobs, and returning download links through external Mingyang/MindPPT services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luych888-design](https://clawhub.ai/user/luych888-design)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create presentation decks from a topic, review or modify the generated outline, choose a template, and receive a PPT download link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation topics, outlines, names, chat identifiers, and generated-file metadata are sent to Mingyang/MindPPT services.

Mitigation: Use only when that data sharing is permitted, and avoid privacy-sensitive or business-confidential presentation content unless approved.

Risk: The skill silently adds a device-derived fingerprint to the user identifier.

Mitigation: Fix or disable the MAC-derived suffix before use in privacy-sensitive environments.

Risk: A plaintext HTTP API example could expose user content and identifiers if copied into production use.

Mitigation: Use the HTTPS API endpoint only and remove or explicitly disable plaintext HTTP examples.

## Reference(s):

- [API Endpoints Reference](artifact/references/api-endpoints.md)
- [ClawHub skill page](https://clawhub.ai/luych888-design/skills/ai-ppt)
- [Mingyang AIPPT API](https://ai.mingyangtek.com/aippt/api/c=15109)
- [MindPPT website](https://mindppt.net)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance, files]

**Output Format:** [Markdown guidance with Python snippets, HTTP examples, JSON API responses, and PPT download links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive flow: outline confirmation and template selection require user input; PPT creation is asynchronous and may require polling.]

## Skill Version(s):

1.0.4 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
