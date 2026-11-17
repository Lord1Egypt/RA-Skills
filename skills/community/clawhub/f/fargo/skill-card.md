## Description:

FargoRate helps agents look up pool player ratings, FargoRate IDs, match odds, race-to recommendations, handicaps, top rankings, and rating changes using the fargo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rgstephens](https://clawhub.ai/user/rgstephens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and pool league organizers use FargoRate to retrieve player ratings, compare match odds, get race-length guidance, and monitor rating or robustness changes over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned external fargo executable installed from a personal Homebrew tap.

Mitigation: Review the Homebrew tap and executable provenance before installation, and pin or otherwise verify the dependency where possible.

Risk: Using --db can persist player data and locally added contact details, and --changes can print those details in command output.

Mitigation: Use --db only when tracking is needed, keep the database in a private location, and avoid adding contact details if output may be logged, shared, or sent through bots.

## Reference(s):

- [FargoRate website](https://fargorate.com)
- [FargoRate skill homepage](https://github.com/rgstephens/fargo-skill)
- [ClawHub FargoRate skill page](https://clawhub.ai/rgstephens/skills/fargo)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a local SQLite database when --db is enabled; --json can emit raw API JSON.]

## Skill Version(s):

0.4.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
