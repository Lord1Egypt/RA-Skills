## Description: <br>
Collects public aviation information from agencies such as ICAO, FAA, EASA, and Korea's MOLIT, structures it as tagged JSON, and helps generate reports in Markdown, Excel, Word, or PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkbeomjun-gkgkgk](https://clawhub.ai/user/parkbeomjun-gkgkgk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and aviation analysts can use this skill to collect public aviation regulatory, safety, news, statistics, or certification information and organize it into local datasets and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public website collection can exceed site expectations or produce incomplete results if targets are broad or automated too aggressively. <br>
Mitigation: Keep target sites and queries explicit, respect robots.txt and rate limits, and record source URLs and collection timestamps. <br>
Risk: Generated datasets and reports can contain stale, incomplete, or incorrectly parsed aviation information. <br>
Mitigation: Review collected items and generated reports against the cited source pages before relying on them for operational or compliance decisions. <br>
Risk: Optional cron scheduling can cause recurring collection and repeated local file creation. <br>
Mitigation: Add scheduled jobs only when recurring collection is intended, and review schedule frequency, working directory, and output paths before enabling them. <br>
Risk: The artifact references helper scripts and optional document libraries that may not be present in every installed copy. <br>
Mitigation: Inspect any helper scripts and install optional dependencies from trusted sources before running report-generation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkbeomjun-gkgkgk/aviation-web-scraper) <br>
- [ICAO](https://www.icao.int) <br>
- [FAA](https://www.faa.gov) <br>
- [EASA](https://www.easa.europa.eu) <br>
- [Korea Ministry of Land, Infrastructure and Transport](https://www.molit.go.kr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas, shell command examples, and report-generation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON collections and Markdown, Excel, Word, or PDF reports when the user executes the described workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
