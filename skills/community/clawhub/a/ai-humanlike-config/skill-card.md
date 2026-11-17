## Description:

Helps agents configure humanlike AI digital employees and assistants using guidance for persistent memory, proactive behavior, tool use, role consistency, reflection, planning, memory consolidation, and ongoing improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers, consultants, and AI configuration teams use this skill to design and package digital employees, personal assistants, or AI teachers with memory, tools, persona, and operating boundaries. It also provides supporting scripts for configuration-pack generation, local smoke evaluation, provenance stamping, ID verification, and authorization-code experiments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled authorization utility is unsafe for real authorization, paid capability gating, high-risk approval, or freeze controls.

Mitigation: Treat license_code.py as a prototype only; replace validation, key management, expiry checks, and revocation handling before using it for real controls.

Risk: Persistent memory, reflection, forgetting, and evolution workflows can retain or transform customer, business, or child-related data.

Mitigation: Make these behaviors opt-in, document retention and deletion rules, minimize stored data, and require explicit review before use with sensitive or child-related contexts.

Risk: The bundled audit report says the package is documentation-only even though Python tools are present.

Mitigation: Audit the Python tools directly and review generated local files before installation or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-humanlike-config)
- [Publisher profile](https://clawhub.ai/user/zhaoxinghua09-cell)
- [Methodology](references/00-方法论.md)
- [Diagnostic checklist](references/01-诊断清单.md)
- [Security hardening and control](references/10-安全加固与可控性.md)
- [Authorization-code scheme](references/14-同意授权码方案.md)
- [Capability evaluation and benchmark grading](references/16-能力评测与对标分级.md)
- [Encrypted ID verification service](references/17-加密ID认证服务.md)
- [One-click configuration package](references/31-一键配置到任意大模型.md)
- [Layered persistent memory](references/32-记忆分层与持久化.md)
- [D1-D4 design roadmap](references/40-设计层待补项与路线图(D1-D4).md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python tool scripts that emit JSON, text reports, and generated configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some bundled tools write local files such as configuration packs, credentials, certificates, revocation lists, timestamps, or evaluation reports when invoked.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
