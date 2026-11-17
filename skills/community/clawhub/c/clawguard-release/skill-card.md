## Description:

ClawGuard helps agents create and verify local digital asset proof records, certificates, visible watermarks, and file, OS, or network scan reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bhxxkj](https://clawhub.ai/user/bhxxkj)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, digital workers, and developers use this skill to create local proof records for digital assets, generate certificates, verify existing proof IDs, add visible watermarks, and inspect local files or host state for security signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host security scanning and cleanup behavior can inspect or delete local data beyond the proof workflow.

Mitigation: Review commands before use, run the skill in a scoped or disposable workspace, and avoid the clean command unless the working directory is disposable.

Risk: Legal, ISO, malware-safety, and ransomware-integrity claims are not independently reliable based on the security evidence.

Mitigation: Treat proof and certificate outputs as operational records, and verify legal or security assurances through independent review before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bhxxkj/skills/clawguard-release)
- [Publisher Profile](https://clawhub.ai/user/bhxxkj)
- [Release Notes V1.8.0](artifact/RELEASE-NOTES-V1.8.0.md)
- [README](artifact/README.md)
- [Features](artifact/FEATURES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Plain text, Markdown certificates, JSON certificate data, local proof files, and command-oriented responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local proof indexes, certificate folders, exported proof records, and optional visible watermarked images.]

## Skill Version(s):

1.8.0 (source: server release evidence and artifact skill.json; release notes dated 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
