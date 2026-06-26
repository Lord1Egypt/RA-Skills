## Description: <br>
基于 OpenAI《Harness Engineering》实践的 Codex 工作规范。强调环境能力补齐、仓库即记录系统、严格分层架构、可观测可验证闭环、持续防漂移治理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmypeng4ios](https://clawhub.ai/user/jimmypeng4ios) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide Codex through multi-step, cross-file software work with repository-backed documentation, PR review loops, observable validation, architecture boundaries, and drift control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository write access, CI permissions, GitHub tokens, or observability credentials could be over-scoped when applying this workflow guidance. <br>
Mitigation: Grant least-privileged access for each repository and tool, and review permissions before allowing PR automation, background scans, or refactor tasks. <br>
Risk: Agent-generated PRs, scans, or refactors could introduce incorrect guidance or unintended repository changes. <br>
Mitigation: Require human review before PRs are merged or recurring background tasks are allowed to run. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jimmypeng4ios/codex-harness-engineering) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance for agent workflow and repository governance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable installer or runtime behavior is included in the artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
