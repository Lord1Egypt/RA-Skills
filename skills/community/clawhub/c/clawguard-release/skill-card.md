## Description: <br>
ClawGuard helps agents create local proof records, certificates, verification reports, security-scan reports, and optional visible image watermarks for digital assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bhxxkj](https://clawhub.ai/user/bhxxkj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and digital-asset creators use this skill to record hashes and timestamps for files, generate proof certificates, verify prior proof IDs, export local records, and run local file, OS, network, or ransomware-oriented checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and record metadata about local files. <br>
Mitigation: Run it only on narrowly scoped folders that do not contain sensitive or unrelated files, and review generated proof records before sharing them. <br>
Risk: The skill may inspect Windows system and network state and may contact public NTP servers. <br>
Mitigation: Use it only in environments where those local inspections and outbound time checks are acceptable. <br>
Risk: Cleanup and restore commands can modify files in the working directory. <br>
Mitigation: Review the selected working directory and keep a separate backup before running cleanup or restore workflows. <br>
Risk: The artifact makes legal, ransomware, and security-scan claims that should not be treated as independently validated. <br>
Mitigation: Use the outputs as operational aids and obtain independent legal or security review before relying on them for enforcement, compliance, or incident response. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bhxxkj/clawguard-release) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bhxxkj) <br>
- [Release notes V1.8.0](artifact/RELEASE-NOTES-V1.8.0.md) <br>
- [Skill manifest](artifact/skill.json) <br>
- [Requirements](artifact/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain-text agent responses, local certificate files, JSON indexes, and scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write proof records, certificate folders, backups, exports, and watermarked image files in local paths selected through the skill workflow.] <br>

## Skill Version(s): <br>
1.8.0 (source: ClawHub release evidence and RELEASE-NOTES-V1.8.0.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
