## Description: <br>
Statically analyzes code for feature flag hygiene issues such as stale flags, SDK misuse, safety risks, and architecture problems before production deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use featurelint to scan repositories, staged changes, or individual files for feature flag hygiene issues and produce reports that guide remediation before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can include source snippets from scanned files, which may expose sensitive code or secrets if shared broadly. <br>
Mitigation: Avoid scanning folders that contain secrets when reports may be saved or shared, and review generated reports before distribution. <br>
Risk: Using FEATURELINT_LICENSE_KEY sends the key for validation and caches license state locally. <br>
Mitigation: Treat the license key as a sensitive credential, set it only in trusted environments, and manage any local cache according to the user's credential-handling practices. <br>


## Reference(s): <br>
- [ClawHub featurelint release](https://clawhub.ai/suhteevah/featurelint) <br>
- [FeatureLint homepage](https://featurelint.pages.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON, CSV, or Markdown reports, with shell command and hook configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be printed to stdout or written to a file and can include source context around findings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
