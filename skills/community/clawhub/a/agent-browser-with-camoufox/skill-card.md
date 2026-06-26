## Description: <br>
Installs Camoufox and patches agent-browser so browser automation can run through a Firefox or Camoufox executable path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdAstraAbyssoque](https://clawhub.ai/user/AdAstraAbyssoque) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install Camoufox, install or locate agent-browser, patch browser-type detection, rebuild the package, and run browser automation with a Camoufox executable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer makes broad persistent changes to global browser automation tooling, including replacing or patching agent-browser files. <br>
Mitigation: Run it only in an isolated or disposable environment, review the script first, and keep backups of the existing global agent-browser installation. <br>
Risk: The installer uses unverified remote installers and downloads for tooling such as uv, Rust, npm packages, and Camoufox. <br>
Mitigation: Prefer pinned and verified downloads where possible, inspect remote install scripts before execution, and avoid running the installer with elevated privileges. <br>
Risk: Camoufox browser automation can be used in ways that bypass service protections or terms. <br>
Mitigation: Use the skill only for automation you are authorized to run and do not use it to bypass protections on services where you do not have permission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AdAstraAbyssoque/agent-browser-with-camoufox) <br>
- [Publisher profile](https://clawhub.ai/user/AdAstraAbyssoque) <br>
- [Camoufox GitHub](https://github.com/daijro/camoufox) <br>
- [agent-browser GitHub](https://github.com/browser-use/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installer modifies global agent-browser files and may download external tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
