## Description: <br>
Batch-download formal A-share annual and semiannual report PDFs from CNInfo using a stock-code CSV, with dry-run preview, resume on failure, force redownload, and configurable year, filtering, timeout, and retry settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gclyde768-arch](https://clawhub.ai/user/gclyde768-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to fetch, re-fetch, or inspect CNInfo annual and semiannual report PDFs for A-share listed companies from a stock-code CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends stock codes from the provided CSV to CNInfo and downloads matching report PDFs over the network. <br>
Mitigation: Use only CSV contents you are comfortable sending to CNInfo, pass an explicit stock CSV and output/runtime directories, and run with --dry-run first. <br>
Risk: Resetting local state deletes download progress and can cause work to be repeated. <br>
Mitigation: Treat the documented reset command as destructive local state cleanup and confirm the runtime directory before deleting state files. <br>
Risk: Network availability, CNInfo response changes, or overly broad input CSVs can affect completeness and runtime. <br>
Mitigation: Review the generated manifest and logs after each run, and tune year, page size, timeout, retries, and stock-code scope as needed. <br>


## Reference(s): <br>
- [CNInfo Reports ClawHub Page](https://clawhub.ai/gclyde768-arch/cninfo-report-downloader) <br>
- [Filter Rules](references/filter_rules.md) <br>
- [CNInfo Full-Text Search](https://www.cninfo.com.cn/new/fulltextSearch) <br>
- [CNInfo Full-Text Search API](https://www.cninfo.com.cn/new/fulltextSearch/full) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; the skill-runner script produces PDF files, CSV manifests, SQLite state, and log files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads are scoped by stock-code CSV, target year, output directory, runtime directory, page size, timeout, retries, dry-run mode, and force-redownload mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
