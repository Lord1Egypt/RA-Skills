## Description: <br>
One-directional knowledge bridge from Google Antigravity IDE to OpenClaw that syncs Markdown documentation from configured Antigravity or Gemini projects into an OpenClaw workspace for native vector indexing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heintonny](https://clawhub.ai/user/heintonny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to pull Antigravity or Gemini project notes, rules, tasks, and documentation into OpenClaw so memory_search can index and query that context. It is useful for cross-project awareness after Antigravity sessions or scheduled local syncs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured syncs can copy and index sensitive local Markdown notes into OpenClaw. <br>
Mitigation: Run the dry run first, keep source paths narrow, and review Markdown content for secrets or private session notes before regular use. <br>
Risk: Markdown-only transfer does not guarantee that copied files are free of credentials or private context. <br>
Mitigation: Avoid broad knowledge directories unless needed and exclude or remove Markdown files that contain secrets, credentials, or confidential session notes. <br>
Risk: Cron-based syncing can continuously refresh indexed content without further review. <br>
Mitigation: Enable cron only when continuous indexing is acceptable for the workspace and periodically audit the configured sources and destination. <br>


## Reference(s): <br>
- [Antigravity Bridge on ClawHub](https://clawhub.ai/heintonny/antigravity-bridge) <br>
- [yq YAML parser](https://github.com/mikefarah/yq) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May copy local Markdown files into the OpenClaw workspace when the sync script is executed.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
