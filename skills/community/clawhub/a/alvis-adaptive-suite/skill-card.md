## Description:

Adaptive Suite helps Clawdbot provide coding, business analysis, project management, web and data development, free-resource discovery, and read-only NAS metadata scanning guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and project teams use this skill for adaptive coding support, business analysis, project management, web and data development, and resource-discovery guidance. It can also guide creation of a read-only local app for NAS metadata scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task context or sensitive data could be sent to external SkillBoss API services.

Mitigation: Use only with non-sensitive context unless explicit consent is obtained, and restrict what data, files, and environment details may be shared.

Risk: NAS metadata scanning could expose filenames, directory structure, or other private operational details.

Mitigation: Run generated scanners in read-only mode, limit scans to approved paths, and review collected metadata before sharing or storing it.

Risk: Broad coding, business, and project-management guidance could be inaccurate or unsuitable for a specific environment.

Mitigation: Review recommendations against project requirements, security policy, and domain expertise before implementation.

## Reference(s):

- [Moltbot Skills Documentation](https://docs.molt.bot/tools/skills)
- [SkillBoss API Hub Endpoint](https://api.SkillBoss.co/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose use of external SkillBoss API services and may generate guidance for a read-only local NAS metadata scanner.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
