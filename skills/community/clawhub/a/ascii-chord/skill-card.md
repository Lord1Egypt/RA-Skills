## Description: <br>
Shows ASCII guitar chord diagrams using the bundled ascii_chord Rust CLI for single chords, chord progressions, and supported chord listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzhong52](https://clawhub.ai/user/yzhong52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, musicians, and music-learning agents use this skill to answer guitar chord questions with terminal-rendered ASCII chord diagrams and supported chord-name lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cargo builds create a persistent target directory and may download normal Rust dependencies. <br>
Mitigation: Run the build from the installed skill directory, review Cargo.toml before first use, and expect local Rust build artifacts. <br>
Risk: Systems without Rust installed may need rustup, which can create home-directory toolchain folders and update PATH. <br>
Mitigation: Install Rust only through an approved toolchain process and confirm shell profile changes before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yzhong52/ascii-chord) <br>
- [Publisher profile](https://clawhub.ai/user/yzhong52) <br>
- [ascii_chord project link from skill documentation](https://github.com/ascii-music/ascii_chord) <br>
- [Rust toolchain installer](https://rustup.rs) <br>
- [aschord package](https://crates.io/crates/aschord) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text chord diagrams with optional Markdown code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chord names are case-sensitive; unsupported chord names require listing supported chords or choosing a close match.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
