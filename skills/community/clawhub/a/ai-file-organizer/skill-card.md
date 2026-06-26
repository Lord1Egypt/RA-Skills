## Description: <br>
Provides a Python CLI that categorizes and renames local files, copies them into organized folders, finds duplicate files by hash, and exports JSON reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to organize folders, classify files by type or configured rules, copy renamed files into target directories, find duplicate files, and generate machine-readable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a user's file layout, including moving duplicate files. <br>
Mitigation: Review before installing, test only on a disposable folder, and keep backups before using duplicate cleanup. <br>
Risk: Documentation claims safety, dry-run, interactive, cloud, AI, and recovery behavior that the security evidence says the code does not actually provide. <br>
Mitigation: Do not rely on documented dry-run or interactive modes unless they are implemented, and avoid cloud or AI credential configs until the maintainer clearly documents what data is uploaded and when. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON reports] <br>
**Output Format:** [Markdown guidance with command examples; JSON for exported organize and duplicate reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include file counts, category summaries, duplicate counts, errors, target paths, and elapsed time.] <br>

## Skill Version(s): <br>
3.0.0 (source: evidence.release.version, SKILL.md frontmatter, _meta.json, and CHANGELOG.md; artifact changelog date 2026-03-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
