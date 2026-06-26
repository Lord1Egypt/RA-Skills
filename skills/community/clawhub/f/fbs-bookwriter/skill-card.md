## Description: <br>
FBS-BookWriter helps agents plan, write, review, and export long-form manuscripts such as books, manuals, white papers, industry guides, and long reports through a Node-based writing workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duhongchao-fbsir](https://clawhub.ai/user/duhongchao-fbsir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and agent operators use this skill to manage long-document projects from intake and outline through chapter drafting, quality checks, manuscript cleanup, and Markdown or HTML delivery. It is intended for trusted local project roots where the agent may run the bundled Node scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Node scripts and modify manuscript files. <br>
Mitigation: Install and run it only in a trusted project root, review commands before executing them, and keep backups for important manuscript files. <br>
Risk: The skill may read host profile or memory data and keep persistent writing state. <br>
Mitigation: Review or disable host-profile, host-memory, and auto-preview behavior when tighter privacy or containment is required. <br>
Risk: Admin, publishing, commercial ledger, and self-evolution commands can have broader project or account effects. <br>
Mitigation: Avoid WeCom admin, publish, commercial ledger, and self-evolution commands unless those effects are intended and authorized. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duhongchao-fbsir/fbs-bookwriter) <br>
- [FBS-BookWriter homepage](https://fbs-bookwriter.u3w.com/) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>
- [Version baseline v2.1.2](docs/history/version-baseline-v2.1.2.md) <br>
- [Skill full specification](references/01-core/skill-full-spec.md) <br>
- [Agent task strategy](references/05-ops/agent-task-strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON status from scripts, shell commands, and generated manuscript or delivery files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and npm; optional HTML and document conversion features depend on installed optional dependencies.] <br>

## Skill Version(s): <br>
2.1.2 (source: package.json, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
