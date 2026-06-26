## Description: <br>
Indexes EML emails into an SQLite database, providing a web interface for searching, management, Excel export, and file deletion, with IP access control and integrated JSON automated backup/restore. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamfromtw](https://clawhub.ai/user/williamfromtw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, records administrators, and email operations teams use this skill to index local EML archives, search email metadata and content, export selected results, and manage JSON backups from a local web interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local web admin features use a known default admin password. <br>
Mitigation: Change the admin password in config.json before starting the web app and restrict access to trusted local or protected networks. <br>
Risk: The database, CSV exports, and backup ZIPs can contain private email archive data. <br>
Mitigation: Store generated files in access-controlled locations and handle exports and backups as sensitive records. <br>
Risk: Delete and restore operations can alter database records and local email files. <br>
Mitigation: Take a separate backup before using delete or restore, and verify the selected records before confirming the operation. <br>
Risk: Runtime dependencies are declared without pinned versions. <br>
Mitigation: Pin and audit Flask and tqdm in a controlled environment before deployment. <br>


## Reference(s): <br>
- [Traditional Chinese Documentation](references/SKILL-TW.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/williamfromtw/eml-to-sqlite-indexer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python code, JSON configuration, SQLite data, CSV exports, and JSON backup ZIP files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill handles private email archives and can create, export, restore, and delete local email records and files.] <br>

## Skill Version(s): <br>
7.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
