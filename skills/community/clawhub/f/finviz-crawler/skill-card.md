## Description:

Continuous financial news crawler for finviz.com with SQLite storage, article extraction, query tooling, and optional background service operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camopel](https://clawhub.ai/user/camopel)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to maintain a local financial news archive, monitor selected market tickers, and retrieve recent headlines or article content for summaries and digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may create persistent user-level background execution that runs across logins.

Mitigation: Review the service setup before installation, make service creation explicitly opt-in where possible, and know how to disable or remove the systemd or launchd entry.

Risk: The skill downloads dependencies and browser components for web crawling.

Mitigation: Install in an isolated Python environment, pin or review dependencies before use, and avoid running it on machines with sensitive files.

Risk: The crawler scrapes third-party sites and may use browser automation.

Mitigation: Run it on a network where this traffic is acceptable, confirm applicable site terms, and keep crawl intervals conservative.

Risk: The skill writes and deletes local article files as part of expiry and ticker removal behavior.

Mitigation: Use a dedicated data directory, review expiry settings before first run, and back up any local archive that must be retained.

Risk: The security guidance calls out ticker validation and Chromium sandbox settings for review.

Mitigation: Validate ticker inputs, inspect the browser launch configuration, and patch sandbox settings before use in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/camopel/skills/finviz-crawler)
- [Finviz](https://finviz.com)
- [PrivateApp](https://github.com/camopel/PrivateApp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with bash commands, plus text or JSON output from the query CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When installed and run, the crawler stores article metadata in SQLite and article content as local Markdown files.]

## Skill Version(s):

3.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
