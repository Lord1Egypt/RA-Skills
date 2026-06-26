## Description: <br>
A simple, fast and user-friendly alternative to 'find' based on sharkdp/fd for local file search and filesystem analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find files by name or extension, identify large, recent, empty, or duplicate files, and summarize local directory contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan broad local filesystem paths supplied by the caller. <br>
Mitigation: Run it only against intended project directories and avoid sensitive home, credential, or system locations. <br>
Risk: Path and argument handling is unsafe enough to warrant review before installation, especially if arguments come from untrusted text. <br>
Mitigation: Do not pass untrusted paths or arguments; review commands before execution. <br>
Risk: Duplicate-file results may be false positives because matching-size files are compared using only the first 64KB. <br>
Mitigation: Treat duplicate output as candidate matches and verify full file contents before deleting or modifying files. <br>


## Reference(s): <br>
- [File Finder ClawHub listing](https://clawhub.ai/ckchzh/file-finder) <br>
- [sharkdp/fd reference project](https://github.com/sharkdp/fd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text command output and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filesystem scan results are command-limited; duplicate results are candidate matches because matching-size files are hashed only on their first 64KB.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
