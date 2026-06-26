## Description: <br>
Searches Gangtise File Center across reports, announcements, meeting notes, opinions, and investment calendars, returning file IDs, key metadata, summaries, and optional download guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangtisegts](https://clawhub.ai/user/gangtisegts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, researchers, and agents use this skill to build candidate lists of Gangtise documents by type, date, security, institution, industry, or keyword before downloading or reviewing full files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and configured credentials are sent to Gangtise. <br>
Mitigation: Install and run the skill only when the publisher and Gangtise account context are trusted for the submitted queries and credentials. <br>
Risk: Downloads or saved results can write files into a local Gangtise workspace. <br>
Mitigation: Avoid automatic download or result-saving behavior in shared or regulated workspaces unless retention and cleanup are planned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gangtisegts/gangtise-file) <br>
- [Publisher profile](https://clawhub.ai/user/gangtisegts) <br>
- [Company announcement guide](artifact/references/announcement.md) <br>
- [Foreign report guide](artifact/references/foreign_report.md) <br>
- [File download guide](artifact/references/get_file.md) <br>
- [Investment calendar guide](artifact/references/investment_calendar.md) <br>
- [Opinion guide](artifact/references/opinion.md) <br>
- [Research report guide](artifact/references/report.md) <br>
- [Meeting summary guide](artifact/references/summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with inline shell commands and local file paths when downloads are requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gangtise access credentials and may write downloaded files or saved results to a local Gangtise workspace.] <br>

## Skill Version(s): <br>
1.4.12 (source: server release metadata; artifact frontmatter says 1.4.10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
