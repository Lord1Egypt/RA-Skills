## Description:

Audits repositories and plans an AI-native development workflow, with opt-in scaffolding, fail-closed checks, and auditable reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect a repository and plan adoption of an auditable AI-native workflow, then optionally create project guidance and local verification entrypoints. They review real checks and retain responsibility for production approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release suspicious and reports concerns about instructions that could authorize repository changes by default; the scan is partial because two referenced paths were missing.

Mitigation: Review the complete skill and its referenced files before installing, and confirm that repository writes require explicit authorization in the target workflow.

Risk: The security summary reports a concern that evaluation failures may be recorded as passes.

Mitigation: Review the evaluation behavior and verify that real configured failures remain visible before relying on its results.

Risk: The security guidance says the partial scan does not establish safety, including from its clean persistence rating.

Mitigation: Treat the suspicious verdict as unresolved until the missing paths are accounted for and the relevant security concerns have been reviewed.

## Reference(s):

- [AI Native Bootstrap on ClawHub](https://clawhub.ai/qomob/skills/ai-native-bootstrap)
- [Implementation standard](artifact/references/implementation-standard.md)
- [Adapters and safety](artifact/references/adapters-and-safety.md)
- [OpenAI CLI reference](https://developers.openai.com/api/reference/cli)
- [OpenAI skills and Agents SDK](https://developers.openai.com/blog/skills-agents-sdk)
- [OpenCode skills documentation](https://opencode.ai/docs/skills)
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Configuration files, Shell commands]

**Output Format:** [Repository audit and planning reports, project guidance and configuration templates, and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project checks and evaluation cases require project-specific review and configuration; unconfigured checks are reported as BLOCKED.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
