## Description:

Audience Of One helps agents diagnose and rewrite Chinese AI-like writing by restoring three concrete coordinates: speaker, audience, and purpose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[damomhd](https://clawhub.ai/user/damomhd)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and agents use this skill to diagnose and revise Chinese drafts for public posts, scripts, reports, PRDs, technical documentation, and email. It is intended for style and audience-fit work while preserving facts and asking for missing source material when the draft does not support a concrete rewrite.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad writing triggers can overlap with other writing or editing skills.

Mitigation: Review activation phrases when installing alongside similar writing skills and route fact-checking, translation, or code/log work to more appropriate tools.

Risk: A rewrite can introduce unsupported speaker, audience, or purpose details if the original text lacks evidence.

Mitigation: Use placeholders or ask the author for missing facts instead of inventing details; preserve names, dates, numbers, terms, commands, and responsibility assignments.

Risk: Readers could mistake style rewriting for factual validation.

Mitigation: Treat outputs as writing guidance or revised prose only, and verify factual claims against source material before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/damomhd/skills/audience-of-one)
- [Server-resolved GitHub provenance](https://github.com/DamomHd/audience-of-one)
- [Coordinate diagnostic table](references/coordinates-diagnostic.md)
- [Scenario coordinate guide](references/scenarios.md)
- [Rewrite examples](references/examples.md)
- [Evaluation samples](references/evals.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text rewrite and diagnostic feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a rewritten draft, coordinate diagnosis, placeholder-shaped rewrite guidance, suggested deletion list for long drafts, and brief preservation notes for high-risk factual or technical text.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
