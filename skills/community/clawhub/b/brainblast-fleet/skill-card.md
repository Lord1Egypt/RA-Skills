## Description:

Autonomous, scheduled agent that finds real, proven security footguns in popular SDKs and submits them to the open Brainblast corpus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsb-117](https://clawhub.ai/user/dsb-117)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers and developers use this skill to run scheduled sourcing cycles that discover, prove, and submit public-code security footgun examples to the Brainblast corpus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional cron job can run unattended on a recurring schedule.

Mitigation: Run the fleet manually first in a restricted account or sandbox, inspect cron history, and install the cron job only after the operating schedule is acceptable.

Risk: The workflow downloads and executes the current contents of a remote repository without integrity pinning.

Mitigation: Inspect the remote code before use and pin or otherwise verify the executable revision before enabling persistent operation.

Risk: Optional registry and reprove tokens can increase submission or verification privileges.

Mitigation: Avoid setting optional tokens unless needed, keep them scoped to the registry workflow, and remove them when unattended operation does not require them.

## Reference(s):

- [Brainblast Registry](https://registry.brainblast.tech)
- [Brainblast Fleet on ClawHub](https://clawhub.ai/dsb-117/skills/brainblast-fleet)
- [Publisher Profile](https://clawhub.ai/user/dsb-117)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and script-generated status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports seams swept, candidates proven or drafted, corpus delta, registry rejects, and suggested next seams.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
