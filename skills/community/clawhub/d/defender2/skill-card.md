## Description:

Scans npm packages or projects for JavaScript malware, Windows right-to-left override filename attacks, suspicious private-use characters, Base64-encoded payloads, and known malicious package indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to scan npm packages, project files, and package manifests for suspicious JavaScript patterns, supply-chain indicators, private-use character obfuscation, Base64 payloads, and RLO filename attacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads local source files and may print paths or snippets from suspicious content.

Mitigation: Run it only on directories you intend to inspect and handle scan output as potentially sensitive.

Risk: RLO filename detection relies on installing the external rlo-detect Python package without a pinned version in the skill documentation.

Mitigation: Install rlo-detect only when needed, preferably in an isolated environment after reviewing or pinning the package.

Risk: Heuristic malware indicators can produce false positives or miss new variants.

Mitigation: Treat findings as triage signals and manually review flagged files before removing dependencies or declaring a project clean.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/defender2)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text scanner findings with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scanned file paths and short snippets from suspicious local content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
