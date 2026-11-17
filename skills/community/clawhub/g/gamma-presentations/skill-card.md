## Description:

Create presentations, documents, social posts, and websites using Gamma's AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrgoodb](https://clawhub.ai/user/mrgoodb)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create Gamma presentations, documents, social posts, and webpages through Gamma's API, including starting generations, checking completion status, and returning a Gamma URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Gamma API key may be exposed if it is stored in plaintext in an agent-readable project file.

Mitigation: Store the key in the GAMMA_API_KEY environment variable or a secret manager, avoid placing it in TOOLS.md or project documents, and rotate any key previously stored in plaintext.

Risk: Selected user content is sent to Gamma's API when generating presentations, documents, social posts, or webpages.

Mitigation: Use the skill only for content that is appropriate to share with Gamma's API and review sensitive inputs before generation.

## Reference(s):

- [Gamma Developer Documentation](https://developers.gamma.app)
- [Gamma Public API](https://public-api.gamma.app/v1.0)
- [ClawHub Skill Page](https://clawhub.ai/mrgoodb/skills/gamma-presentations)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and returned Gamma URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generation IDs, status polling guidance, optional export parameters, and Gamma document URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
