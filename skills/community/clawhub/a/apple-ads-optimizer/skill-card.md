## Description:

Optimizes the user's Apple Ads (Search Ads) campaigns through their connected Apple Ads account - reads the last 14 days of keyword and search term reports, raises bids on keywords that convert under the target CPA (capped +30% per run), lowers or pauses keywords that spend without installs, adds converting search terms as exact keywords and wasteful ones as negatives - every change a dry run with a diff the user approves. Use when the user says "optimize my Apple Ads", "Apple Search Ads bids", "which keywords are wasting money", "add negative keywords", "harvest search terms", "lower my CPA" or sets up a weekly ads review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafalzawadzki](https://clawhub.ai/user/rafalzawadzki)

### License/Terms of Use:

MIT

## Use Case:

App owners and marketers use this skill to review Apple Ads campaign performance and prepare bid, keyword, and negative keyword changes based on a target cost per acquisition. It summarizes proposed changes for review and can support a weekly optimization workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An optional unattended workflow or auto-apply rule can change live ad campaigns without a person reviewing each proposed change.

Mitigation: Start with read-only reports or interactive approvals. Before scheduling, require human approval in AppGoat and disable relevant auto-apply rules, or stop unattended runs after they create proposals.

Risk: AppGoat access can expose sensitive campaign data and allow potentially live campaign changes.

Mitigation: Pin a reviewed repository version and install only the needed playbook; limit unattended access to proposal creation unless live changes are explicitly intended.

## Reference(s):

- [REST API fallback guide](reference/api.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Markdown, Guidance]

**Output Format:** [Markdown campaign summary with proposed changes and approval guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the last 14 full days of campaign data and the user's target CPA; changes are normally proposed as dry runs for review, while unattended or auto-apply configurations can change live campaigns.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
