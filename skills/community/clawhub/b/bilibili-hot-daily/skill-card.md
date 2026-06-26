## Description: <br>
Fetches Bilibili's public popular-video list, prints a ranked report, and can save JSON or CSV exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq853632587](https://clawhub.ai/user/qq853632587) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content analysts use this skill to fetch current Bilibili trending videos, inspect basic engagement metrics, and export the results for lightweight reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact documentation advertises AI summaries, scheduled daily runs, and messaging or email push integrations that are not evidenced in this release. <br>
Mitigation: Treat this version as a public Bilibili hot-list fetcher and local exporter only unless those additional workflows are separately verified. <br>
Risk: The --output option writes to the caller-supplied path and may overwrite an existing file. <br>
Mitigation: Choose output paths deliberately, write to a temporary or dedicated report directory, and review existing files before reusing a path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qq853632587/bilibili-hot-daily) <br>
- [Bilibili popular API endpoint](https://api.bilibili.com/x/web-interface/popular) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, files] <br>
**Output Format:** [Console text report, optional JSON file, or optional CSV file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs public Bilibili video ranking data and engagement metrics; optional --output writes to a caller-selected local path.] <br>

## Skill Version(s): <br>
2.1.2 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
