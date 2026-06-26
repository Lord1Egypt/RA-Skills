## Description: <br>
Build Electron desktop apps with secure architecture and common pitfall avoidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill for practical Electron application guidance, especially secure renderer architecture, preload APIs, IPC validation, packaging, platform differences, and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Electron code could weaken application security if it enables renderer Node.js access, disables context isolation, or exposes broad IPC channels. <br>
Mitigation: Review generated code so nodeIntegration remains false, contextIsolation remains true, preload APIs are narrow, and all IPC channels and payloads are explicitly validated. <br>
Risk: Packaging and update guidance can affect runtime reliability and release trust if dependencies, native modules, logging, updates, or signing choices are applied incorrectly. <br>
Mitigation: Review package dependencies, rebuild native modules for the Electron version in use, avoid storing secrets in ASAR packages, and verify update and code-signing behavior for each target platform. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/electron) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no hidden execution, data access, or persistence is indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
