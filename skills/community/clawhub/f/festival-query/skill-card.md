## Description:

Festival query tool for Chinese lunar dates, traditional Chinese festivals, the 24 solar terms, and major Western or international holidays, with date, year, month, and solar-term query modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhou-xiaobo](https://clawhub.ai/user/zhou-xiaobo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer festival, lunar calendar, solar-term, and holiday-date questions for a specific date, month, or year.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup command installs unpinned Python packages into the host environment and uses `--break-system-packages`.

Mitigation: Install only the needed dependencies in an isolated virtual environment with pinned versions, and avoid `--break-system-packages` on shared or system Python installations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhou-xiaobo/skills/festival-query)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text festival and calendar lookup results from command-line queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-date, year, month, and 2020-2030 solar-term table queries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
