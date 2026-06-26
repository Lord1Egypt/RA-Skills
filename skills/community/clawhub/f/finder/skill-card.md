## Description: <br>
Find files by name, size, date, and type with deduplication. Use when searching filesystems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Finder to enumerate files under selected local directories by name, size, modification date, type, emptiness, or largest-file order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enumerate filenames and file sizes under directories selected by the user. <br>
Mitigation: Use narrow, intentional paths and avoid running it across sensitive system or private directories unless that enumeration is acceptable. <br>
Risk: The shell script does not robustly validate or quote all user-supplied patterns and paths. <br>
Mitigation: Use trusted inputs, avoid unusual shell metacharacters in patterns or paths, and review or harden quoting and validation before broad deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/finder) <br>
- [Publisher homepage](https://bytesagain.com) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Finder shell script](artifact/scripts/script.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output is limited to the first 20 matches for most searches and to the requested count for largest-file listings.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
