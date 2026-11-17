## Description:

Chemvision helps agents answer chemistry questions by using PubChem and OPSIN-backed tools for chemical names, SMILES, formulas, molecular weights, GHS safety information, molecular structure images, and reaction support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panda-lsy](https://clawhub.ai/user/panda-lsy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and chemistry-focused agent operators use this skill to look up compound structures, safety information, and reaction context while reducing unsupported chemistry answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chemistry queries may be processed through a local service that can query PubChem or OPSIN, despite conflicting local-only statements in the artifact.

Mitigation: Avoid confidential or proprietary chemistry queries unless the service implementation has been audited or configured for confirmed local-only operation.

Risk: The server security verdict is suspicious because data handling statements are inconsistent.

Mitigation: Review service configuration and data-flow behavior before deployment, and disclose external lookup behavior to users where applicable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panda-lsy/skills/chemvision-skill)
- [Server-resolved GitHub source repository](https://github.com/panda-lsy/chemvision-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/panda-lsy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Files, Guidance]

**Output Format:** [Markdown and text with inline shell commands, JSON API payloads, and generated image file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local service endpoints and generated molecular structure or chemical equation images.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact metadata reports skill_version 3.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
