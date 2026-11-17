## Description:

CMMI V3.0 Certification Assistant helps PM and EPG teams match project documents to CMMI V3.0 Practice Areas, identify missing evidence, and generate compliant document drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers, EPG teams, and process quality staff use this skill to prepare CMMI V3.0 appraisal evidence by matching uploaded project documents to Practice Areas, reviewing gaps, and drafting compliant document structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically reads uploaded project documents, which may contain confidential project or appraisal evidence.

Mitigation: Use only approved documents, keep generated drafts in an approved workspace, and review outputs before sharing.

Risk: PA mappings and generated templates may be inaccurate or inconsistent for some Practice Areas.

Mitigation: Have a PM, EPG, or quality reviewer validate PA mappings and generated content, especially EVW, MST, ESAF/ESAC, and PCM/PCMD references, before appraisal use.

Risk: Generated compliance documents are drafts and may contain placeholders rather than complete evidence.

Mitigation: Fill missing project-specific evidence and perform a certification-readiness review before relying on the documents.

## Reference(s):

- [Skill README](README.md)
- [CMMI Practice Area Knowledge Base](references/PA_knowledge/)
- [PA Document Template Configuration](scripts/pa_config.json)
- [ClawHub Skill Page](https://clawhub.ai/kooui/skills/cmmi-cert-assistant-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional .docx files generated from PA templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read uploaded project documents and create derivative CMMI compliance drafts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
