## Description: <br>
Scans npm packages or projects for JavaScript malware, Windows filename right-to-left override tricks, suspicious Unicode PUA characters, Base64-encoded payloads, malicious dependencies, and risky package scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to scan npm projects, package.json files, and package directories for indicators of JavaScript supply-chain malware before running or publishing code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads local files and may print file paths, file names, and decoded snippets in its report. <br>
Mitigation: Run it only on npm projects or package directories you intend to inspect, and avoid scanning paths that contain unrelated sensitive files. <br>
Risk: The optional rlo-detect setup command installs an unpinned dependency. <br>
Mitigation: Verify the dependency before installing it and prefer an isolated environment for setup and scanning. <br>
Risk: Heuristic malware indicators can produce false positives or miss new variants. <br>
Mitigation: Treat findings as triage signals and review flagged files manually before deleting packages or changing dependencies. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/goog/defender2) <br>
- [Publisher profile](https://clawhub.ai/user/goog) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Scanner script](artifact/scripts/pua.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Console text report with scan findings, threat status, and recommended follow-up actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scanner supports path, recursive, and verbose options; it exits with status 1 when suspicious files are found and 0 when no suspicious files are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
