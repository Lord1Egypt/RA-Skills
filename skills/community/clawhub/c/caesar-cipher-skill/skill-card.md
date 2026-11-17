## Description:

Provides Caesar cipher encryption, decryption, and brute-force shift exploration for English letters while preserving non-letter characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent for Caesar cipher encryption, decryption, or brute-force checks across all 25 shifts on English-letter text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced scripts/caesar.py implementation is not included in the artifact, so runtime behavior depends on the local script an agent executes.

Mitigation: Confirm the intended caesar.py file is present and trusted before installing or running the skill.

## Reference(s):

- [Source repository](https://github.com/Moxin1044/caesar-cipher-skill)
- [ClawHub skill page](https://clawhub.ai/moxin1044/skills/caesar-cipher-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, and text results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves non-letter characters; supports shifts 1-25 and brute-force listings.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
