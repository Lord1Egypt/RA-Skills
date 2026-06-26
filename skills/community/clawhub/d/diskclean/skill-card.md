## Description: <br>
AI-assisted disk space scanner and cleaner. Finds reclaimable space (node_modules, build caches, package caches, downloads, Docker, Xcode, logs) and intelligently cleans safe items with strict guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xj7r](https://clawhub.ai/user/0xj7r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power users use this skill to scan local macOS or Linux home directories for reclaimable space and guide reviewed cleanup of caches, build outputs, logs, downloads, Docker data, and other disk usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup actions can permanently delete local cache, build, log, dependency, or download files that the user still needs. <br>
Mitigation: Run a scan and dry run first, review the listed paths and categories, and execute confirmed cleanup only after explicit user approval. <br>
Risk: Suggest-tier items such as Downloads, virtual environments, Docker data, and trash may contain user-managed data. <br>
Mitigation: Treat suggest-tier findings as recommendations and delete only specific approved items or categories under the user's home directory. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and scan-result tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON scan results produced by diskclean.sh.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
