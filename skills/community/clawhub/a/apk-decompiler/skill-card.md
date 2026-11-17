## Description:

Decompiles Android APKs, analyzes permissions and components, supports Smali and resource editing, and rebuilds or signs APKs for authorized reverse-engineering workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonakic](https://clawhub.ai/user/tonakic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and Android engineers use this skill to inspect APK structure, permissions, resources, Smali code, and rebuild outputs during authorized analysis or modification work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow downloads and runs persistent third-party APK tooling without built-in integrity checks.

Mitigation: Use a sandbox or disposable workspace, pin and verify tool hashes independently, and keep TOOLS_DIR under explicit user control.

Risk: APK reverse engineering and modification can create legal or policy exposure when used on apps the user is not authorized to inspect or change.

Mitigation: Process only APKs the user is authorized to analyze or modify, and keep authorization and testing boundaries clear before rebuilding or sharing outputs.

Risk: The signing workflow can report signing completion even when signing returns a warning or failure.

Mitigation: Independently verify rebuilt APK signatures before installing, testing, distributing, or relying on the generated APK.

## Reference(s):

- [AndroidManifest.xml modification guide](references/android-manifest.md)
- [Smali syntax quick reference](references/smali-syntax.md)
- [baksmali 2.5.2 download](https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.5.2.jar)
- [smali 2.5.2 download](https://bitbucket.org/JesusFreke/smali/downloads/smali-2.5.2.jar)
- [apktool 2.10.0 download](https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.10.0.jar)
- [dex2jar 2.4 download](https://github.com/pxb1988/dex2jar/releases/download/v2.4/dex-tools-v2.4.zip)
- [uber-apk-signer 1.3.0 download](https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with command examples, file-path references, and generated APK analysis or rebuild artifacts when commands are executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce decompiled APK directories, Smali files, decoded resources, extracted APK contents, JAR files, and rebuilt or signed APK files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
