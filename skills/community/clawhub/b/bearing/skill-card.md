## Description: <br>
A command-line skill advertised as a bearing selection and life calculator, while security evidence reports that the artifact behaves as a local entry tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or users can use this skill to add, list, search, remove, configure, and export local text entries. Do not rely on it for bearing calculations without independent review because ClawScan reports a mismatch between the advertised purpose and artifact behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised bearing-calculator purpose does not match the artifact behavior reported by ClawScan. <br>
Mitigation: Review the script behavior before use and treat outputs as local entry-tracker data, not engineering bearing calculations. <br>
Risk: User-provided entries are retained locally under ~/.bearing or a BEARING_DIR override. <br>
Mitigation: Avoid storing sensitive engineering or project data unless local retention is acceptable. <br>
Risk: Remove and export commands can delete entries or duplicate stored data into local files. <br>
Mitigation: Review command arguments before running remove or export and inspect generated files before sharing them. <br>


## Reference(s): <br>
- [Bearing on ClawHub](https://clawhub.ai/ckchzh/bearing) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text CLI output with local JSONL storage and optional JSON or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries under ~/.bearing by default, or under BEARING_DIR when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
