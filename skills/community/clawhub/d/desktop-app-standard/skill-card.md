## Description:

Build, maintain or audit Tauri/Electron desktop apps, including dependencies, packaging, updates and CI. Next.js shell migration uses the corresponding nextjs-to-tauri or nextjs-to-electron Skill. 支持只读巡检，以及明确请求的 .NET SDK/TFM 静态审计；局部修复也检查已采用的建议依赖升级。

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockbenben](https://clawhub.ai/user/rockbenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit, build, maintain, and release Tauri or Electron desktop applications. It also supports read-only .NET SDK and target framework audits and provides findings, checks, and workflow guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some skill components were only partially inspected by the security scan, so evidence for those portions is incomplete.

Mitigation: Review the uninspected script portions before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rockbenben/skills/desktop-app-standard)
- [Project homepage](https://github.com/rockbenben/aishort-skills/tree/main/skills/desktop-app-standard)
- [Tauri guidance](artifact/references/tauri.md)
- [Electron guidance](artifact/references/electron.md)
- [Release flow guidance](artifact/references/release-flow.md)
- [CI traps reference](artifact/references/ci-traps.md)
- [Official .NET release metadata](https://builds.dotnet.microsoft.com/dotnet/release-metadata/releases-index.json)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown guidance, text or JSON audit reports, and code or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the requested audit, implementation, or release task.]

## Skill Version(s):

0.9.22 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
