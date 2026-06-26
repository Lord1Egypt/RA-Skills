## Description: <br>
Manage Homebrew end-to-end on macOS, including detecting whether Homebrew is installed, understanding formula vs cask, updating metadata and packages, installing/uninstalling software, searching/listing package state, cleanup/autoremove, diagnostics, and Brewfile workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weichengwu](https://clawhub.ai/user/weichengwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical users, and support agents use this skill to manage Homebrew on macOS: checking installation health, updating metadata and packages, installing or removing formulae and casks, cleaning dependencies, troubleshooting brew errors, and exporting or applying Brewfile state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Homebrew operations can install, uninstall, upgrade, clean up, or otherwise change software on a Mac. <br>
Mitigation: Review and approve package installs, uninstalls, upgrades, cleanup, autoremove, Brewfile sync, and installer steps only when the expected changes are understood. <br>
Risk: Running the Homebrew installer executes a remote shell script when Homebrew is missing. <br>
Mitigation: Detect whether Homebrew is already installed first, clearly report when it is missing, and proceed with the installer only after the user confirms. <br>
Risk: Cleanup, autoremove, uninstall, or Brewfile sync commands can remove packages or alter the local development environment. <br>
Mitigation: Use dry-run or check commands where available, confirm exact targets before destructive changes, and verify results after execution. <br>


## Reference(s): <br>
- [Homebrew official installer script](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes concise command reports, verification steps, and troubleshooting guidance for Homebrew package and Brewfile workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
