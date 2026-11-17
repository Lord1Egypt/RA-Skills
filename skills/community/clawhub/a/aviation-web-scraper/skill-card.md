## Description:

Collects aviation information from sources such as ICAO, FAA, EASA, and Korean aviation agencies, structures it as tagged JSON, and helps convert it into Word, Excel, PDF, or Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkbeomjun-gkgkgk](https://clawhub.ai/user/parkbeomjun-gkgkgk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and aviation operations users can use this skill to collect public aviation regulations, notices, safety information, news, statistics, and certification updates, then organize them into structured datasets and reports. It supports one-time collection and user-configured scheduled collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled collection can run more often than intended or accumulate reports over time.

Mitigation: Review cron examples before enabling them, run only the schedules needed, use a dedicated output directory, and check for overwrites or accumulated reports.

Risk: Optional document-generation packages can affect the user's Python environment.

Mitigation: Install optional packages in a virtual environment with pinned versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkbeomjun-gkgkgk/skills/aviation-web-scraper)
- [ClawHub publisher profile](https://clawhub.ai/user/parkbeomjun-gkgkgk)
- [ICAO](https://www.icao.int)
- [FAA](https://www.faa.gov)
- [EASA](https://www.easa.europa.eu)
- [Korean Ministry of Land, Infrastructure and Transport](https://www.molit.go.kr)
- [Korea Institute of Aviation Safety Technology](https://www.kiast.or.kr)
- [NTSB](https://www.ntsb.gov)
- [IATA](https://www.iata.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with JSON schemas, shell command examples, and report-generation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or guide creation of JSON collections, Markdown reports, Excel data, Word documents, PDFs, and cron schedule entries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
