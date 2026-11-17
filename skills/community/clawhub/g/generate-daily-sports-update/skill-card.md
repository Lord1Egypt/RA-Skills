## Description:

Runs the sports science crawler to generate a daily report, sync to Notion, and prevent duplicate content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w2478328197-arch](https://clawhub.ai/user/w2478328197-arch)

### License/Terms of Use:


## Use Case:

Developers and sports science practitioners use this skill to run a local crawler that gathers recent sports science and wearable technology updates, generates a daily Markdown report, syncs it to Notion, and avoids duplicate entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run unaudited local Python code and dependencies while using Notion credentials.

Mitigation: Install only from a trusted sports-science-daily checkout, review daily_sports_update.py and requirements.txt, use a dedicated virtual environment, pin and verify dependencies, and run from an owned directory.

Risk: The Notion token could allow broader workspace access than the daily report requires.

Mitigation: Restrict the Notion integration token to the minimum page and permissions needed for report sync.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/w2478328197-arch/skills/generate-daily-sports-update)
- [Project homepage](https://github.com/w2478328197-arch/sports-science-daily)
- [PubMed E-utilities endpoint](https://eutils.ncbi.nlm.nih.gov)
- [Notion API endpoint](https://api.notion.com)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown report, terminal output, local JSON history, and Notion page updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, installed project dependencies, NOTION_TOKEN, NOTION_PAGE_ID, and access to execute the local Python script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
