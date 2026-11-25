## Description:

Automates Android app releases to Google Play through Easy WebBridge and an already logged-in browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect Android projects, prepare and upload app releases, complete Google Play listings and policy forms, submit changes for review, and check publication status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the release suspicious because its documented installer may download and run an unpinned package; part of the analysis is incomplete.

Mitigation: Review the installer and script, use a specifically reviewed version, and install without access to sensitive credentials or signed-in browser sessions.

Risk: The skill can upload app materials and submit release changes through a signed-in Google Play Console browser.

Mitigation: Confirm the target app, package, release scope, and intended end state before submission, then verify the status shown in Play Console.

## Reference(s):

- [Easy WebBridge runtime repository](https://github.com/xxjrq/easy-webbridge)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files, Configuration instructions]

**Output Format:** [Markdown with shell commands and release status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AAB build or upload results, store listing updates, and Play Console review or publication status.]

## Skill Version(s):

0.2.2 (source: package.json, manifest.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
