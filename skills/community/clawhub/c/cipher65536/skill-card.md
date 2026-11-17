## Description:

cipher65536 encodes and decodes arbitrary files as Base65536 Unicode text with gzip compression, filename preservation, and optional XOR-based scramble mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turinfohlen](https://clawhub.ai/user/turinfohlen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert binary files into Unicode text for text-only transfer paths and to decode those files back into their original file form. Scramble mode should be reviewed before use and should not be treated as sensitive-data encryption without independent approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scramble mode is presented as encryption, but the security evidence warns not to rely on it for sensitive encryption.

Mitigation: Use independently reviewed encryption for sensitive data and treat scramble mode only as an obfuscation or transport feature unless it is separately approved.

Risk: The skill can be used to bypass upload restrictions or platform policies.

Mitigation: Use it only where text-based file transfer is allowed by the destination platform and organizational policy.

Risk: Decoding untrusted inputs or omitting a safe output path can write files using metadata-controlled names.

Mitigation: Decode only trusted files or always pass an explicit safe --output path in a controlled directory.

Risk: Generated .key files control access to scrambled content and data may be unrecoverable if a key is lost.

Mitigation: Protect .key files as secrets, transfer keys separately from encoded content, and use approved backup or key custody practices.

Risk: The artifact's usage examples include an unpinned pip install command.

Mitigation: Prefer installing dependencies from the pinned artifact/requirements.txt file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turinfohlen/skills/cipher65536)
- [encoding-details.md](artifact/references/encoding-details.md)
- [scrambleing-details.md](artifact/references/scrambleing-details.md)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with command examples and file outputs from the included Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script may write encoded text files, decoded binary files, and .key files when executed.]

## Skill Version(s):

1.0.4 (source: server release metadata and artifact/_meta.json; SKILL.md frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
