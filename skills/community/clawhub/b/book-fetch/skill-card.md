## Description: <br>
Download ebooks (epub/pdf) from Anna's Archive and upload them to MEGA automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zerone0x](https://clawhub.ai/user/zerone0x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Book Fetch to search for a requested book, download an EPUB, PDF, or MOBI file through Anna's Archive/Libgen paths, and upload the result to a configured MEGA library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download books from Anna's Archive/Libgen sources and upload them to MEGA without a separate confirmation step. <br>
Mitigation: Use --dry-run for search-only review, use --pick -1 or an explicit --pick value for ambiguous titles, and confirm you have the right to download and store the requested book. <br>
Risk: Uploads depend on the local mega-put or rclone account configuration. <br>
Mitigation: Verify which MEGA account or rclone remote is authenticated before running the upload path. <br>
Risk: Downloaded files are cached locally in /tmp/books after the run. <br>
Mitigation: Review and remove cached files after use when local retention is not intended. <br>


## Reference(s): <br>
- [Book Fetch on ClawHub](https://clawhub.ai/zerone0x/book-fetch) <br>
- [Anna's Archive](https://annas-archive.li) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download ebook files to /tmp/books and upload them to a configured MEGA Books folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
