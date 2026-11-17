## Description:

Review and merge Charon Memory Git proposals as an independent reviewer principal: inspect exact changesets, record digest-bound verdicts, apply protected merges, and verify landed state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mentholmike](https://clawhub.ai/user/mentholmike)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review Charon Memory Git proposals through an independent reviewer principal, apply digest-bound verdicts, merge approved proposals, and verify the accepted memory state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could review or merge a proposal originated by the same principal, weakening reviewer independence.

Mitigation: Install this only for agents using a dedicated review-profile credential, and confirm deployment enforcement rejects self-review and self-approval.

Risk: A stale proposal or changed target state could cause an approval to apply to the wrong memory state.

Mitigation: Inspect exact base and source changeset IDs before verdicts, re-review after proposal or target movement, and verify the landed state after merge.

Risk: Proposal content could contain credentials, private reasoning, or unnecessary personal data.

Mitigation: Request changes instead of approving when sensitive content is present, and avoid copying sensitive proposal content into tickets or chat.

## Reference(s):

- [Charon ClawHub release](https://clawhub.ai/mentholmike/skills/charon)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text]

**Output Format:** [Markdown with inline command and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review verdict guidance and merge verification steps for exact Charon proposal and changeset identifiers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
