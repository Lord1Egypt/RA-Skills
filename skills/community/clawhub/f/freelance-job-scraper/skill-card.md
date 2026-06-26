## Description: <br>
Autonomous freelance job monitoring agent. Scans Hacker News Who is Hiring, YC jobs board, and remote job aggregators for high-value automation and AI gigs, scores them by relevance and payout, and flags actionable leads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanxevo3](https://clawhub.ai/user/lanxevo3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and freelance operators can use this skill to scan for AI, automation, and scraping-related job leads and produce a prioritized digest for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation claims coverage of YC Jobs, RemoteOK, and WeWorkRemotely, while the security evidence says those scanners are missing or undocumented. <br>
Mitigation: Treat the generated digest as partial coverage until the missing scanners are added or the documentation is corrected. <br>
Risk: The script uses the current authenticated GitHub CLI session for API requests. <br>
Mitigation: Run it only with a low-scope GitHub account or token that is acceptable for this workflow. <br>
Risk: The security verdict is suspicious due to overstated source coverage and a mismatched authenticated data source. <br>
Mitigation: Review the skill before installation and verify its data sources before using results for business decisions. <br>


## Reference(s): <br>
- [Freelance Job Scraper ClawHub page](https://clawhub.ai/lanxevo3/freelance-job-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown digest with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print a scored job-lead report and accepts keyword, minimum pay, and output-file options.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
