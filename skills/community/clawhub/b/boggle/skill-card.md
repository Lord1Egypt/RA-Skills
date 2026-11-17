## Description:

Solve Boggle boards by finding valid German and English words on a 4x4 letter grid using dictionary-backed search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianhaberl](https://clawhub.ai/user/christianhaberl)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to solve Boggle boards from typed grids or confirmed photo-derived grids, with English and German results presented separately. It is intended for word-game assistance where dictionary-only matching and standard Boggle scoring are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads missing dictionary files from GitHub on first use.

Mitigation: Pre-download or vendor the dictionaries from a trusted source, add checksum verification where practical, and block network access after setup in stricter environments.

## Reference(s):

- [Boggle Solver Skill Page](https://clawhub.ai/christianhaberl/skills/boggle)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Dictionary Data Source](https://github.com/christianhaberl/boggle-openclaw-skill/tree/main/data)
- [Raw Dictionary Download Base](https://raw.githubusercontent.com/christianhaberl/boggle-openclaw-skill/main/data)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown word lists or JSON solver output with Boggle scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [English and German dictionaries are run separately; results are dictionary-only and scored with standard Boggle scoring.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
