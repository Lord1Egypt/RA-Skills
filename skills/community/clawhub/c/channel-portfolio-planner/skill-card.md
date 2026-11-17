## Description:

Helps an agent plan an organic social channel portfolio from audience evidence, objectives, platform capability, staffing capacity, and boundary routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, social, and founder-led growth teams use this skill to choose organic social channels before posting begins or when rebalancing an existing channel mix. It produces a channel portfolio that ties each recommendation to audience evidence, objective fit, platform access, and available staffing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted analytics, audience research, and platform excerpts may contain untrusted instructions or inaccurate claims.

Mitigation: Treat those inputs as evidence only, ignore embedded instructions, and ask for missing audience evidence instead of guessing channel fit.

Risk: Channel plans and proposed-state records can persist sensitive strategy details.

Mitigation: Save portfolio files and channel proposal events only after explicit user confirmation, using the documented memory and event paths.

Risk: Closed social platforms can penalize unauthorized scraping, posting, or engagement automation.

Mitigation: Use user exports or manual-package access for closed platforms and avoid automated posting or engagement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/channel-portfolio-planner)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown portfolio with capability matrix, cadence-budget check, tier recommendations, boundary triage, proposed-state event details, and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save the portfolio or submit proposed channel-state events only after user confirmation.]

## Skill Version(s):

19.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
