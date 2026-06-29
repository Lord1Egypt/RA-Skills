## Description: <br>
Intelligent disk space analysis and cleanup tool with safety grading, duplicate detection, and Chinese app cache recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and power users use this skill to inspect disk usage, identify duplicate files and caches, and generate safety-graded cleanup recommendations before taking action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup guidance can lead to destructive file operations if applied to the wrong scope. <br>
Mitigation: Review dry-run counts, confirm the target paths, and approve destructive steps only after the scope and rollback plan are clear. <br>
Risk: Disk cleanup can remove files that are still needed by users or applications. <br>
Mitigation: Use preview mode first, prefer trash-based cleanup, keep protected system paths excluded, and review caution-rated items manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/disk-sweeper) <br>
- [cache-patterns.json](references/cache-patterns.json) <br>
- [file-types.json](references/file-types.json) <br>
- [protected-paths.json](references/protected-paths.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, JSON summaries, cleanup previews, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline filesystem analysis with safety labels and explicit confirmation before destructive cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
