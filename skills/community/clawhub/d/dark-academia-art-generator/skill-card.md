## Description:

Generates moody dark academia images like candlelit libraries, vintage portraits, classical statues, and autumn campus scenes using Neta AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate dark academia themed image concepts and receive a direct generated image URL from a text prompt. It supports moodboards, journal covers, study playlist art, social posts, and related scholarly or gothic visual assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Neta API token is passed on the command line, where it may be exposed through shell history, logs, or process inspection on shared systems.

Mitigation: Use a short-lived or revocable token, avoid shared execution environments, and rotate the token after use if exposure is possible.

Risk: The documented install command is unpinned, so a later package version could be installed without review.

Mitigation: Install from a trusted or pinned release path and review the resolved files before running the skill.

Risk: Prompts, reference IDs, and the token are sent to the external Neta image service.

Mitigation: Avoid sensitive prompt content or private reference identifiers unless the external service terms and data handling are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/dark-academia-art-generator)
- [Neta AI token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference image arguments affect generation.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
