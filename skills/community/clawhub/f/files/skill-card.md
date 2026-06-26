## Description: <br>
Safely organize, deduplicate, and analyze files with intelligent bulk operations and full undo support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users who need to reorganize local file collections use this skill to plan and execute scoped file organization, duplicate detection, cleanup analysis, and batch rename or move operations with previews, trash handling, and undo records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad or mistaken file operations could move, rename, or trash files the user did not intend to change. <br>
Mitigation: Use clearly scoped directories, review previews and manifests before confirming bulk changes, and rely on native trash plus undo records for recoverability. <br>
Risk: Undo records and duplicate-detection caches may store sensitive file paths, names, or checksums. <br>
Mitigation: Clear local undo and hash-cache data when those details are sensitive, and avoid scanning folders that do not need to be reorganized. <br>
Risk: Symlinks or unsafe paths can redirect operations outside the expected working area. <br>
Mitigation: Canonicalize paths, skip symlinks during traversal, block protected system paths, and require explicit confirmation before following external targets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/files) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file operation plans, previews, confirmations, progress summaries, and manifest expectations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include undo-record requirements, trash-handling guidance, scoped path checks, and safety warnings for bulk file operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
