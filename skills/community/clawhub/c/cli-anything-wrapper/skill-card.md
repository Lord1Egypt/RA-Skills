## Description: <br>
Wraps CLI-Anything so OpenClaw can invoke CLI functions for supported local applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntaffffff](https://clawhub.ai/user/ntaffffff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to list supported CLI-Anything application harnesses and invoke local tools such as GIMP, Blender, LibreOffice, OBS, ComfyUI, Ollama, and Zotero from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper can execute local CLI-Anything harnesses for many desktop and AI tools, which may modify files or application state. <br>
Mitigation: Use dry-run mode first, require explicit approval for state-changing actions, and restrict use to applications and harnesses the operator has reviewed. <br>
Risk: The install path can clone and run setup steps from a third-party GitHub repository without a pinned revision. <br>
Mitigation: Review and pin the CLI-Anything repository before installation, or install it manually from an approved source. <br>


## Reference(s): <br>
- [CLI-Anything Wrapper Usage Guide](references/USAGE.md) <br>
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything) <br>
- [ClawHub release page](https://clawhub.ai/ntaffffff/cli-anything-wrapper) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text status output, optional JSON app listings, and local command execution results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run installed local software through CLI-Anything; dry-run mode can show intended commands without executing them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
