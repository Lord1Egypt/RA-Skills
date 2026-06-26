## Description: <br>
Robust Docker volume migration and backup using per-volume encrypted archives and registry-based transport. Supports dry-runs, container exclusion, and safe restoration without executing untrusted code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to back up Docker volumes into encrypted registry images and restore them on Docker hosts. It is intended for Docker volume migration, disaster recovery, and host-to-host transfer workflows where registry storage is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Docker-level access to local volumes and authority to push or pull registry images. <br>
Mitigation: Run dry-run first, use an explicit private registry target, and install only where Docker-level access to the affected volumes is acceptable. <br>
Risk: Restore operations can overwrite data in same-named destination volumes. <br>
Mitigation: Verify the backup image and destination host before restore, and avoid restoring onto hosts with important same-named volumes unless overwrite is intended. <br>
Risk: The encryption password is supplied as a command-line argument and may be exposed through shell history or local process inspection. <br>
Mitigation: Use a dedicated password, avoid reusing important credentials, control local shell history and host access, and rotate the password if exposure is suspected. <br>
Risk: Encrypted backup data is stored inside registry image layers and remains sensitive even when encrypted. <br>
Mitigation: Push backups only to private registry repositories with appropriate access controls and sufficient storage quota. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ugvfpdcuwfnh/docker-volume-backup-or-restore) <br>
- [Limitations and Tradeoffs](references/limitations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on Docker backup and restore commands, registry image references, encryption passwords, dry-run mode, and container exclusion options.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
