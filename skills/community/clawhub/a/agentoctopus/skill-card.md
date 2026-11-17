## Description:

AgentOctopus routes a natural-language query to the best installed specialized skill, executes the selected skill, and falls back to a direct LLM answer when no skill fits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leiw5173](https://clawhub.ai/user/leiw5173)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use AgentOctopus to route user requests across installed skills, manage skill installation and updates, and configure CLI or gateway access for skill execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install, overwrite, update, evolve, and execute skills from remote sources with limited documented trust controls.

Mitigation: Install only from trusted publishers and reviewed sources; prefer pinned versions and review replacements before using overwrite or update paths.

Risk: Arbitrary cloud sync URLs or forced overwrites can change the local skill set or routing behavior.

Mitigation: Avoid arbitrary cloud URLs, use dry-run or check modes first, and reserve --force for reviewed replacements.

Risk: Opt-in evolution can alter skill descriptions, triggers, or instructions based on usage signals.

Mitigation: Keep evolution disabled unless adaptive behavior is intended, and review proposed risky changes plus rollback history before approval.

Risk: Credentials may be exposed if real API keys are pasted directly into shell commands.

Mitigation: Use the configured secrets file or interactive setup flow, and avoid entering real keys in command lines that may be stored in shell history.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, TypeScript examples, and JSON request or response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include routed skill responses, direct LLM fallback answers, setup guidance, masked configuration summaries, and error guidance.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
