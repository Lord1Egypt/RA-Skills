## Description:

Retrieves AI-related job listings from BOSS Zhipin for a specified city and domain, saves structured results, and summarizes new roles and market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[batiger](https://clawhub.ai/user/batiger)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and analysts use this skill to collect BOSS Zhipin AI job listings for a selected city, compare them with prior collections, and generate concise summaries and reports for application planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated BOSS Zhipin browser session through Chrome remote debugging.

Mitigation: Use a dedicated BOSS Zhipin account or session in a separate temporary Chrome profile and close the debugging browser immediately after use.

Risk: The skill may install Python dependencies automatically without enough safeguards.

Mitigation: Review package installation steps first and run the skill in an isolated workspace or virtual environment.

Risk: Generated CSV files can carry spreadsheet-related risk when opened directly.

Mitigation: Set explicit output paths and treat generated CSV files as untrusted before opening them in spreadsheet software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/batiger/skills/extract-boss-job)
- [BOSS Zhipin job search target](https://www.zhipin.com/web/geek/jobs?query=%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%B7%A5%E7%A8%8B%E5%B8%88&city=101020100)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated CSV, text, HTML, and optional image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local job data files and summaries; generated CSV files should be treated as untrusted before opening in spreadsheet software.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
