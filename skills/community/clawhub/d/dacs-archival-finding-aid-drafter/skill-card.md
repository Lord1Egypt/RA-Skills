## Description:

Use this skill when an archivist wants to draft, review, or refine a DACS finding aid for a processed or partly processed archival collection, including ArchivesSpace-ready descriptive notes, EAD3 field mapping, access and use restrictions, reparative-description checks, and archivist sign-off boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Archivists and collections staff use this skill to turn confirmed collection facts into a draft DACS-compliant finding aid for ArchivesSpace or equivalent systems. It supports collection-level descriptions, optional series-level container lists, EAD3 mapping, access and use notes, and required professional review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process confidential donor terms, access restrictions, PII, or culturally sensitive descriptions in the chat.

Mitigation: Use it only when that material is appropriate to discuss in the session, avoid external tool calls for confidential content, and keep generated finding aids in draft review until qualified staff verify them.

Risk: Generated finding aids could contain incorrect access, rights, provenance, or descriptive claims if source facts are incomplete.

Mitigation: Require confirmed collection facts, mark unknowns explicitly, avoid inventing creators, dates, extents, donor terms, restrictions, or rights status, and obtain processing-archivist and head-of-collections sign-off before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/dacs-archival-finding-aid-drafter)
- [Open-Skill-Hub issues](https://github.com/archlab-space/Open-Skill-Hub/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft finding aid with structured notes, tables, and mapping appendix]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are draft-only and require processing-archivist and head-of-collections review before publication, EAD export, PDF release, or access-system push.]

## Skill Version(s):

0.1.3 (source: server release metadata and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
