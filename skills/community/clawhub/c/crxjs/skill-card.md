## Description: <br>
CRXJS helps agents guide Chrome extension development with Vite, including HMR for extension contexts, manifest-driven builds, dynamic content script imports, and type-safe manifests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to scaffold or modify CRXJS-based Chrome extension projects, configure Vite and manifests, troubleshoot HMR issues, and prepare extension builds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad GitHub CLI authority that is not central to CRXJS development guidance. <br>
Mitigation: Allow GitHub CLI use only for tasks that explicitly require it, and review proposed repository or issue operations before execution. <br>
Risk: Generated npm project files or dependency changes can alter build behavior and supply-chain exposure. <br>
Mitigation: Review scaffolded files, package scripts, and dependency changes before running or publishing the extension. <br>
Risk: Copied Chrome extension permissions and URL match patterns may be broader than needed. <br>
Mitigation: Narrow permissions and match patterns to the minimum required before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/crxjs) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>
- [Project homepage](https://github.com/samber/cc-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose npm, git, and GitHub CLI commands for supervised execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
