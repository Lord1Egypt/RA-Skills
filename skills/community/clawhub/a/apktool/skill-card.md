## Description: <br>
A command-line assistant skill for reverse engineering Android APK files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect, decode, rebuild, troubleshoot, and document Android APK packages with Apktool, Java, and optional JADX support. Use should be limited to APKs the user owns or is authorized to assess. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APK reverse engineering, rebuilding, signing, and integrity-check workflows can be misused on software the user is not authorized to assess. <br>
Mitigation: Use the skill only on APKs the user owns or has explicit permission to analyze, and respect copyright, licensing, and software-protection rules. <br>
Risk: Manual installation examples download releases and change privileged system paths. <br>
Mitigation: Prefer trusted package managers such as apt or Homebrew; when manual installation is needed, review each sudo or PATH-changing command and verify downloaded releases where possible. <br>


## Reference(s): <br>
- [Apktool homepage](https://apktool.org) <br>
- [Apktool documentation](https://apktool.org/docs) <br>
- [Apktool GitHub repository](https://github.com/iBotPeaches/Apktool) <br>
- [Apktool install guide](references/install.md) <br>
- [Apktool usage guide](references/usage.md) <br>
- [Apktool troubleshooting guide](references/troubleshooting.md) <br>
- [JADX release used by manual install metadata](https://github.com/skylot/jadx/releases/download/v1.5.0/jadx-1.5.0.zip) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and command explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include APK analysis, rebuild, signing, installation, and troubleshooting steps for authorized APK workflows.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
