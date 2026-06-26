## Description: <br>
Apk Decompiler helps agents guide authorized Android APK reverse-engineering workflows, including decompilation, Smali and resource analysis, editing, rebuilding, and signing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonakic](https://clawhub.ai/user/tonakic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect APK structure, permissions, resources, and Smali code, then rebuild and sign modified APKs when they are authorized to analyze or modify the application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs third-party APK reverse-engineering tools. <br>
Mitigation: Run setup on a trusted network, keep TOOLS_DIR under user control, and verify downloaded tools when possible. <br>
Risk: Unknown APKs can contain untrusted or malicious content. <br>
Mitigation: Analyze APKs in a sandbox, virtual machine, emulator, or disposable device. <br>
Risk: APK analysis or modification may be unauthorized for some applications. <br>
Mitigation: Use the skill only when authorized to inspect or modify the apps involved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tonakic/apk-decompiler) <br>
- [AndroidManifest.xml modification guide](references/android-manifest.md) <br>
- [Smali syntax quick reference](references/smali-syntax.md) <br>
- [baksmali download used by setup script](https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.5.2.jar) <br>
- [smali download used by setup script](https://bitbucket.org/JesusFreke/smali/downloads/smali-2.5.2.jar) <br>
- [apktool download used by setup script](https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.10.0.jar) <br>
- [dex2jar release used by setup script](https://github.com/pxb1988/dex2jar/releases/download/v2.4/dex-tools-v2.4.zip) <br>
- [uber-apk-signer release used by setup script](https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, file paths, and analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that read, decompile, rebuild, or sign APK files and may write decompiled project files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
