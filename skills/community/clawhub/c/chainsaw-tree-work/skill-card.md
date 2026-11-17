## Description:

Safe chainsaw operation and basic tree felling techniques for felling trees, cutting firewood, clearing storm damage, buying a first chainsaw, and learning safety practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to screen whether chainsaw and tree work is appropriate for DIY work, confirm required protective equipment, and provide safety-focused guidance for felling, limbing, bucking, storm cleanup, and chainsaw selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill asks for filesystem access it does not need.

Mitigation: Remove the filesystem permission before release, or install only where unnecessary local file access is denied or tightly sandboxed.

Risk: The security evidence says the install command uses an unpinned npx installer.

Mitigation: Use a pinned or otherwise verified install command before deployment.

Risk: The skill provides guidance for physically hazardous chainsaw and tree work.

Mitigation: Keep the skill's PPE confirmation, professional-job screening, local-regulation reminders, and refusal behavior for unsafe cutting requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/chainsaw-tree-work)
- [OSHA chainsaw safety standards](https://www.osha.gov/chain-saws)
- [USDA Forest Service](https://www.fs.usda.gov/)
- [Stihl safety guidelines](https://www.stihlusa.com/safety/)
- [Game of Logging](https://www.gameoflogging.com/)
- [Tree Care Industry Association](https://www.tcia.org/)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown safety guidance with structured checklists and YAML state/triggers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes screening steps, PPE confirmation rules, local-regulation reminders, and refusal guidance for unsafe cutting requests.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
