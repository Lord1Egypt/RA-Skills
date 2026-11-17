## Description:

A-share short-term trading decision skill for 1-5 day market sentiment, sector rotation, stock screening, capital-flow confirmation, signal scoring, prediction logging, and next-day comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenera](https://clawhub.ai/user/kenera)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to generate short-term CN A-share research signals, daily recommendation artifacts, risk controls, and comparison reports for a 1-5 day trading horizon. Outputs should be treated as research signals and decision support, not instructions to trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An optional optimization command can overwrite a caller-selected JSON configuration file.

Mitigation: Back up the target configuration and use `--apply-to-config` only when the overwrite is intentional.

Risk: Caller-provided config paths can point outside the skill directory.

Mitigation: Avoid absolute paths and `..` segments for configuration options; review resolved paths before running optimization.

Risk: Generated stock recommendations can be mistaken for trading instructions.

Mitigation: Treat outputs as research signals and decision support, and apply independent review before any trading decision.

Risk: Unpinned dependencies can change runtime behavior.

Mitigation: Run the skill in a virtual environment and pin dependencies where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kenera/skills/a-share-short-decision)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [requirements.md](artifact/requirements.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON artifacts, and CLI command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write prediction logs, daily recommendation JSON, optimization JSON, and Markdown summaries under data/.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
