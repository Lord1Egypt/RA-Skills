## Description: <br>
Helps migrate Windows developer-tool caches, plugins, and application data directories to a user-selected drive by copying the data, replacing the original directory with an NTFS Junction, and verifying the redirect. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunliangzesmile](https://clawhub.ai/user/sunliangzesmile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Windows power users use this skill to identify large application cache or data directories, move them off the system drive, synchronize related tool configuration, and verify NTFS Junction migration status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move, delete, and permanently redirect local application folders. <br>
Mitigation: Back up important data, close affected applications, confirm exact source and destination paths, and verify the Junction after migration. <br>
Risk: Broad or incorrect source paths could affect more data than intended. <br>
Mitigation: Use exact cache or application data directories only, avoid system-wide or broad profile paths, and prefer a preliminary scan before running migration commands. <br>
Risk: VSCode migration can modify launcher and settings files. <br>
Mitigation: Review those file changes first, keep a copy of the original launcher/settings files, or use skip options when launcher edits are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunliangzesmile/cache-migration) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with PowerShell and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows 10/11 focused; scripts operate on local filesystem paths and NTFS Junctions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
