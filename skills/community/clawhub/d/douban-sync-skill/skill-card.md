## Description: <br>
Export and sync Douban book, movie, music, and game collections to local CSV files for local archive or Obsidian-style workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosformula](https://clawhub.ai/user/cosformula) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to export a Douban user's media history, run incremental RSS sync, migrate older Markdown exports, and manage the resulting local CSV archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves Douban media history, comments, ratings, and sync state as local files that may contain personal data. <br>
Mitigation: Keep DOUBAN_OUTPUT_DIR private, avoid public or unprotected cloud-shared folders, and handle generated CSV and state files as personal data. <br>
Risk: Browser-based full export connects to an existing logged-in Douban browser session. <br>
Mitigation: Use browser mode only with a session you intentionally expose to the scraper, and disconnect or close that browser session after export. <br>
Risk: A scheduled RSS sync can continue collecting new Douban activity over time. <br>
Mitigation: Enable cron only when ongoing automatic sync is intended, and remove the scheduled job when continuous collection is no longer needed. <br>
Risk: Full export and RSS requests may be rate limited or blocked by Douban. <br>
Mitigation: Use the documented delays and retry behavior, and pause scraping when rate limiting or blocking occurs. <br>


## Reference(s): <br>
- [Douban Sync ClawHub release page](https://clawhub.ai/cosformula/douban-sync-skill) <br>
- [Douban publisher profile](https://clawhub.ai/user/cosformula) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript helper scripts, CSV output files, and a JSON RSS state file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DOUBAN_USER. Generated files are written under DOUBAN_OUTPUT_DIR when set, otherwise under ~/douban-sync.] <br>

## Skill Version(s): <br>
0.2.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
