## Description: <br>
Helps agents repair merged Android APK installation failures by providing shell-based guidance to update the manifest, keep resources.arsc uncompressed and aligned, re-sign the APK, and verify the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softwareme](https://clawhub.ai/user/softwareme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Android engineers use this skill when a merged universal APK fails to install, especially on Android 11 and later. It guides the agent through manifest repair, native library extraction settings, resources.arsc compression handling, APK alignment, signing, and validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script rewrites and re-signs an APK using hard-coded paths and embedded signing values. <br>
Mitigation: Edit the script before use, set explicit input and output paths, remove hard-coded signing passwords, and use a dedicated non-production test key. <br>
Risk: APK repair steps can alter app packaging, signing identity, or install behavior. <br>
Mitigation: Work on a copy of the APK, verify the final APK, and test on non-production devices before distribution or installation. <br>
Risk: Sideloading a modified APK can expose devices or users to untrusted code. <br>
Mitigation: Use trusted APK sources only and avoid personal or production devices for sideloading tests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/softwareme/fix-universal-apk-installation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires users to customize APK paths, Android SDK build tools paths, keystore paths, and signing values before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
