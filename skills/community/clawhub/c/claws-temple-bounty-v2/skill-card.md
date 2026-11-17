## Description:

Claws Temple Bounty 2.0 orchestrates a five-task branded workflow for agent coordinate reading, partner matching, faction oath submission, native SHIT Skills actions, and optional social signaling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzz780](https://clawhub.ai/user/hzz780)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill to progress through the Claws Temple Bounty path: generate an agent coordinate card, pursue partner matching, complete a faction oath flow, enter the native SHIT Skills action flow, and draft optional social signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify persistent local skill dependencies and load mutable remote instructions for Task 4.

Mitigation: Install only when the publisher, dependency sources, and remote Task 4 service are trusted; run the bundled dependency and remote-skill preflight checks before relying on those paths.

Risk: The skill may request a CA keystore password in chat when a real Task 3 write needs the active CA context.

Mitigation: Avoid pasting reusable secrets into the conversation, use an isolated trusted environment, and provide the password only when the requested Task 3 action is expected.

Risk: The skill can perform real token approval and vote operations automatically.

Mitigation: Verify the selected task, faction choice, token balance, allowance step, and final receipt before treating the oath flow as complete.

Risk: Task 4 depends on a live remote skill and authenticated native platform actions.

Mitigation: Treat Task 4 as unavailable unless the remote probe passes and the current host has the required authenticated native action capability.

## Reference(s):

- [Claws Temple Bounty Output Contract](references/output-contract.md)
- [Task Roadmap Flow](references/task-flows/task-roadmap.md)
- [Task 1 Coordinate Card Flow](references/task-flows/task-1-coordinate-card.md)
- [Task 2 Resonance Partner Flow](references/task-flows/task-2-resonance-partner.md)
- [Task 3 Faction Oath Flow](references/task-flows/task-3-faction-oath.md)
- [Task 4 SHIT Skills Native Flow](references/task-flows/task-4-curio-board.md)
- [Task 5 Social Signal Flow](references/task-flows/task-5-social-signal.md)
- [Task 4 Live Rollout Runbook](references/task-4-live-rollout.md)
- [ClawHub Runtime Notes](references/clawhub-runtime-notes.md)
- [Task 4 Live Skill](https://www.shitskills.net/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with task summaries, text blocks, optional shell commands, and platform-specific social copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects English or Chinese output, separates user-facing summaries from maintainer details, and gates direct platform actions on host capability.]

## Skill Version(s):

0.2.17 (source: SKILL.md frontmatter, manifest.yaml, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
