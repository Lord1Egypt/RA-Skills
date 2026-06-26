## Description: <br>
Review Flutter Android APK/AAB release artifacts for manifest, permission, cleartext traffic, exported component, embedded secret, signing, size, WebView, deep link, and third-party service risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anasfik](https://clawhub.ai/user/anasfik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this agent skill to inspect Flutter Android APK/AAB release artifacts before shipping. It guides evidence collection for Android manifest, signing, embedded-secret, WebView, network, deep-link, and third-party service risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APK/AAB inspection can expose private artifacts, production secrets, signing details, or customer data. <br>
Mitigation: Inspect only artifacts the user is authorized to review, keep reports evidence-focused, and redact secret values before sharing. <br>
Risk: Fetching published APKs with apkeep may require Google Play access tokens or may conflict with app-store expectations if used broadly. <br>
Mitigation: Use apkeep only for authorized or appropriate public app review, do not store Google account credentials, and avoid bulk or high-parallel downloads. <br>
Risk: Recommended fixes may affect sensitive production behavior such as authentication, payments, permissions, signing, publishing, privacy, or API key migration. <br>
Mitigation: Require explicit human approval before changing sensitive app behavior; generate reports, checklists, and recommendations without silently modifying the app. <br>
Risk: Reverse-engineering tools and string extraction can produce incomplete or misleading conclusions if their output is treated as source code. <br>
Mitigation: Treat decompiled code and extracted strings as artifact evidence only, cite exact paths or command outputs, and avoid claiming full Dart source recovery from Flutter binaries. <br>


## Reference(s): <br>
- [Flutterguard Cli on ClawHub](https://clawhub.ai/anasfik/flutterguard-cli) <br>
- [EFF apkeep](https://github.com/EFForg/apkeep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security review report with findings, evidence, status, score, recommended actions, and human-approval notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should cite observable artifact evidence and redact secrets.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
