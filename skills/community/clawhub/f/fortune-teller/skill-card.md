## Description:

Fortune Teller provides entertainment-focused fortune-telling guidance, including tarot, I Ching, daily fortune, compatibility, numerology, and palmistry topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for entertainment-oriented fortune-telling prompts and command guidance. Review before use if sensitive personal data could be entered into its commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled utility may keep user-supplied text and command history in plaintext under the configured fortune-teller data directory.

Mitigation: Avoid entering sensitive personal data into add, search, or run commands, and review the configured FORTUNE_TELLER_DIR before use.

Risk: Security evidence marks the release suspicious because the entertainment skill bundles a mismatched local utility.

Mitigation: Review the scripts and expected commands before installing or enabling the skill in a production agent environment.

Risk: Some command availability and output language may be inconsistent with the public fortune-telling summary.

Mitigation: Run the help command and test required commands before depending on the skill in a workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/skills/fortune-teller)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command output with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required; output may include Chinese-language fortune-telling text.]

## Skill Version(s):

2.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
