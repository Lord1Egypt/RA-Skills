## Description:

Expert Insist is a prompt-engineering skill that prompts an agent to form an independent view, challenge its assumptions, and re-derive advice after user corrections instead of simply agreeing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn-zhou-chn](https://clawhub.ai/user/shawn-zhou-chn)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can apply this skill when an agent is asked for recommendations, tradeoff analysis, strategy, planning, evaluation, or revised advice after a correction. It is intended to make advice more explicit about conclusions, reasoning, assumptions, and disagreements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation may make answers more opinionated and self-challenging on many recommendation or planning questions.

Mitigation: Use narrower trigger wording, disable the skill for neutral-answer contexts, or ask the agent for a concise factual response when opinionated analysis is not wanted.

Risk: The skill encourages firm advice, which can still be wrong when user-provided assumptions or facts are incomplete.

Mitigation: Require the agent to state key assumptions, ask clarifying questions when facts are unclear, and preserve competing conclusions when the validation rounds do not converge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn-zhou-chn/skills/expert-insist)
- [Publisher profile](https://clawhub.ai/user/shawn-zhou-chn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language advice with conclusions, reasoning, assumptions, challenges, and optional clarifying questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only skill; no code execution, persistent service, credentials, or external dependencies are requested by the artifact.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
