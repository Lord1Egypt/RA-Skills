## Description:

Automated daily literature search system for academic researchers. Performs scheduled searches across PubMed, OpenAlex, and Semantic Scholar with automatic deduplication, OA download, smart categorization, and daily reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzr101622](https://clawhub.ai/user/wzr101622)

### License/Terms of Use:

MIT-0

## Use Case:

Academic researchers use this skill to monitor recent literature across PubMed, OpenAlex, and Semantic Scholar, organize papers by configurable topics, and produce daily reports for ongoing reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can make persistent cron changes by default.

Mitigation: Review install.sh before execution, run dry-run or manual commands first, and add cron only after explicitly deciding unattended daily runs are appropriate.

Risk: Environment files may contain email addresses, API keys, or webhook secrets.

Mitigation: Avoid sourcing untrusted .env files as shell code and store real credentials in a controlled secret store or protected local environment.

Risk: Automatic downloads and external literature API calls can create storage, copyright, and rate-limit exposure.

Mitigation: Keep downloads limited to open-access or otherwise lawful papers, monitor disk usage, and configure API credentials and request limits responsibly.

Risk: The search script relies on a referenced literature-review skill path.

Mitigation: Verify the referenced literature-review skill path is present and trusted before running automated searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzr101622/skills/daily-literature-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, logs, local files, and command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local paper files, logs, reports, cron entries, and optional notifications when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
