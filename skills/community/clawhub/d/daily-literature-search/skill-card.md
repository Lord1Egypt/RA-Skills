## Description: <br>
Automated daily literature search system for academic researchers. Performs scheduled searches across PubMed, OpenAlex, and Semantic Scholar with automatic deduplication, OA download, smart categorization, and daily reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wzr101622](https://clawhub.ai/user/Wzr101622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and research teams use this skill to monitor recent academic literature across PubMed, OpenAlex, and Semantic Scholar, deduplicate findings, organize open-access papers, and generate daily Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation can add recurring background execution through a cron job. <br>
Mitigation: Review install.sh, run the installer with --dry-run first, explicitly decide whether scheduled execution is desired, and use the uninstall option or remove the cron entry for manual-only use. <br>
Risk: The search script runs a local literature-review skill that is not clearly declared as a dependency. <br>
Mitigation: Verify that the referenced literature-review skill is present in the workspace and trusted before enabling scheduled runs. <br>
Risk: Configuration may include API keys, webhooks, and user email values. <br>
Mitigation: Keep .env and configuration files private, avoid adding real secrets until after review, and restrict file permissions where secrets are stored. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Wzr101622/daily-literature-search) <br>
- [Publisher profile](https://clawhub.ai/user/Wzr101622) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Configuration example](artifact/config.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, log text, organized local files, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download open-access PDFs and write logs, reports, and categorized paper files when configured to do so.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
