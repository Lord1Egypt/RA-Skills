## Description: <br>
Build with Deno runtime avoiding permission gotchas, URL import traps, and Node.js migration pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when building, configuring, or migrating Deno projects that need safe runtime permissions, reliable dependency imports, and Node.js compatibility guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Deno commands may request overly broad runtime permissions such as full filesystem, network, environment, subprocess, FFI, or all-access permissions. <br>
Mitigation: Review permission flags before execution and scope them to the exact paths, hosts, environment variables, commands, or interfaces required by the project. <br>
Risk: Remote imports or unpinned dependencies can make Deno projects fail at startup or change behavior between runs. <br>
Mitigation: Use explicit versions, maintain a deno.lock file, and vendor or cache dependencies for production and CI workflows. <br>
Risk: Node.js migration guidance can be incomplete for packages that rely on native addons or unsupported Node APIs. <br>
Mitigation: Test every migrated dependency and runtime path under the same Deno version and permissions intended for deployment. <br>


## Reference(s): <br>
- [Deno Skill on ClawHub](https://clawhub.ai/ivangdavila/deno) <br>
- [Permission System Traps](artifact/permissions.md) <br>
- [Import and Dependency Traps](artifact/imports.md) <br>
- [Node.js Migration Traps](artifact/node-compat.md) <br>
- [Deno Standard Library Example](https://deno.land/std@0.210.0/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline TypeScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the deno binary for commands that the agent recommends or helps users run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
