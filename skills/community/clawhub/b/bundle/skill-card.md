## Description:

Package directories into distributable bundles with manifests for release packaging, content verification, and checksum generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to create, inspect, verify, size, and extract directory bundles with manifests and checksums.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe argument handling can cause unintended file operations, including destructive behavior.

Mitigation: Review generated commands before execution and avoid using the skill on important directories until argument handling is fixed.

Risk: Archive extraction may be unsafe for untrusted bundles until extraction validates archive paths.

Mitigation: Extract only trusted bundles, prefer empty temporary directories, and inspect archive contents before extraction.

## Reference(s):

- [Bundle ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/bundle)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash command examples; script commands produce tar archives, checksum files, manifests, listings, and status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on local paths and may read or write bundle archives, checksum files, extracted files, and ~/.local/share/bundle.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
