## Description: <br>
Enterprise Security Suite provides OpenClaw helpers for high-risk operation prompts, file backups, rollback, changelog logging, and skill-installation checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gk752448784](https://clawhub.ai/user/gk752448784) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add operational guardrails around file changes, rollbacks, change logging, and skill-installation review in OpenClaw environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The main confirmation safeguard currently auto-approves high-risk actions instead of waiting for explicit approval. <br>
Mitigation: Do not rely on this version to block high-risk actions; require an external manual confirmation step or patch confirmHighRisk before deployment. <br>
Risk: The activation script persistently changes agent memory through shell-driven writes to a local pgmemory Docker/Postgres setup. <br>
Mitigation: Run activate.js only when those persistent rules are intended, and plan how to inspect or remove the inserted memory records during uninstall or rollback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gk752448784/enterprise-security-suite) <br>
- [Publisher profile](https://clawhub.ai/user/gk752448784) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Console text, Markdown reports, JavaScript return objects, backup files, changelog entries, and activation commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Activation can persist memory rules through the local pgmemory Docker/Postgres setup; security evidence says the confirmation safeguard currently auto-approves.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
