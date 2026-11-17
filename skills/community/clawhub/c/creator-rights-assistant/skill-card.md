## Description:

Use when a creator, manager, or label is finalizing an asset and wants a clean, standards-mapped record of its origin, authorship context, licensing scope, attribution requirements, and integrity signals, or wants to track license durations, territories, expirations, source-material permissions, and rights transfers across a catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otherpowers](https://clawhub.ai/user/otherpowers)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, managers, labels, and their supporting agents use this skill before publication to create or maintain an Asset Origin Record for a creative work. The record captures origin, attribution, licensing scope, source-material permissions, integrity signals, and lifecycle notes without adjudicating ownership or providing legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Asset Origin Records may contain sensitive rights, collaborator, licensing, and dispute context.

Mitigation: Keep sidecar files under the creator's control and use minimal exports unless there is a clear reason to share more.

Risk: Rights questions can carry legal weight, and the skill does not validate licenses, ownership, infringement, or legal outcomes.

Mitigation: Use the skill for documentation and seek qualified legal counsel for rights questions with legal weight.

Risk: Embedded metadata can expose names, identity details, and collaborator information beyond the creator's intended audience.

Mitigation: Respect consent limits, keep identity-sensitive details out of embedded copies by default, and avoid naming collaborators without consent.

## Reference(s):

- [Creator Rights Assistant on ClawHub](https://clawhub.ai/otherpowers/skills/creator-rights-assistant)
- [C2PA explainer, specification 2.4](https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html)
- [C2PA FAQ](https://c2pa.org/faqs/)
- [Local Contexts labels](https://localcontexts.org/labels/about-the-labels/)
- [Local Contexts Traditional Knowledge Labels](https://localcontexts.org/labels/traditional-knowledge-labels/)
- [Content Credentials](https://en.wikipedia.org/wiki/Content_Credentials)
- [IPTC metadata](https://en.wikipedia.org/wiki/IPTC_Information_Interchange_Model)
- [XMP](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform)
- [Creative Commons](https://en.wikipedia.org/wiki/Creative_Commons)
- [SPDX](https://en.wikipedia.org/wiki/Software_Package_Data_Exchange)
- [Local Contexts](https://localcontexts.org/)
- [ISRC](https://en.wikipedia.org/wiki/International_Standard_Recording_Code)
- [ISWC](https://en.wikipedia.org/wiki/International_Standard_Musical_Work_Code)
- [IPI](https://en.wikipedia.org/wiki/Interested_Parties_Information)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration]

**Output Format:** [Markdown guidance and plain-text or JSON sidecar records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces creator-controlled Asset Origin Records, commonly as asset.abc.json, with fields marked when information is not yet recorded.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
