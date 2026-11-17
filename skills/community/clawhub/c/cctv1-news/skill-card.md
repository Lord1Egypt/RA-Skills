## Description:

Fetches CCTV Xinwen Lianbo content and saves the daily program link, segment links, and summaries to a local text file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kawayixixing](https://clawhub.ai/user/kawayixixing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal automation users can fetch CCTV Xinwen Lianbo program metadata, video links, and segment summaries into dated local text files, either manually or through an optional scheduler.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be configured to run daily through cron, launchd, or Windows Task Scheduler.

Mitigation: Only add a scheduled task when recurring execution is intended, and remove or disable the task when daily collection is no longer needed.

Risk: The scraper writes local dated output files in the script directory.

Mitigation: Review the output location and file permissions before use, and periodically clean up or archive generated files.

Risk: The skill depends on live CCTV website structure and network access.

Mitigation: Run it in a virtual environment with pinned dependencies and review failures when CCTV page layout or connectivity changes.

## Reference(s):

- [Skill usage instructions](references/使用说明.md)
- [CCTV Xinwen Lianbo page](https://tv.cctv.com/lm/xwlb/)
- [ClawHub skill page](https://clawhub.ai/kawayixixing/skills/cctv1-news)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes a dated cctv_news_YYYYMMDD.txt file in the script directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
