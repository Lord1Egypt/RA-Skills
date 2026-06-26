## Description: <br>
Fast indexed local file and path search on Windows using voidtools Everything for file lookup, path lookup, recent-file discovery, match counts, and other indexed search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamQ96](https://clawhub.ai/user/williamQ96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill on Windows to search local files through the Everything index instead of slower recursive filesystem scans. It is suited for scoped file lookup, path lookup, recent-file discovery, match counts, and advanced es.exe queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can install tooling, start Everything, install shims, and make persistent user PATH changes. <br>
Mitigation: Decide before first use whether setup actions are acceptable; avoid --install-shim when a persistent PATH shim is not desired. <br>
Risk: Broad searches can enumerate local indexed file names and paths. <br>
Mitigation: Prefer scoped searches with --path and avoid raw or --allow-empty unless broad enumeration is intended. <br>
Risk: Results depend on the Windows Everything index and may miss files that are not indexed. <br>
Mitigation: Use recursive filesystem scans when index coverage is unsuitable or non-indexed files are required. <br>


## Reference(s): <br>
- [Everything CLI PowerShell wrapper](references/everything-cli.ps1.txt) <br>
- [ClawHub skill page](https://clawhub.ai/williamQ96/everything-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [JSON search results with command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and recent commands return query metadata, scope, sorting, path, count, offset, limit, and result entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
