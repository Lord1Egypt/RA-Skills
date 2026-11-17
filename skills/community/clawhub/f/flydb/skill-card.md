## Description:

Routes Flydb database migration requests to the appropriate companion skill for CLI setup, migration execution, script management, web or MCP workflows, multi-environment CI, and FLYDB error triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzxcoding](https://clawhub.ai/user/zzxcoding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to choose the right Flydb companion workflow for onboarding, migration execution, migration script governance, multi-environment CI, and error triage without duplicating detailed procedures from companion skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install examples fetch related skills from mutable remote sources.

Mitigation: Verify the GitHub or SkillHub source before installation and prefer a pinned commit or trusted release when available.

Risk: Companion workflows may involve production database credentials or write-capable migration operations.

Mitigation: Avoid installing or running migration-related skills in environments that already expose production database credentials unless that access is intended; require dry-run review and explicit authorization before write operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzxcoding/skills/flydb)
- [Flydb GitHub project](https://github.com/zzxCoding/Flydb)
- [Flydb Gitee mirror](https://gitee.com/zzhenxuan/Flydb)
- [Flydb skills repository](https://github.com/zzxCoding/skills)
- [SkillHub install guide](https://skillhub.cn/install/skillhub.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with routing tables and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes requests to companion skills and keeps detailed command parameters, naming rules, and environment organization patterns in those companion skills.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
