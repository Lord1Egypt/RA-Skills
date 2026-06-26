## Description: <br>
Ledger-informed persona lifecycle management that replaces low-performing personas with successor personas derived from mistake patterns in board decision history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill in long-running consensus systems to replace degraded evaluator personas and preserve auditable governance quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies the configured consensus persona state. <br>
Mitigation: Run it only against the intended consensus state path and review generated persona_set and persona_respawn artifacts after use. <br>
Risk: Successor personas are shaped by ledger and decision inputs. <br>
Mitigation: Keep ledger inputs trusted and inspect the derived learning summary before relying on the updated persona set. <br>
Risk: Dependency drift can change runtime behavior. <br>
Mitigation: Use lockfile-based or pinned dependency installs for reproducible deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-persona-respawn) <br>
- [consensus-guard-core package](https://www.npmjs.com/package/consensus-guard-core) <br>
- [consensus-guard-core repository](https://github.com/kaicianflone/consensus-guard-core) <br>
- [consensus-tools repository](https://github.com/kaicianflone/consensus-tools) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Configuration] <br>
**Output Format:** [JSON artifacts and command-line status JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persona_respawn and persona_set artifacts under the configured consensus state path.] <br>

## Skill Version(s): <br>
1.1.13 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
