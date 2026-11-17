## Description:

Turns an article, document, release note, or paper into a short Ofox explainer-video workflow by selecting one concrete idea, drafting spoken words, estimating cost, and producing approved generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and content teams use this skill to turn source writing into a short spoken explainer clip while setting expectations that the clip carries one idea rather than summarizing the whole source. The skill guides idea selection, prompt construction, cost quoting, approval, generation, and post-run checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source text and prompts are sent to Ofox under the user's API key.

Mitigation: Confirm the user is comfortable sharing the source material with Ofox before generation.

Risk: Generated clips are paid outputs and a command flag cannot prove that human approval occurred.

Mitigation: Show the dry-run cost table first, wait for explicit approval, then run the matching command with --approved.

Risk: If ofox-video-core is missing, optional unpinned npx installer commands could modify the user's skill environment.

Mitigation: Prefer a trusted, pinned installer path where available and relay installer commands for the user to run rather than executing them automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/explainer)
- [Release homepage](https://github.com/ofoxai/skills/tree/main/skills/explainer)
- [Ofox API key setup](https://app.ofox.ai)
- [ofox-video-core safety contract](../ofox-video-core/SKILL.md)
- [Prompt structure reference](../ofox-video-core/references/prompt-structure.md)
- [Creative brief reference](../ofox-video-core/references/creative-brief.md)
- [Approval gate reference](../ofox-video-core/references/approval-gate.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Files]

**Output Format:** [Markdown guidance with bash commands, approval recaps, and generated MP4 file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OFOX_API_KEY for paid generation; uses curl and jq through the delegated Ofox video core workflow.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
