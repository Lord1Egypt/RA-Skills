## Description:

Turns fight concepts and source references into fictional fight story beats, action chains, spatial routes, and action storyboards, and can ingest confirmed reference files into its local reference library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and agents use this skill to turn rough fight ideas into fictional action design, choreography logic, spatial routing, and storyboard tables. They can also use it to classify and ingest user-confirmed reference material into scenes, directing plans, move references, conditional skills, or sample scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags a conflict between the stated no-prompt boundary and prompt-generation templates or detailed combat instructions in the artifact.

Mitigation: Review before installing, keep use limited to fictional choreography and storyboards, and strip or clearly reclassify prompt-generation templates before use.

Risk: Detailed move references could be misread as real-world fighting instruction.

Mitigation: Use the move library only for fictional staging and storyboard continuity, not for training, tactical advice, or real-world harm.

Risk: Confirmed reference ingestion can persist private or sensitive user-provided material into the skill reference library.

Mitigation: Review files before ingestion, require explicit confirmation, and remove confidential or personal material before allowing library updates.

Risk: Reference examples may invite copying protected characters, settings, or distinctive expression.

Mitigation: Reuse only transferable mechanisms such as escalation, spatial phases, reversals, and continuity constraints, and avoid copying proprietary characters or distinctive wording.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangminrui2022/skills/fight-video-create-skill)
- [Workflow and operating constraints](artifact/SKILL.md)
- [English README](artifact/README.en.md)
- [Changelog](artifact/changelog.md)
- [Reference router](artifact/scripts/route_reference.py)
- [Route metadata validator](artifact/scripts/validate_routes.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose, storyboard tables, reference-selection summaries, and occasional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update reference files and routing JSON after a confirmed reference-ingestion workflow.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
