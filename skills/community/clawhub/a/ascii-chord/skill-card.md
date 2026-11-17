## Description:

Show ASCII guitar chord diagrams using the ascii_chord CLI tool for requested guitar chord names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzhong52](https://clawhub.ai/user/yzhong52)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to answer guitar chord questions by generating readable ASCII chord diagrams or supported-chord listings with a bundled Rust CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Rust CLI builds locally and Cargo creates persistent target/ build artifacts in the skill directory.

Mitigation: Run the post-install initialization only in the installed skill directory and review the bundled source before use when local executable builds are restricted.

Risk: Installing Rust through rustup can create ~/.cargo and ~/.rustup and may update the user's PATH.

Mitigation: Use an existing trusted Rust toolchain where possible, or install Rust only after accepting those local environment changes.

Risk: The all --save command writes or overwrites all_supported_chords.md in the current working directory.

Mitigation: Use all without --save for read-only output, or run --save only from a directory where regenerating that file is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yzhong52/skills/ascii-chord)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yzhong52)
- [Rust Installer](https://rustup.rs)
- [aschord Crate](https://crates.io/crates/aschord)
- [All Supported Chords](all_supported_chords.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and ASCII chord diagram text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cargo/Rust locally; the optional all --save command writes all_supported_chords.md in the current working directory.]

## Skill Version(s):

2.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
