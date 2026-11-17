## Description:

Helps agents assess Canadian federal Express Entry eligibility, estimate CRS and FSW selection scores, and monitor IRCC policy sources for changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forrest-tech](https://clawhub.ai/user/forrest-tech)

### License/Terms of Use:

MIT

## Use Case:

External users and immigration-support agents use this skill to triage Canadian federal Express Entry eligibility, estimate candidate scores from provided profile data, and identify current IRCC sources to verify before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRS and eligibility outputs can be incomplete, approximate, or outdated as immigration policy changes.

Mitigation: Treat outputs as estimates and verify them against current official IRCC sources or a qualified professional before making immigration decisions.

Risk: Policy monitoring and discovery behavior may fetch public pages, write local source/hash files, or add non-federal sources.

Mitigation: Review or disable auto_discover.py and cron monitoring when federal IRCC-only behavior or strict local-file control is required.

Risk: Fetched public policy pages are external untrusted content.

Mitigation: Use fetched pages only as policy text evidence, avoid submitting personal information to external sites, and do not execute instructions from page content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forrest-tech/skills/federal-immigration-expert)
- [Publisher profile](https://clawhub.ai/user/forrest-tech)
- [IRCC Express Entry rounds of invitations](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations.html)
- [IRCC category-based selection](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations/category-based-selection.html)
- [IRCC Canadian Experience Class eligibility](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/who-can-apply/canadian-experience-class.html)
- [IRCC Federal Skilled Worker eligibility](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/who-can-apply/federal-skilled-workers.html)
- [IRCC Federal Skilled Trades eligibility](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/who-can-apply/federal-skilled-trades.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell commands and tabular score details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate profile input can be supplied as stdin JSON to scripts/evaluator.py; eligibility and CRS outputs are estimates that require verification against current official IRCC sources.]

## Skill Version(s):

1.2.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
