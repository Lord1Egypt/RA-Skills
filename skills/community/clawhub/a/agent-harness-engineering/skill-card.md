## Description: <br>
Bootstrap or upgrade a software repository for agent-first engineering. Use when a user wants to improve project-wide development discipline around `AGENTS.md`, progressive-disclosure docs, agent-readable architecture/context, mechanical quality checks, CI-enforced structure, or optional garbage-collection/maintenance loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeyitech](https://clawhub.ai/user/yeyitech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to bootstrap or upgrade repositories with agent-readable documentation, quality checks, and optional maintenance reporting. It is intended for repositories that need clearer `AGENTS.md` routing, progressive-disclosure docs, and mechanical guardrails for coding agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bootstrap can make persistent changes to repository documentation, helper scripts, and an optional CLAUDE.md symlink. <br>
Mitigation: Run with `--dry-run`, verify the target `--repo` path, and inspect the resulting diff before committing changes. <br>
Risk: The reviewed package appears to reference template assets that are not included in the artifact. <br>
Mitigation: Confirm the bundled bootstrap assets are present and test the bootstrap in a disposable workspace before using it on a production repository. <br>


## Reference(s): <br>
- [Bootstrap Playbook](references/bootstrap-playbook.md) <br>
- [Docs Blueprint](references/docs-blueprint.md) <br>
- [Quality Gates](references/quality-gates.md) <br>
- [Garbage Collection](references/garbage-collection.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and repository file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bootstrap supports dry-run review and can create or update agent docs, validation scripts, and an optional CLAUDE.md symlink.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
