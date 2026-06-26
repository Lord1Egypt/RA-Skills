## Description: <br>
Do App Store Optimization (ASO) with the ASO Suite CLI across iPhone, iPad, Mac, Apple TV, Apple Watch, and VisionOS by finding keywords with popularity/difficulty data, tracking keyword position over time, annotating tracked keywords with notes and global color-coded tags, and monitoring ratings, editorial features, and chart appearances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hesselbom](https://clawhub.ai/user/hesselbom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ASO practitioners, app developers, and marketing teams use this skill to operate the ASO Suite CLI for app discovery, keyword research, keyword tracking, notes and tags, competitor relationships, charts, features, ratings, and ASO event records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires logging into a third-party ASO Suite account and can use long-lived CLI access credentials. <br>
Mitigation: Install only when the ASO Suite publisher is trusted, authenticate through the documented login flow, and keep the stored CLI token protected. <br>
Risk: Some commands can create, edit, delete, track, untrack, plan, or unplan persistent ASO account data. <br>
Mitigation: Prefer read-only commands first and require explicit approval before running commands that modify tracked apps, planned apps, keywords, tags, notes, relationships, or events. <br>
Risk: Keyword notes and events may contain sensitive internal ASO strategy. <br>
Mitigation: Avoid putting confidential strategy or sensitive business data into ASO Suite notes or event records unless the account's handling of that data is approved. <br>


## Reference(s): <br>
- [ASO Suite](https://www.asosuite.com/) <br>
- [ClawHub ASO Suite release](https://clawhub.ai/hesselbom/asosuite) <br>
- [Publisher profile](https://clawhub.ai/user/hesselbom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of the `asosuite` CLI and recommends `--json` for commands that support machine-readable output.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
