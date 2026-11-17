## Description:

Daily news briefing generator that produces conversational audio briefings and DOCX documents covering weather, X/Twitter trends, web trends, world news, politics, technology, local news, sports, markets, and crypto; it is macOS-only and uses local text-to-speech tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matusvojtek](https://clawhub.ai/user/matusvojtek)

### License/Terms of Use:


## Use Case:

External users use Briefing Room through an agent to gather current weather, trends, news, sports, market, and crypto information into a daily spoken briefing and companion document. Developers and power users can configure location, language, voice, sections, and output location for repeated personal briefing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleanup command can permanently delete unrelated date-named folders when output.folder is broad or misconfigured.

Mitigation: Use a dedicated Briefing Room output directory, avoid broad folders such as /tmp, ~/Documents, Desktop, or Downloads, and do not run the clean command until deletion is constrained with confirmation or ownership checks.

Risk: The skill performs web searches and API requests, starts a background generation session, and saves generated files to disk.

Mitigation: Install and run it only in environments where those network, background-session, and file-write behaviors are acceptable, and review the configured location and output folder before generating a briefing.

## Reference(s):

- [Briefing Room on ClawHub](https://clawhub.ai/matusvojtek/skills/briefing-room)
- [MLX-Audio](https://github.com/ml-explore/mlx-audio)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [Coinbase BTC Spot Price API](https://api.coinbase.com/v2/prices/BTC-USD/spot)
- [GetDayTrends](https://getdaytrends.com/)
- [Google Trends RSS](https://trends.google.com/trending/rss?geo=US)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash and Python command snippets; generated briefing artifacts are DOCX and MP3 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes a local configuration file, saves dated briefing outputs under the configured folder, and requires macOS plus internet access for the full workflow.]

## Skill Version(s):

1.0.3 (source: server release metadata and changelog, released 2026-02-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
