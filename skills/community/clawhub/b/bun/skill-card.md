## Description: <br>
Build with Bun runtime avoiding Node.js compatibility traps, bundler pitfalls, and package manager gotchas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill for Bun runtime, bundler, package-manager, and Node.js migration guidance. It helps identify compatibility traps, choose safer build and install commands, and troubleshoot Bun-specific behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup commands can delete local dependency files or lockfiles if run in the wrong project. <br>
Mitigation: Confirm the working directory and commit or back up important dependency files before copying cleanup commands. <br>
Risk: Regenerated Bun dependencies may differ from npm or yarn resolution. <br>
Mitigation: Run the full test suite and review dependency diffs after `bun install` or lockfile regeneration. <br>


## Reference(s): <br>
- [Bun ClawHub Skill Page](https://clawhub.ai/ivangdavila/bun) <br>
- [Bundler Traps](artifact/bundler.md) <br>
- [Node.js Compatibility Traps](artifact/node-compat.md) <br>
- [Package Manager Traps](artifact/packages.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Bun install, build, package-management, and cleanup commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
